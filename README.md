# 🇧🇷 Português Zero → B1

为西班牙语 B2 使用者设计的巴西葡语（PT-BR）速成程序：**16 周，每周 3 小时，目标 CEFR B1**。

## 特性

- 📚 16 周结构化课程（CEFR A1→B1），西语→葡语迁移优先
- 🔄 内置西语→葡语语法/发音/词汇对照（含假朋友预警）
- 📝 每周自动考试（8 种题型自动批改）+ AI 批改（自带 API Key 或导出 prompt）
- 📊 学习仪表盘：进度追踪、连续天数 streak、成绩走势
- 📖 错题本：自动收集错题，支持标记掌握
- 📱 响应式设计（手机/电脑），纯 Vanilla JS 无构建依赖

## 使用

直接访问 GitHub Pages：`https://caobenjamin196-lang.github.io/portugues-zero-b1/`

学习数据（进度、错题、API Key）全部存储在浏览器 localStorage，不离开本机。

## 本地运行

```bash
python3 -m http.server 8000
# 打开 http://localhost:8000
```

## 项目结构

```
├── index.html          # 学习仪表盘
├── quiz.html           # 测验运行页
├── theory/             # 16 周理论讲解（W1-W4 完整，W5-W16 陆续上线）
├── exercises/          # 每周题库 JSON（W1-W4 完整）
├── readings/           # 阅读材料（W1-W4）
├── assets/css|js       # 样式与逻辑（quiz-engine / ai-grader / progress / data / app）
├── data/               # 课程大纲、词汇表、动词变位表
└── docs/DESIGN.md      # 完整设计文档
```

## License

MIT
