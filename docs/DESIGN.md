# 🇧🇷 Português Zero → B1 — 西语B2基础者的葡语速成程序

## 项目设计文档 v1.0

**作者**: 鲶鱼军师🐟 为大王设计
**日期**: 2026-07-21
**变体**: 巴西葡语（PT-BR）
**基础**: 西班牙语B2（可大量语法迁移）
**目标**: CEFR B1（阅读新闻、日常交流、写短文）
**节奏**: 每周3小时，共16周
**部署**: GitHub Pages 纯前端 + AI批改

---

## 一、核心设计理念

### 1.1 为什么16周而不是更长？

西语B2基础意味着：
- **词汇重叠~70%**：约60%词汇直接可用，10%需微调（如 -ción → -ção）
- **语法框架共享**：ser/estar、阴阳性、动词变位体系、SVO语序、subjuntivo概念
- **可跳过的内容**：基础发音（部分）、阴阳性概念、基础句法、ser/estar区分

**需要聚焦的差异点**：
1. 发音（葡语14个元音 vs 西语5个）
2. 人称代词省略规则差异（PT-BR更倾向保留主语）
3. 虚拟式未来时（葡语有，西语已废弃）
4. 动词变位差异（特别是ter vs tener、ir变位、过去完成时）
5. 介词使用差异（em vs en、para vs por）
6. 葡语独有结构（被动语态se + verbo、不定式人称化）
7. 词汇假朋友（embarazada vs embaraçada、exquisito vs esquisito等）

### 1.2 "A+AI"考试纠错机制

- **A（自动）**：题库预置 + 程序自动批改选择题/填空题/匹配题
- **AI（智能）**：开放性问答/翻译/写作题 → 调用AI API批改 + 生成错题分析

纯前端无法直接调AI API（密钥不能暴露），方案：
- **方案**：前端自动批改客观题 + 导出主观题答案 → 用户手动粘贴到AI对话框批改
- **或**：用户自带API Key（如OpenAI），前端直接调用，密钥存localStorage

---

## 二、16周课程大纲

### Phase 1: 发音与基础迁移（第1-4周）

> 目标：掌握PT-BR发音系统，完成西语→葡语的语法迁移

| 周 | 主题 | 语法重点 | 阅读 | 周考形式 |
|---|---|---|---|---|
| W1 | 发音系统：14个元音+鼻元音+半元音 | 字母→音素映射规则；重音规则 | 短句朗读+拼音练习 | 听辨选择+重音标注 |
| W2 | 名词/冠词/形容词：阴阳性转移规则 | -ción→-ção、-dad→-dade、-ón→-ão；形容词后置；复数规则 | 简短描述文（自我介绍、家庭） | 选词填空+词性转换 |
| W3 | 动词现在时：规则动词+-ar/-er/-ir | ser/estar差异（与西语对比）；ter/haver/fazer/ir不规则；代词省略规则 | 日常对话短文（餐厅、购物） | 变位填空+翻译 |
| W4 | 介词与连词 | em/de/para/por vs en/de/para/por；contractions（no/na/do/da）；连词差异 | 短新闻（100-150词） | 介词选择+句型改写 |

**W4 周考（Phase 1结业考）**：
- 自动：30题选择+填空（发音、词性、变位、介词）
- AI：1段80词翻译（西→葡）+ 1段自我介绍写作（50词）

---

### Phase 2: 时态体系（第5-8周）

> 目标：掌握葡语全部核心时态，能阅读简单新闻和故事

| 周 | 主题 | 语法重点 | 阅读 | 周考形式 |
|---|---|---|---|---|
| W5 | 过去时：pretérito perfeito vs imperfeito | 与西语pretérito/imperfecto对应；PT-BR用法差异；不规则动词（foi/esteve/teve） | 短篇故事（300词） | 时态选择+动词变位 |
| W6 | 进行时与完成时 | estar+gerúndio vs estar+andando；pretérito composto（tenho falado）；与西语差异 | 新闻报道（200词） | 时态转换+阅读理解 |
| W7 | 将来时与条件式 | futuro do presente（falarei）；futuro do pretérito（falaria）= 西语condicional；ir+infinitivo | 预测/计划类文章 | 填空+翻译 |
| W8 | 虚拟式：presente + pretérito imperfeito | subjuntivo presente（与西语高度相似）；subjuntivo imperfeito（葡语独有用法）；触发词对比 | 评论/观点文章（250词） | 虚拟式选择+句型改写 |

