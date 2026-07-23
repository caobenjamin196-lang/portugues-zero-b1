/* app.js — 主逻辑：仪表盘渲染、导航、设置（DESIGN.md 3.6 节） */

/* ===== 通用工具 ===== */
function toast(msg, ms) {
  let el = document.querySelector('.toast');
  if (!el) {
    el = document.createElement('div');
    el.className = 'toast';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), ms || 2600);
}

function renderHeader(active) {
  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <a class="brand" href="${Data.basePath()}index.html"><span class="flag">🇧🇷</span> Português Zero → B1</a>
    <nav class="site-nav">
      <a href="${Data.basePath()}index.html" data-nav="dashboard">📊 仪表盘</a>
      <a href="${Data.basePath()}index.html#weeks" data-nav="weeks">📚 课程</a>
      <a href="${Data.basePath()}index.html#mistakes" data-nav="mistakes">📝 错题本</a>
      <a href="${Data.basePath()}flashcards.html" data-nav="flashcards">🃏 单词卡</a>
      <a href="${Data.basePath()}index.html#settings" data-nav="settings">⚙️ 设置</a>
    </nav>`;
  document.body.prepend(header);
  if (active) {
    const a = header.querySelector(`[data-nav="${active}"]`);
    if (a) a.classList.add('active');
  }
}

function renderFooter() {
  const f = document.createElement('footer');
  f.className = 'site-footer';
  f.innerHTML = `🇧🇷 Português Zero → B1 · 为西班牙语B2学习者设计的16周巴西葡语速成程序 · MIT License`;
  document.body.appendChild(f);
}

/* ===== 仪表盘 ===== */
async function initDashboard() {
  const root = document.getElementById('dashboard');
  if (!root) return;

  let curriculum;
  try {
    curriculum = await Data.loadCurriculum();
  } catch (e) {
    root.innerHTML = `<div class="card"><p>⚠️ 课程数据加载失败：${e.message}</p>
      <p class="text-dim">请通过本地服务器访问（python3 -m http.server），不要直接双击 html 文件。</p></div>`;
    return;
  }

  const d = Progress.load();
  const s = Progress.loadSettings();
  const cur = curriculum.weeks.find(w => w.week === d.currentWeek) || curriculum.weeks[0];
  const curStats = d.weeklyStats['w' + cur.week] || { studyTime: 0, quizScore: null, completed: false };
  const pending = Progress.getPendingMistakes();
  const fcPool = (typeof Progress.getFlashcards === 'function') ? Progress.getFlashcards() : [];

  const weekPct = Math.min(100, Math.round((curStats.studyTime / 3) * 100));

  /* 成绩走势 */
  const trend = curriculum.weeks.map(w => {
    const st = d.weeklyStats['w' + w.week];
    const score = st && st.quizScore !== null && st.quizScore !== undefined ? st.quizScore : null;
    const h = score === null ? 4 : Math.max(4, Math.round(score * 0.8));
    const cls = score === null ? 'empty' : score >= 80 ? '' : score >= 60 ? 'mid' : 'low';
    return `<div class="score-bar" title="W${w.week} ${w.title}：${score === null ? '未考' : score + '分'}">
      <div class="bar ${cls}" style="height:${h}px"></div><div class="wl">W${w.week}</div></div>`;
  }).join('');

  /* 周列表 */
  const weekItems = curriculum.weeks.map(w => {
    const st = d.weeklyStats['w' + w.week];
    const done = st && st.completed;
    const isCurrent = w.week === d.currentWeek;
    const cls = done ? 'done' : isCurrent ? 'current' : '';
    const scoreBadge = st && st.quizScore !== null && st.quizScore !== undefined
      ? `<span class="badge ${st.quizScore >= 60 ? 'badge-green' : 'badge-red'}">${st.quizScore}分</span>` : '';
    return `<a class="week-item ${cls}" href="${Data.basePath()}theory/${w.theoryPage}">
      <div class="week-num">W${w.week}</div>
      <div class="meta">
        <div class="title">${w.title} ${done ? '✅' : isCurrent ? '👈 当前' : ''}</div>
        <div class="desc">${w.grammar}</div>
      </div>
      ${scoreBadge}
    </a>`;
  }).join('');

  /* 错题本 */
  const mistakeRows = pending.slice(0, 20).map((m) => {
    const idx = d.mistakeBank.indexOf(m);
    return `<div class="vocab-item" style="align-items:flex-start">
      <div style="flex:1">
        <div><span class="badge badge-blue">W${m.week}</span> <span class="badge badge-gray">${m.topic}</span></div>
        <div class="mt-1">${m.question}</div>
        <div class="text-dim" style="font-size:0.85rem">你的答案：<span style="color:var(--danger)">${m.userAnswer}</span> ・ 正确：<span style="color:var(--success)">${m.correctAnswer}</span></div>
      </div>
      <button class="btn btn-sm btn-outline" onclick="masterMistake(${idx})">已掌握</button>
    </div>`;
  }).join('') || '<p class="text-dim">暂无错题，继续保持！🎉</p>';

  root.innerHTML = `
    <section class="dash-hero">
      <h1>🇧🇷 Português Zero → B1</h1>
      <div class="sub">Semana ${d.currentWeek} de 16 · 连续学习 <span class="streak-flame">${d.streak.current} 天 🔥</span>（最佳 ${d.streak.best} 天）· 累计 ${d.totalStudyHours}h</div>
    </section>

    <div class="grid grid-3">
      <div class="card card-accent-green no-hover stat"><div class="num">${d.currentWeek}/16</div><div class="label">当前周</div></div>
      <div class="card card-accent-yellow no-hover stat"><div class="num">${d.totalStudyHours}h</div><div class="label">累计学习</div></div>
      <div class="card card-accent-blue no-hover stat"><div class="num">${pending.length}</div><div class="label">待复习错题</div></div>
    </div>

    <div class="card card-accent-green no-hover">
      <div class="flex-between">
        <h3>📊 本周进度（W${cur.week} · ${cur.title}）</h3>
        <span class="text-dim">${curStats.studyTime}h / 3.0h · ${weekPct}%</span>
      </div>
      <div class="progress-bar mt-1"><div class="fill" style="width:${weekPct}%"></div></div>
      <div class="flex mt-2">
        <button class="btn btn-outline btn-sm" onclick="logStudyTime(${cur.week})">⏱ 记录 30 分钟学习</button>
      </div>
    </div>

    <div class="card card-accent-yellow no-hover">
      <h3>📖 当前课程：W${cur.week} - ${cur.title}</h3>
      <p class="text-dim">${cur.grammar}</p>
      <div class="flex mt-2">
        <a class="btn btn-primary" href="${Data.basePath()}theory/${cur.theoryPage}">继续学习 →</a>
        <a class="btn btn-secondary" href="${Data.basePath()}quiz.html?week=${cur.week}">开始周考 📝</a>
        ${cur.week <= 4 ? `<a class="btn btn-outline" href="${Data.basePath()}vocab.html?week=${cur.week}">📚 本周词汇 100 词</a>` : ''}
      </div>
    </div>

    <div class="card card-accent-blue no-hover">
      <h3>📚 每周频率词汇（W1-W4 · 每周 100 词）</h3>
      <p class="text-dim">按使用频率排序：W1 = 排名 1-100 · W2 = 101-200 · W3 = 201-300 · W4 = 301-400 · 🔊 点读发音（pt-BR）· 动词附现在时变位表与西语对照 · 假朋友警示</p>
      <div class="flex mt-2">
        <a class="btn btn-primary btn-sm" href="${Data.basePath()}vocab.html?week=1">W1 · 1-100</a>
        <a class="btn btn-primary btn-sm" href="${Data.basePath()}vocab.html?week=2">W2 · 101-200</a>
        <a class="btn btn-primary btn-sm" href="${Data.basePath()}vocab.html?week=3">W3 · 201-300</a>
        <a class="btn btn-primary btn-sm" href="${Data.basePath()}vocab.html?week=4">W4 · 301-400</a>
      </div>
    </div>

    <div class="card card-accent-yellow no-hover">
      <div class="flex-between">
        <h3>🃏 单词卡 · ${fcPool.length} 张待过关</h3>
        <a class="btn btn-primary btn-sm" href="${Data.basePath()}flashcards.html">练习单词卡 →</a>
      </div>
      <p class="text-dim">周考答错的词汇题自动入卡 · 专项考试累计答对 3 次过关移出 · 任何考试再答错该词即重新入卡并清零进度</p>
    </div>

    <div class="card no-hover" id="mistakes">
      <div class="flex-between"><h3>📝 错题本（${pending.length} 题待复习）</h3></div>
      <div class="vocab-list mt-1">${mistakeRows}</div>
    </div>

    <div class="card no-hover">
      <h3>📈 成绩走势（W1-W16）</h3>
      <div class="score-trend mt-2">${trend}</div>
    </div>

    <h3 class="mt-3 mb-1" id="weeks">📚 全部课程</h3>
    <div class="week-list">${weekItems}</div>

    <div class="card no-hover mt-3" id="settings">
      <h3>⚙️ 设置</h3>
      <label>AI 批改方案（DESIGN.md 3.4 节）</label>
      <div class="flex">
        <label style="margin:0;font-weight:400"><input type="radio" name="aiMode" value="A" ${s.aiMode === 'A' ? 'checked' : ''} style="width:auto"> 方案A：自带 API Key 自动批改</label>
        <label style="margin:0;font-weight:400"><input type="radio" name="aiMode" value="B" ${s.aiMode === 'B' ? 'checked' : ''} style="width:auto"> 方案B：导出 prompt 手动粘贴</label>
      </div>
      <div id="apiKeyZone" class="${s.aiMode === 'A' ? '' : 'hidden'}">
        <label>API Key（仅存于本机 localStorage，不会上传）</label>
        <input type="password" id="apiKeyInput" value="${s.apiKey}" placeholder="sk-...">
        <label>API Endpoint</label>
        <input type="text" id="apiEndpointInput" value="${s.apiEndpoint}">
        <label>模型</label>
        <input type="text" id="apiModelInput" value="${s.apiModel}">
      </div>
      <div class="flex mt-2">
        <button class="btn btn-primary btn-sm" onclick="saveSettingsUI()">💾 保存设置</button>
        <button class="btn btn-outline btn-sm" onclick="exportProgress()">📤 导出进度 JSON</button>
        <button class="btn btn-outline btn-sm" onclick="document.getElementById('importFile').click()">📥 导入进度 JSON</button>
        <input type="file" id="importFile" accept=".json" class="hidden" onchange="importProgress(this)">
        <button class="btn btn-danger btn-sm" onclick="resetProgress()">🗑 清空全部数据</button>
      </div>
    </div>
  `;

  document.querySelectorAll('input[name="aiMode"]').forEach(r => {
    r.addEventListener('change', () => {
      document.getElementById('apiKeyZone').classList.toggle('hidden', r.value !== 'A' || !r.checked);
      document.getElementById('apiKeyZone').classList.toggle('hidden',
        document.querySelector('input[name="aiMode"]:checked').value !== 'A');
    });
  });

  Progress.touchStudy(0);
}

function masterMistake(idx) {
  Progress.markMistakeReviewed(idx, true);
  toast('✅ 已标记为掌握');
  initDashboard();
}

function logStudyTime(week) {
  Progress.addStudyTime(week, 0.5);
  toast('⏱ 已记录 30 分钟');
  initDashboard();
}

function saveSettingsUI() {
  const s = Progress.loadSettings();
  s.aiMode = document.querySelector('input[name="aiMode"]:checked').value;
  s.apiKey = document.getElementById('apiKeyInput').value.trim();
  s.apiEndpoint = document.getElementById('apiEndpointInput').value.trim() || s.apiEndpoint;
  s.apiModel = document.getElementById('apiModelInput').value.trim() || s.apiModel;
  Progress.saveSettings(s);
  toast('💾 设置已保存');
}

function exportProgress() {
  const blob = new Blob([Progress.exportJSON()], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `ptzb1-progress-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
  toast('📤 进度已导出');
}

function importProgress(input) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      Progress.importJSON(reader.result);
      toast('📥 导入成功');
      initDashboard();
    } catch (e) {
      toast('⚠️ 导入失败：' + e.message, 4000);
    }
  };
  reader.readAsText(file);
  input.value = '';
}

function resetProgress() {
  if (confirm('确定要清空全部学习数据吗？此操作不可撤销。')) {
    Progress.resetAll();
    toast('🗑 数据已清空');
    initDashboard();
  }
}
