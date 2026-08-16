#!/usr/bin/env python3
"""批量预生成 PT-BR 神经语音（edge-tts）音频。

输出：
  assets/audio/words/w{week}_{rank}_{safe}.mp3   —— 800 个单词
  assets/audio/examples/w{week}_{rank}_{safe}.mp3 —— 800 条例句（example.pt）
  assets/audio/conj/{safe_verb}_{person}.mp3     —— 每个动词 5 人称变位

可重复运行：已存在的文件自动跳过（断点续跑）。
依赖：/usr/bin/python3 -m pip install --user edge-tts
用法：/usr/bin/python3 tools/generate_audio.py [--limit N] [--concurrency N]
"""
import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "frequency-vocab.json"
OUT_WORDS = ROOT / "assets" / "audio" / "words"
OUT_EXAMPLES = ROOT / "assets" / "audio" / "examples"
OUT_CONJ = ROOT / "assets" / "audio" / "conj"
VOICE = "pt-BR-FranciscaNeural"
RATE = "-8%"  # 接近真人语速，略慢一点便于学习

PERSONS = [("eu", "eu"), ("tu", "tu"), ("ele/ela/você", "ele"),
           ("nós", "nos"), ("eles/elas/vocês", "eles")]


def safe(s: str) -> str:
    """与前端 assets/js/tts.js 的 safeName() 保持一致。"""
    s = re.sub(r"\s+", "_", s.strip().lower())
    return re.sub(r"[^a-z0-9à-ÿ_\-]", "", s)


def collect_jobs():
    data = json.loads(VOCAB.read_text(encoding="utf-8"))
    jobs = []  # (text, path)
    seen_conj = set()
    n_words = n_verbs = 0
    for w in range(1, 17):
        for e in data.get(f"w{w}", []):
            pt = e["pt"]
            sw = safe(pt)
            if not sw:
                continue
            jobs.append((pt, OUT_WORDS / f"w{w}_{e['rank']}_{sw}.mp3"))
            n_words += 1
            example = (e.get("example") or {}).get("pt")
            if example:
                jobs.append((example, OUT_EXAMPLES / f"w{w}_{e['rank']}_{sw}.mp3"))
            conj = e.get("conjugations")
            if conj:
                n_verbs += 1
                for jkey, pkey in PERSONS:
                    form = conj.get(jkey)
                    if not form:
                        continue
                    name = f"{sw}_{pkey}.mp3"
                    if name in seen_conj:
                        print(f"⚠️ 变位文件名冲突：{name}（{pt}）", file=sys.stderr)
                        continue
                    seen_conj.add(name)
                    jobs.append((form, OUT_CONJ / name))
    return jobs, n_words, n_verbs


async def gen_one(sem, text, path):
    if path.exists() and path.stat().st_size > 0:
        return "skip"
    async with sem:
        try:
            import edge_tts
            comm = edge_tts.Communicate(text, VOICE, rate=RATE)
            await comm.save(str(path))
            return "ok"
        except Exception as ex:  # noqa: BLE001
            print(f"✗ {path.name}: {ex}", file=sys.stderr)
            try:
                path.unlink(missing_ok=True)
            except Exception:
                pass
            return "fail"


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="本轮最多新生成 N 个（0=不限）")
    ap.add_argument("--concurrency", type=int, default=12)
    args = ap.parse_args()

    OUT_WORDS.mkdir(parents=True, exist_ok=True)
    OUT_EXAMPLES.mkdir(parents=True, exist_ok=True)
    OUT_CONJ.mkdir(parents=True, exist_ok=True)

    jobs, n_words, n_verbs = collect_jobs()
    todo = [(t, p) for t, p in jobs if not (p.exists() and p.stat().st_size > 0)]
    print(f"词条 {n_words} · 动词 {n_verbs} · 任务总数 {len(jobs)} · 待生成 {len(todo)}")
    if args.limit:
        todo = todo[: args.limit]

    sem = asyncio.Semaphore(args.concurrency)
    results = await asyncio.gather(*(gen_one(sem, t, p) for t, p in todo))
    ok = results.count("ok")
    fail = results.count("fail")
    print(f"本轮：新生成 {ok} · 失败 {fail} · 剩余 {len(jobs) - len([1 for _, p in jobs if p.exists()])}")


if __name__ == "__main__":
    asyncio.run(main())