**W8 周考（Phase 2结业考）**：
- 自动：40题（时态、虚拟式、不规则变位）
- AI：1段150词新闻翻译 + 1段观点写作（100词，要求使用至少3种时态）

---

### Phase 3: 复杂结构与阅读强化（第9-12周）

> 目标：掌握葡语独有结构，能阅读中等长度文章

| 周 | 主题 | 语法重点 | 阅读 | 周考形式 |
|---|---|---|---|---|
| W9 | 虚拟式未来时 + 被动语态 | futuro do subjuntivo（西语已废弃，葡语独有）；se+verbo被动；被动结构对比 | 法律/正式文书片段 | 虚拟式未来填空+被动改写 |
| W10 | 不定式与动名词 | infinitivo pessoal（人称化不定式，葡语独有）；gerúndio vs infinitivo选择 | 报刊专栏（350词） | 不定式人称化填空+阅读理解 |
| W11 | 关系代词与从句 | que/quem/cujo/onde/o qual；关系从句 vs 西语差异；定语从句结构 | 传记/历史文章（400词） | 关系代词选择+从句合并 |
| W12 | 假朋友与词汇深化 | 50个高频假朋友（embarazada/embaraçada等）；同源词变形规则；巴西俚语入门 | 文学片段（500词） | 词汇辨析+翻译+阅读理解 |

**W12 周考（Phase 3结业考）**：
- 自动：40题（虚拟式未来、不定式人称化、关系代词、假朋友）
- AI：1段250词专栏翻译 + 1段评论写作（150词）

---

### Phase 4: B1综合应用（第13-16周）

> 目标：综合运用，达到CEFR B1水平

| 周 | 主题 | 语法重点 | 阅读 | 周考形式 |
|---|---|---|---|---|
| W13 | 阅读强化：新闻 | 时态混合运用；新闻体词汇；标题缩略语法 | 3篇真实新闻（每篇300-400词） | 阅读理解+词汇+翻译 |
| W14 | 阅读强化：文学 | 文学时态用法；叙述体；对话描写 | 短篇小说（800-1000词） | 阅读理解+语法分析 |
| W15 | 写作强化 | 论证结构；连接词；正式/非正式语域 | 范文3篇（议论文/邮件/评论） | AI批改：1篇200词议论文 |
| W16 | 综合复习 + 模拟B1考试 | 全部语法点查漏补缺 | 综合阅读（800词） | **B1模拟考** |

**W16 B1模拟考试**（期末）：
- Part 1 阅读理解（30分钟）：2篇文章 + 20题
- Part 2 语法与词汇（20分钟）：40题
- Part 3 翻译（15分钟）：1段100词（西→葡）
- Part 4 写作（25分钟）：1篇150词议论文
- 自动批改：Part 1+2（60题）
- AI批改：Part 3+4

---

## 三、技术架构

### 3.1 项目结构

```
portugues-zero-b1/
├── index.html                 # 主页（学习仪表盘）
├── theory/
│   ├── w01-pronunciation.html # 第1周语法讲解
│   ├── w02-nouns-articles.html
│   ├── w03-present-tense.html
│   ├── ...
│   └── w16-review.html
├── exercises/
│   ├── w01-quiz.json          # 第1周自动批改题库
│   ├── w02-quiz.json
│   ├── ...
│   └── w16-final-exam.json
├── readings/
│   ├── w01-short-sentences.txt
│   ├── w05-short-story.txt
│   ├── w13-news-1.txt
│   └── ...
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js             # 主逻辑
│   │   ├── quiz-engine.js     # 自动批改引擎
│   │   ├── ai-grader.js       # AI批改接口
│   │   ├── progress.js        # 进度追踪
│   │   └── data.js            # 题库加载
│   └── audio/                 # 发音音频（TTS生成或外链）
│       └── ...
├── data/
│   ├── curriculum.json        # 课程大纲数据
│   ├── vocabulary.json        # 词汇表（含假朋友）
│   ├── verb-conjugations.json # 动词变位表
│   └── progress.json          # 用户进度（localStorage）
├── README.md
└── LICENSE
```

### 3.2 技术栈

