/* data.js — 题库/课程数据加载 */

const Data = (() => {
  const cache = {};

  async function fetchJSON(url) {
    if (cache[url]) return cache[url];
    const res = await fetch(url);
    if (!res.ok) throw new Error(`加载失败 ${url}: HTTP ${res.status}`);
    const json = await res.json();
    cache[url] = json;
    return json;
  }

  function basePath() {
    // 页面可能在根目录或子目录；通过 script 标签定位 assets 路径
    const scripts = document.querySelectorAll('script[src]');
    for (const s of scripts) {
      const src = s.getAttribute('src');
      const idx = src.indexOf('assets/js/data.js');
      if (idx >= 0) return src.slice(0, idx);
    }
    return '';
  }

  async function loadCurriculum() {
    return fetchJSON(basePath() + 'data/curriculum.json');
  }

  async function loadQuiz(week) {
    const w = String(week).padStart(2, '0');
    return fetchJSON(basePath() + `exercises/w${w}-quiz.json`);
  }

  async function loadVocabulary() {
    return fetchJSON(basePath() + 'data/vocabulary.json');
  }

  async function loadVerbConjugations() {
    return fetchJSON(basePath() + 'data/verb-conjugations.json');
  }

  return { loadCurriculum, loadQuiz, loadVocabulary, loadVerbConjugations, basePath };
})();
