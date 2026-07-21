#!/usr/bin/env python3
"""把 readings/*.txt 转成带 charset 和样式的 HTML 页面，解决浏览器乱码。

用法: python3 tools/txt2reading.py readings/w01-short-sentences.txt \
        --title "W1 阅读 · 短句朗读练习" --back ../theory/w01-pronunciation.html
输出: 同目录同名 .html
"""
import argparse
import html
import re
from pathlib import Path

RULE = re.compile(r"^-{10,}$")
BANNER = re.compile(r"^={10,}$")


def convert(txt_path: Path, title: str, back: str) -> Path:
    lines = txt_path.read_text(encoding="utf-8").splitlines()

    # 去掉开头的 === 横幅（标题由 --title 提供）
    body = []
    skip_banner = True
    for ln in lines:
        if skip_banner and (BANNER.match(ln) or ln.strip() == "" or "阅读" in ln and skip_banner):
            if BANNER.match(ln):
                # 横幅第二行之后结束跳过
                pass
            continue
        body.append(ln)
    # 更稳妥的横幅剔除：丢弃前 4 行（=、标题、=、空）
    if len(lines) > 3 and BANNER.match(lines[0]):
        body = lines[3:]

    parts = []
    i = 0
    in_answers = False
    while i < len(body):
        ln = body[i]
        # 分节: ---- \n 标题 \n ----
        if RULE.match(ln) and i + 2 < len(body) and RULE.match(body[i + 2]):
            section = body[i + 1].strip()
            if "答案" in section or "自测" in section:
                pass
            if section.startswith("答案"):
                in_answers = True
                parts.append('<details class="answers"><summary>🔑 查看答案</summary>')
                i += 3
                continue
            parts.append(f'<h2 class="section">{html.escape(section)}</h2>')
            i += 3
            continue
        if RULE.match(ln):
            i += 1
            continue
        s = ln.rstrip()
        if s.strip() == "":
            i += 1
            continue
        esc = html.escape(s)
        if s.strip().startswith("答案") and not in_answers:
            in_answers = True
            parts.append('<details class="answers"><summary>🔑 查看答案</summary>')
            i += 1
            continue
        if s.startswith("【"):
            parts.append(f'<div class="note">{esc}</div>')
        elif re.match(r"^\s*提示", s):
            parts.append(f'<p class="hint">{esc}</p>')
        elif re.match(r"^\d+\.", s):
            # 编号句：葡语/西语部分加粗，括号中文保持常规
            parts.append(f'<p class="item">{esc}</p>')
        elif in_answers or re.match(r"^\d+\.\s", s):
            parts.append(f'<p class="answer-item">{esc}</p>')
        else:
            parts.append(f'<p class="line">{esc}</p>')
        i += 1
    if in_answers:
        parts.append("</details>")

    content = "\n      ".join(parts)
    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} · Português Zero → B1</title>
  <link rel="stylesheet" href="../assets/css/style.css">
  <style>
    .reading {{ max-width: 760px; margin: 0 auto; padding: 24px 16px 64px; }}
    .reading h1 {{ font-size: 1.5rem; margin-bottom: 4px; }}
    .reading .crumb {{ margin-bottom: 20px; font-size: .9rem; }}
    .reading .section {{ margin: 28px 0 12px; padding: 10px 14px; border-left: 4px solid #FEDD00;
      background: rgba(254,221,0,.08); border-radius: 8px; font-size: 1.05rem; }}
    .reading .note {{ background: rgba(0,151,57,.12); border: 1px solid rgba(0,151,57,.35);
      border-radius: 10px; padding: 12px 16px; margin: 12px 0; line-height: 1.7; }}
    .reading .item {{ margin: 14px 0 2px; font-size: 1.06rem; font-weight: 600; line-height: 1.8; }}
    .reading .hint {{ margin: 0 0 6px 1.2em; opacity: .75; font-size: .92rem; line-height: 1.6; }}
    .reading .line {{ margin: 6px 0; line-height: 1.8; }}
    .reading .answers {{ margin-top: 28px; border: 1px solid rgba(255,255,255,.15);
      border-radius: 10px; padding: 12px 16px; }}
    .reading .answers summary {{ cursor: pointer; font-weight: 600; }}
    .reading .answer-item {{ margin: 6px 0 6px 1em; line-height: 1.7; }}
  </style>
</head>
<body>
  <main class="reading">
    <p class="crumb"><a href="../index.html">🏠 仪表盘</a> · <a href="{html.escape(back)}">← 返回本周课程</a></p>
    <h1>📖 {html.escape(title)}</h1>
    {content}
  </main>
</body>
</html>
"""
    out = txt_path.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("txt", type=Path)
    ap.add_argument("--title", required=True)
    ap.add_argument("--back", required=True)
    a = ap.parse_args()
    print(convert(a.txt, a.title, a.back))