```
纯前端，无后端依赖：
├── HTML5              # 页面结构
├── CSS3               # 样式（响应式，支持手机）
├── Vanilla JavaScript # 逻辑（无框架依赖，降低维护成本）
├── JSON               # 题库/词汇/课程数据
└── localStorage       # 进度存储（无需数据库）
```

### 3.3 自动批改引擎（Quiz Engine）

支持题型：
```javascript
// 题型枚举
const QUESTION_TYPES = {
  SINGLE_CHOICE: 'single_choice',    // 单选
  MULTI_CHOICE: 'multi_choice',      // 多选
  FILL_BLANK: 'fill_blank',          // 填空（精确匹配/容错）
  MATCHING: 'matching',              // 连线匹配
  ORDERING: 'ordering',              // 排序
  ACCENT_MARK: 'accent_mark',        // 重音标注
  CONJUGATION: 'conjugation',        // 动词变位
  TRANSLATION_CHECK: 'translation'   // 翻译对照（自动评分）
};
```

批改逻辑：
```javascript
// 填空题容错规则
function normalizeAnswer(str) {
  return str
    .toLowerCase()
    .trim()
    .replace(/\s+/g, ' ')           // 多空格→单空格
    .replace(/[.,!?;:]/g, '')       // 忽略标点
    .replace(/áàãâä/g, 'a')          // 元音容错（初级阶段）
    .replace(/éèêë/g, 'e')
    .replace(/íìîï/g, 'i')
    .replace(/óòõôö/g, 'o')
    .replace(/úùûü/g, 'u')
    .replace(/ç/g, 'c');
}

// 变位题：接受多个正确答案
function checkConjugation(userAnswer, acceptableForms) {
  const normalized = normalizeAnswer(userAnswer);
  return acceptableForms.some(form => normalizeAnswer(form) === normalized);
}
```

### 3.4 AI批改接口（ai-grader.js）

方案A：用户自带API Key
```javascript
// 用户在设置页输入自己的API Key
// 存储在 localStorage，不离开浏览器
async function gradeWithAI(question, userAnswer, apiKey) {
  const prompt = `
    你是一位巴西葡语教师。请批改以下题目。

    题目: ${question.prompt}
    参考答案: ${question.referenceAnswer}
    学生答案: ${userAnswer}

    请按以下格式输出：
    1. 得分: X/10
    2. 错误标注: [具体错误位置]
    3. 纠正: [正确形式]
    4. 解释: [为什么错，与西班牙语的差异点]
    5. 类似练习建议: [1-2个相关练习]
  `;

  // 调用用户选择的AI API
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3
    })
  });
  return await response.json();
}
```

方案B：导出到AI对话框
```javascript
// 生成一个预填充的prompt，用户复制到任意AI对话框
function exportToAIPrompt(questions, userAnswers) {
  const prompt = questions.map((q, i) => `
    题目${i+1}: ${q.prompt}
    我的答案: ${userAnswers[i]}
    参考答案: ${q.referenceAnswer || '(开放题)'}
  `).join('\n---\n');

  const fullPrompt = `请作为巴西葡语教师批改以下练习，逐题给出：得分、错误标注、纠正、与西班牙语差异说明。\n\n${prompt}`;
  
  // 复制到剪贴板
  navigator.clipboard.writeText(fullPrompt);
  return '已复制到剪贴板，请粘贴到AI对话框进行批改';
}
```

### 3.5 进度追踪系统

```javascript
// progress.js — localStorage 数据结构
{
  "currentWeek": 3,
  "totalStudyHours": 7.5,
  "weeklyStats": {
    "w1": { "studyTime": 3.0, "quizScore": 85, "completed": true },
    "w2": { "studyTime": 3.0, "quizScore": 78, "completed": true },
    "w3": { "studyTime": 1.5, "quizScore": null, "completed": false }
  },
  "mistakeBank": [
    {
      "week": 2,
      "question": "A menina ___ alta. (ser/estar)",
      "userAnswer": "está",
      "correctAnswer": "é",
      "topic": "ser vs estar",
      "reviewCount": 0,
      "lastReview": null,
      "mastered": false
    }
  ],
  "streak": { "current": 7, "best": 12, "lastStudy": "2026-07-20" }
}
```

错题本功能：
- 自动收集每次周考的错误
- 按"语法主题"分类
- 间隔重复（Spaced Repetition）算法提醒复习
- 掌握后标记 `mastered: true` 移出复习队列

