/* progress.js — localStorage 进度追踪（DESIGN.md 3.5 节数据结构） */

const Progress = (() => {
  const KEY = 'ptzb1_progress';
  const SETTINGS_KEY = 'ptzb1_settings';

  const defaultData = () => ({
    currentWeek: 1,
    totalStudyHours: 0,
    weeklyStats: {},          // { "w1": { studyTime, quizScore, completed } }
    mistakeBank: [],          // { week, question, userAnswer, correctAnswer, topic, reviewCount, lastReview, mastered }
    streak: { current: 0, best: 0, lastStudy: null }
  });

  const defaultSettings = () => ({
    aiMode: 'B',              // 'A' = 用户API Key, 'B' = 导出prompt
    apiKey: '',
    apiEndpoint: 'https://api.openai.com/v1/chat/completions',
    apiModel: 'gpt-4o-mini'
  });

  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return defaultData();
      return Object.assign(defaultData(), JSON.parse(raw));
    } catch (e) {
      console.error('进度数据损坏，重置', e);
      return defaultData();
    }
  }

  function save(data) {
    localStorage.setItem(KEY, JSON.stringify(data));
  }

  function loadSettings() {
    try {
      const raw = localStorage.getItem(SETTINGS_KEY);
      if (!raw) return defaultSettings();
      return Object.assign(defaultSettings(), JSON.parse(raw));
    } catch (e) {
      return defaultSettings();
    }
  }

  function saveSettings(s) {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(s));
  }

  /* 记录一次学习活动（更新 streak + totalStudyHours） */
  function touchStudy(hours) {
    const d = load();
    const today = new Date().toISOString().slice(0, 10);
    if (d.streak.lastStudy !== today) {
      const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
      if (d.streak.lastStudy === yesterday) {
        d.streak.current += 1;
      } else {
        d.streak.current = 1;
      }
      d.streak.lastStudy = today;
      d.streak.best = Math.max(d.streak.best, d.streak.current);
    }
    if (hours && hours > 0) d.totalStudyHours = Math.round((d.totalStudyHours + hours) * 10) / 10;
    save(d);
    return d;
  }

  function addStudyTime(week, hours) {
    const d = load();
    const wk = 'w' + week;
    if (!d.weeklyStats[wk]) d.weeklyStats[wk] = { studyTime: 0, quizScore: null, completed: false };
    d.weeklyStats[wk].studyTime = Math.round((d.weeklyStats[wk].studyTime + hours) * 10) / 10;
    d.totalStudyHours = Math.round((d.totalStudyHours + hours) * 10) / 10;
    save(d);
    touchStudy(0);
    return d;
  }

  /* 周考成绩录入（百分制）。自动推进 currentWeek。 */
  function recordQuizScore(week, score) {
    const d = load();
    const wk = 'w' + week;
    if (!d.weeklyStats[wk]) d.weeklyStats[wk] = { studyTime: 0, quizScore: null, completed: false };
    const prev = d.weeklyStats[wk].quizScore;
    d.weeklyStats[wk].quizScore = prev === null ? score : Math.max(prev, score);
    if (score >= 60) {
      d.weeklyStats[wk].completed = true;
      if (week >= d.currentWeek && week < 16) d.currentWeek = week + 1;
    }
    save(d);
    touchStudy(0);
    return d;
  }

  /* 写入错题本（去重：同周同题不重复添加，而是重置 mastered） */
  function addMistake(entry) {
    const d = load();
    const existing = d.mistakeBank.find(
      m => m.week === entry.week && m.question === entry.question
    );
    if (existing) {
      existing.userAnswer = entry.userAnswer;
      existing.mastered = false;
      existing.reviewCount = 0;
    } else {
      d.mistakeBank.push({
        week: entry.week,
        question: entry.question,
        userAnswer: entry.userAnswer,
        correctAnswer: entry.correctAnswer,
        topic: entry.topic || '综合',
        reviewCount: 0,
        lastReview: null,
        mastered: false
      });
    }
    save(d);
    return d;
  }

  function getPendingMistakes() {
    return load().mistakeBank.filter(m => !m.mastered);
  }

  function markMistakeReviewed(index, mastered) {
    const d = load();
    if (d.mistakeBank[index]) {
      d.mistakeBank[index].reviewCount += 1;
      d.mistakeBank[index].lastReview = new Date().toISOString().slice(0, 10);
      if (mastered) d.mistakeBank[index].mastered = true;
      save(d);
    }
    return d;
  }

  function removeMistake(index) {
    const d = load();
    d.mistakeBank.splice(index, 1);
    save(d);
    return d;
  }

  /* 导出 / 导入 */
  function exportJSON() {
    return JSON.stringify({ progress: load(), settings: loadSettings(), exportedAt: new Date().toISOString() }, null, 2);
  }

  function importJSON(text) {
    const obj = JSON.parse(text);
    if (!obj.progress) throw new Error('文件格式不正确：缺少 progress 字段');
    save(Object.assign(defaultData(), obj.progress));
    if (obj.settings) saveSettings(Object.assign(defaultSettings(), obj.settings));
    return true;
  }

  function resetAll() {
    localStorage.removeItem(KEY);
    localStorage.removeItem(SETTINGS_KEY);
  }

  return {
    load, save, loadSettings, saveSettings,
    touchStudy, addStudyTime, recordQuizScore,
    addMistake, getPendingMistakes, markMistakeReviewed, removeMistake,
    exportJSON, importJSON, resetAll
  };
})();
