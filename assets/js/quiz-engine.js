/* quiz-engine.js — 自动批改引擎（DESIGN.md 3.3 节）
   支持题型：single_choice / multi_choice / fill_blank / matching /
            ordering / accent_mark / conjugation / translation
*/

const QuizEngine = (() => {

  /* 填空题容错规则（DESIGN.md 3.3） */
  function normalizeAnswer(str) {
    return String(str == null ? '' : str)
      .toLowerCase()
      .trim()
      .replace(/\s+/g, ' ')
      .replace(/[.,!?;:"""'']/g, '')
      .replace(/[áàãâä]/g, 'a')
      .replace(/[éèêë]/g, 'e')
      .replace(/[íìîï]/g, 'i')
      .replace(/[óòõôö]/g, 'o')
      .replace(/[úùûü]/g, 'u')
      .replace(/ç/g, 'c');
  }

  /* 变位题：接受多个正确答案 */
  function checkConjugation(userAnswer, acceptableForms) {
    const normalized = normalizeAnswer(userAnswer);
    return acceptableForms.some(form => normalizeAnswer(form) === normalized);
  }

  /* 检查单个文本答案是否命中 answer（string 或 string[]） */
  function checkTextAnswer(userAnswer, answer) {
    const forms = Array.isArray(answer) ? answer : [answer];
    return checkConjugation(userAnswer, forms);
  }

  function answerToDisplay(answer) {
    if (Array.isArray(answer)) return answer.join(' / ');
    if (answer && typeof answer === 'object') {
      return Object.entries(answer).map(([k, v]) => `${k}: ${v}`).join('，');
    }
    return String(answer);
  }

  /**
   * 批改单题。
   * @param q 题目对象
   * @param userAnswer 用户答案（题型相关结构）
   * @returns {{correct:boolean, partial:number, maxPartial:number}}
   *   partial/maxPartial 用于 multi_choice、conjugation 的部分给分
   */
  function grade(q, userAnswer) {
    switch (q.type) {
      case 'single_choice': {
        const ok = normalizeAnswer(userAnswer) === normalizeAnswer(q.answer);
        return { correct: ok, partial: ok ? 1 : 0, maxPartial: 1 };
      }

      case 'accent_mark': {
        // 重音标注题：严格比较，重音符号不容错（否则失去考点）
        const strict = s => String(s == null ? '' : s).toLowerCase().trim().replace(/\s+/g, ' ');
        const ok = strict(userAnswer) === strict(q.answer);
        return { correct: ok, partial: ok ? 1 : 0, maxPartial: 1 };
      }

      case 'multi_choice': {
        const want = new Set((Array.isArray(q.answer) ? q.answer : [q.answer]).map(normalizeAnswer));
        const got = new Set((userAnswer || []).map(normalizeAnswer));
        let hits = 0;
        got.forEach(g => { if (want.has(g)) hits++; });
        const wrongPicks = got.size - hits;
        const partial = Math.max(0, hits - wrongPicks);
        return {
          correct: hits === want.size && wrongPicks === 0,
          partial,
          maxPartial: want.size
        };
      }

      case 'fill_blank':
      case 'translation': {
        if (Array.isArray(q.blanks)) {
          // 多空题：answer 为数组的数组
          let hits = 0;
          q.blanks.forEach((acceptable, i) => {
            if (checkTextAnswer((userAnswer || [])[i] || '', acceptable)) hits++;
          });
          return { correct: hits === q.blanks.length, partial: hits, maxPartial: q.blanks.length };
        }
        const ok = checkTextAnswer(userAnswer || '', q.answer);
        return { correct: ok, partial: ok ? 1 : 0, maxPartial: 1 };
      }

      case 'conjugation': {
        // answer: { 人称: 正确形式 }，userAnswer: { 人称: 用户输入 }
        const persons = Object.keys(q.answer);
        let hits = 0;
        persons.forEach(p => {
          const ua = (userAnswer || {})[p] || '';
          if (checkTextAnswer(ua, q.answer[p])) hits++;
        });
        return { correct: hits === persons.length, partial: hits, maxPartial: persons.length };
      }

      case 'matching': {
        // answer: { 左项: 右项 }，userAnswer: { 左项: 用户选的右项 }
        const keys = Object.keys(q.answer);
        let hits = 0;
        keys.forEach(k => {
          if (normalizeAnswer((userAnswer || {})[k] || '') === normalizeAnswer(q.answer[k])) hits++;
        });
        return { correct: hits === keys.length, partial: hits, maxPartial: keys.length };
      }

      case 'ordering': {
        // answer: 正确顺序的数组，userAnswer: 用户排列的数组
        const want = (q.answer || []).map(normalizeAnswer);
        const got = (userAnswer || []).map(normalizeAnswer);
        let hits = 0;
        for (let i = 0; i < want.length; i++) if (want[i] === got[i]) hits++;
        return { correct: hits === want.length && want.length === got.length, partial: hits, maxPartial: want.length };
      }

      default:
        return { correct: false, partial: 0, maxPartial: 1 };
    }
  }

  /* 错题本条目构造 */
  function mistakeEntry(week, q, userAnswer) {
    let ua = userAnswer, ca = q.answer;
    if (q.type === 'fill_blank' && Array.isArray(q.blanks)) ca = q.blanks.map(b => Array.isArray(b) ? b[0] : b).join(' / ');
    return {
      week,
      question: `[${q.id}] ${q.prompt}`,
      userAnswer: typeof ua === 'object' ? JSON.stringify(ua) : String(ua == null ? '' : ua),
      correctAnswer: answerToDisplay(ca),
      topic: q.topic || q.type
    };
  }

  return { normalizeAnswer, checkConjugation, checkTextAnswer, grade, answerToDisplay, mistakeEntry };
})();