### 3.6 学习仪表盘（index.html）

```
┌─────────────────────────────────────────────────┐
│  🇧🇷 Português Zero → B1                         │
│  Semana 3 de 16 · 连续学习 7天 🔥                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  📊 本周进度                                      │
│  ████████████░░░░  1.5h / 3.0h                   │
│                                                  │
│  📖 当前课程: W3 - 动词现在时                      │
│  [继续学习]  [开始周考]                            │
│                                                  │
│  📝 错题本: 12题待复习                             │
│  [复习错题]                                       │
│                                                  │
│  📈 成绩走势                                      │
│  W1: 85%  W2: 78%  W3: --                        │
│                                                  │
│  ⚙️ 设置  |  📊 详细统计  |  🔄 导出/导入进度       │
│                                                  │
│  AI批改: [方案A: API Key] [方案B: 导出prompt]      │
└─────────────────────────────────────────────────┘
```

---

## 四、题库设计规范

### 4.1 JSON题库格式

```json
{
  "week": 3,
  "title": "动词现在时",
  "questions": [
    {
      "id": "w3_q001",
      "type": "fill_blank",
      "difficulty": 1,
      "prompt": "Eu ___ português todos os dias. (estudar)",
      "answer": ["estudo"],
      "hint": "注意：第一人称单数 -ar → -o",
      "explanation": "estudar → estudo。与西语estudio对应，但注意葡语中主语'Eu'通常保留（PT-BR倾向不省略主语）。",
      "spanishContrast": "西语: (Yo) estudio portugués todos los días. — 葡语需保留'Eu'。"
    },
    {
      "id": "w3_q002",
      "type": "single_choice",
      "difficulty": 2,
      "prompt": "选择正确的动词形式：Nós ___ feliz hoje. (ser/estar + 正确形式)",
      "options": ["somos", "estamos", "é", "está"],
      "answer": "estamos",
      "explanation": "feliz表示临时状态用estar。Nós estamos = 我们（暂时）是。与西语'Nosotros estamos'一致。",
      "spanishContrast": "西语: Nosotros estamos felices. — 注意葡语adjective不随复数变化时仍可用单数形式（feliz不改）。"
    },
    {
      "id": "w3_q003",
      "type": "conjugation",
      "difficulty": 3,
      "prompt": "请给出动词'ter'的现在时全部变位：",
      "answer": {
        "eu": "tenho",
        "tu": "tens",
        "ele/ela": "tem",
        "nós": "temos",
        "eles/elas": "têm"
      },
      "explanation": "ter是西语tener的对应词，但变位完全不同。注意第三人称复数têm带重音符号。",
      "spanishContrast": "西语tener: tengo/tienes/tiene/tenemos/tienen — 葡语ter: tenho/tens/tem/temos/têm"
    },
    {
      "id": "w3_q004",
      "type": "translation",
      "difficulty": 3,
      "aiGraded": true,
      "prompt": "将以下句子翻译为巴西葡语：\n我有一本书和两支笔。她在家里。",
      "referenceAnswer": "Eu tenho um livro e duas canetas. Ela está em casa.",
      "scoringCriteria": "ter变位正确(2分)、冠词um/duas正确(2分)、复数canetas正确(1分)、estar+em casa正确(2分)、主语保留(1分)、拼写(2分)",
      "spanishContrast": "西语: Tengo un libro y dos bolígrafos. Ella está en casa. — 注意葡语保留主语'Eu'，'em'对应'en'。"
    }
  ]
}
```

### 4.2 每周题量标准

| 题型 | 数量 | 分值 | 批改方式 |
|---|---|---|---|
| 单选/多选 | 15题 | 30分 | 自动 |
| 填空/变位 | 10题 | 30分 | 自动 |
| 翻译（短句） | 3题 | 15分 | 自动（容错匹配） |
| 翻译（段落）/写作 | 1-2题 | 25分 | AI批改 |
| **合计** | ~30题 | 100分 | |

---

## 五、阅读材料规划

| 阶段 | 周次 | 材料类型 | 长度 | 来源 |
|---|---|---|---|---|
| 入门 | W1-4 | 短句/对话/自我介绍 | 50-150词 | 自编（针对西语者设计） |
| 基础 | W5-8 | 短篇故事/新闻 | 200-300词 | 改编自Practice Portuguese/BBC Brasil |
| 进阶 | W9-12 | 专栏/传记/文学片段 | 350-500词 | 真实素材（G1/BBC Brasil/Folha de S.Paulo） |
| B1 | W13-16 | 新闻/小说/议论文 | 400-1000词 | 真实素材原文 |

