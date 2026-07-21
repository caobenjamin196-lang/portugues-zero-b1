/* ai-grader.js — AI批改（DESIGN.md 3.4 节）
   方案A：用户自带 API Key（存 localStorage，不离开浏览器）
   方案B：生成预填充 prompt，复制到剪贴板，用户粘贴到任意 AI 对话框
*/

const AIGrader = (() => {

  function buildPrompt(question, userAnswer) {
    return `你是一位巴西葡语（PT-BR）教师，学生是西班牙语B2水平的中文母语者。请批改以下题目。

题目: ${question.prompt}
参考答案: ${question.referenceAnswer || '(开放题)'}
评分标准: ${question.scoringCriteria || '(按语言准确性综合评分)'}
学生答案: ${userAnswer}

请按以下格式输出（用中文）：
1. 得分: X/10
2. 错误标注: [具体错误位置]
3. 纠正: [正确形式]
4. 解释: [为什么错，与西班牙语的差异点]
5. 类似练习建议: [1-2个相关练习]`;
  }

  /* 方案A：调用用户配置的 AI API */
  async function gradeWithAI(question, userAnswer) {
    const s = Progress.loadSettings();
    if (!s.apiKey) throw new Error('未配置 API Key，请在仪表盘设置中填写，或切换方案B。');
    const prompt = buildPrompt(question, userAnswer);
    const response = await fetch(s.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${s.apiKey}`
      },
      body: JSON.stringify({
        model: s.apiModel || 'gpt-4o-mini',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.3
      })
    });
    if (!response.ok) {
      const text = await response.text().catch(() => '');
      throw new Error(`API 请求失败 HTTP ${response.status}: ${text.slice(0, 200)}`);
    }
    const json = await response.json();
    const content = json.choices && json.choices[0] && json.choices[0].message
      ? json.choices[0].message.content
      : JSON.stringify(json);
    return content;
  }

  /* 方案B：导出到 AI 对话框（复制 prompt 到剪贴板） */
  async function exportToAIPrompt(questions, userAnswers) {
    const blocks = questions.map((q, i) => `
题目${i + 1}: ${q.prompt}
我的答案: ${userAnswers[i]}
参考答案: ${q.referenceAnswer || '(开放题)'}
评分标准: ${q.scoringCriteria || '(按语言准确性综合评分)'}`).join('\n---\n');

    const fullPrompt = `请作为巴西葡语（PT-BR）教师批改以下练习（学生是西班牙语B2水平的中文母语者），逐题给出：得分(X/10)、错误标注、纠正、与西班牙语差异说明、类似练习建议。请用中文回复。\n${blocks}`;

    try {
      await navigator.clipboard.writeText(fullPrompt);
      return { ok: true, message: '已复制到剪贴板，请粘贴到AI对话框进行批改', prompt: fullPrompt };
    } catch (e) {
      // 剪贴板不可用时回退：显示文本让用户手动复制
      return { ok: false, message: '自动复制失败，请手动复制下方文本', prompt: fullPrompt };
    }
  }

  /* 统一入口：根据设置自动选择方案 */
  async function grade(question, userAnswer) {
    const s = Progress.loadSettings();
    if (s.aiMode === 'A' && s.apiKey) {
      const result = await gradeWithAI(question, userAnswer);
      return { mode: 'A', result };
    }
    const r = await exportToAIPrompt([question], [userAnswer]);
    return { mode: 'B', result: r.message, prompt: r.prompt };
  }

  return { buildPrompt, gradeWithAI, exportToAIPrompt, grade };
})();