每篇阅读材料附带：
- 词汇表（标注假朋友）
- 语法点标注（本周所学）
- 3-5道阅读理解题

---

## 六、西语→葡语迁移速查表（内置工具）

程序内置一个交互式对照表，方便随时查阅：

```
┌──────────────────────────────────────────────────┐
│  🔄 西语→葡语语法速查                              │
├──────────────────────────────────────────────────┤
│                                                   │
│  [发音] [名词] [动词] [介词] [时态] [虚拟式] [假朋友]│
│                                                   │
│  ── 时态对照 ──                                    │
│  西语 pretérito indefinido  →  PT pretérito perfeito│
│  西语 pretérito imperfecto  →  PT pretérito imperfeito│
│  西语 condicional           →  PT futuro do pretérito│
│  西语 futuro simple         →  PT futuro do presente │
│  西语 presente subjuntivo   →  PT presente subjuntivo│
│  西语 imperfecto subj.      →  PT imperfeito subj.   │
│  西语 (已废弃)              →  PT futuro do subj. ★  │
│                                                   │
│  ★ = 葡语独有，西语无对应                           │
│                                                   │
│  [点击展开详细对比+例句]                            │
└──────────────────────────────────────────────────┘
```

---

## 七、GitHub部署方案

### 7.1 仓库结构

```
portugues-zero-b1/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions自动部署
├── docs/
│   └── DESIGN.md              # 本设计文档
├── index.html
├── theory/
├── exercises/
├── readings/
├── assets/
├── data/
├── README.md
└── LICENSE
```

### 7.2 部署方式

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

### 7.3 README.md

```markdown
# 🇧🇷 Português Zero → B1

为西班牙语使用者设计的巴西葡语速成程序（16周，每周3小时）。

## 特性
- 📚 16周结构化课程（CEFR A1→B1）
- 🔄 西语→葡语语法迁移对照
- 📝 每周自动考试 + AI批改
- 📊 进度追踪 + 错题本
- 🔥 学习连续性（streak）
- 📱 响应式设计（手机/电脑）

## 使用
直接访问 GitHub Pages: [链接]

## 本地运行
\`\`\`bash
python3 -m http.server 8000
# 打开 http://localhost:8000
\`\`\`

## License
MIT
```

---

## 八、实施计划

### 第一步：搭建骨架（本周）
1. 创建GitHub仓库
2. 搭建HTML/CSS/JS框架
3. 实现学习仪表盘 + 进度追踪
4. 编写W1-W4题库和阅读材料

### 第二步：Phase 1内容（第1周开发）
1. 完成W1-W4全部语法讲解页面
2. 完成自动批改引擎
3. 完成AI批改接口（方案A+B）
4. 内置西语→葡语速查表

### 第三步：Phase 2-3内容（第2-3周开发）
1. W5-W12语法讲解 + 题库
2. 阅读材料采集与标注
3. 错题本间隔重复算法

### 第四步：Phase 4 + B1模拟考（第4周开发）
1. W13-W16综合内容
2. B1模拟考试系统
3. 最终测试 + 优化

---

## 九、关键设计决策记录

| 决策 | 选择 | 理由 |
|---|---|---|
| 葡语变体 | PT-BR（巴西） | 大王指定；资源丰富；发音更清晰 |
| 目标水平 | B1 | 实用性阈值（读新闻+日常交流） |
| 周期 | 16周/3小时每周 | 西语B2可加速，常规需24周 |
| 技术栈 | 纯Vanilla JS | 无构建依赖，GitHub Pages零配置部署 |
| 数据存储 | localStorage | 纯前端，无需后端/数据库 |
| AI批改 | 方案A(用户API Key) + 方案B(导出prompt) | 兼顾有/无API Key的用户 |
| 题库格式 | JSON | 易维护、易扩展、可社区贡献 |
| 框架 | 无（Vanilla JS） | 降低维护成本，避免依赖过时 |
| 设计哲学 | 西语迁移优先 | 跳过重叠部分，聚焦差异点 |

---

🐟 鲶鱼军师 设计完毕
2026-07-21 10:25 GMT-3
