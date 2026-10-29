"""Video gaya "Gimana kalau…" (Remotion) untuk Ghostrip.

Pakai:
  python3 engine/whatif.py suara  konten/YYYY-MM-DD-whatif.json   → tulis voice/requests/<voice_id>.json (SATU request narasi per video)
  python3 engine/whatif.py render konten/YYYY-MM-DD-whatif.json   → render semua post engine "remotion" ke media/<tanggal>/<slot>.mp4
        [--tanpa-suara]  render tanpa narasi (timing diperkirakan), hanya untuk pratinjau — JANGAN masuk halaman posting

Format post (kind "reel", engine "remotion"):
{"slot": "reel1-whatif", "kind": "reel", "engine": "remotion", "time": "11:30",
 "judul": "TRUK DITAHAN DI JEMBATAN TIMBANG", "part": 1, "lokasi": "02.14 WIB · JALINTIM SUMATERA", "jam": "02:14",
 "topic": "...", "caption": "...", "tiktok_title": "...",
 "scenes": [{"type": "jalan", "narasi": "Jam dua pagi, truk Pak Darto masuk *jembatan timbang*.", ...parameter adegan}, ...]}
Satu adegan = satu kalimat narasi. Kata di dalam *bintang* jadi kata kunci oranye di teks layar.
Jenis adegan (lihat remotion/src/scenes.tsx): jalan, dokumen, timbangan, stat, aturan, karakter, peta, struk, angka, cta.
"""
import glob, json, math, os, re, shutil, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RM = os.path.join(ROOT, "remotion")
FPS = 30
SR = 44100


def plain(t):
    return re.sub(r"\*", "", t).strip()


def voice_id(date, post):
    return post.get("voice_id") or f"{date}-{post['slot']}"


def cmd_suara(spec_path):
    spec = json.load(open(spec_path))
    for post in spec["posts"]:
        if post.get("engine") != "remotion":
            continue
        vid = voice_id(spec["date"], post); post["voice_id"] = vid
        text = "\n".join(plain(s["narasi"]) for s in post["scenes"])
        req = {"id": vid, "mode": "narasi", "rev": 1,
               "jadwal": f"{spec['date']}T{post.get('time', '23:59')}",
               "lines": [{"who": "NARATOR", "tone": "narasi", "text": text}]}
        p = os.path.join(ROOT, "voice", "requests", f"{vid}.json")
        if os.path.exists(p):
            req["rev"] = json.load(open(p)).get("rev", 0) + 1
        json.dump(req, open(p, "w"), ensure_ascii=False, indent=1)
        print("request suara:", os.path.relpath(p, ROOT))
    json.dump(spec, open(spec_path, "w"), ensure_ascii=False, indent=1)


# ---------- audio: musik tegang orisinal + whoosh ----------
def musik(dur, path):
    t = np.arange(int(dur * SR)) / SR
    pad = np.zeros_like(t)
    for f0, a in [(110.0, 0.32), (130.81, 0.22), (164.81, 0.18), (55.0, 0.30)]:
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t + f0)
        pad += a * lfo * (np.sin(2 * np.pi * f0 * t) + 0.35 * np.sin(2 * np.pi * f0 * 1.003 * t))
    beat = np.zeros_like(t)
    for st in np.arange(0.4, dur, 0.857):  # denyut pelan ±70 bpm
        n = int(0.35 * SR); i = int(st * SR)
        if i + n > len(t): break
        k = np.arange(n) / SR
        beat[i:i + n] += 0.9 * np.sin(2 * np.pi * (60 - 30 * k) * k) * np.exp(-k * 9)
    tick = np.zeros_like(t)
    for st in np.arange(0.2, dur, 0.4285):  # detik jam
        n = int(0.02 * SR); i = int(st * SR)
        if i + n > len(t): break
        tick[i:i + n] += 0.12 * np.random.RandomState(int(st * 100)).randn(n) * np.exp(-np.arange(n) / (0.004 * SR))
    x = 0.5 * pad + beat + tick
    fade = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.2)
    x = x * fade
    x = x / (np.abs(x).max() + 1e-9) * 0.6
    tulis_wav(path, x)


def whoosh(path):
    n = int(0.45 * SR); k = np.arange(n) / SR
    noise = np.random.RandomState(7).randn(n)
    env = np.sin(np.pi * k / 0.45) ** 2
    # filter sapuan sederhana: rata-rata bergerak dengan lebar menurun
    out = np.zeros(n); acc = 0.0
    for i in range(n):
        a = 0.02 + 0.25 * (i / n)
        acc = acc + a * (noise[i] - acc); out[i] = acc
    x = out * env; x = x / (np.abs(x).max() + 1e-9) * 0.5
    tulis_wav(path, x)


def tulis_wav(path, x, sr=SR):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def baca_wav(path):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    return x, sr


# ---------- timing kalimat dari jeda di rekaman narasi ----------
def timing_dari_suara(path, sentences):
    x, sr = baca_wav(path)
    hop = int(sr * 0.02)
    e = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    thr = 0.08 * np.percentile(e, 95)
    voiced = e > thr
    idx = np.where(voiced)[0]
    s0, s1 = idx[0] * 0.02, (idx[-1] + 1) * 0.02
    # kumpulkan jeda >= 0.14 dtk
    gaps = []; run = 0
    for i, v in enumerate(voiced):
        if not v: run += 1
        else:
            if run * 0.02 >= 0.14: gaps.append(((i - run / 2) * 0.02, run * 0.02))
            run = 0
    w = np.array([max(4, len(s)) for s in sentences], float); cum = np.cumsum(w) / w.sum()
    bounds = [s0]; used = set()
    for k in range(len(sentences) - 1):
        target = s0 + cum[k] * (s1 - s0)
        cand = [(abs(c - target) - 0.15 * min(d, 1.0), j, c) for j, (c, d) in enumerate(gaps) if j not in used and c > bounds[-1] + 0.5 and abs(c - target) < 1.6]
        if cand:
            _, j, c = min(cand); used.add(j); bounds.append(c)
        else:
            bounds.append(max(target, bounds[-1] + 0.6))
    bounds.append(s1)
    return [(bounds[i], bounds[i + 1]) for i in range(len(sentences))], len(x) / sr


def timing_perkiraan(sentences):
    t = 0.3; out = []
    for s in sentences:
        d = max(1.3, len(s) / 13.5); out.append((t, t + d)); t += d + 0.25
    return out, t


def potong_frasa(text, maks=3):
    """Pecah kalimat jadi frasa 2-3 kata; *kata kunci* tidak dipotong."""
    toks = re.findall(r"\*[^*]+\*[.,!?…]*|\S+", text)
    chunks, cur, n = [], [], 0
    for tk in toks:
        k = len(tk.strip("*").split())
        if cur and (n + k > maks):
            chunks.append(" ".join(cur)); cur, n = [], 0
        cur.append(tk); n += k
        if re.search(r"[.,!?…]$", tk.strip("*")) and n >= 2:
            chunks.append(" ".join(cur)); cur, n = [], 0
    if cur:
        if chunks and n == 1 and len(chunks[-1].split()) < 4: chunks[-1] += " " + cur[0]
        else: chunks.append(" ".join(cur))
    return chunks


def chromium():
    for p in sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome")) + sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome"))):
        if os.path.exists(p): return p
    try:
        return subprocess.check_output(["node", "-e", "console.log(require('playwright').chromium.executablePath())"], text=True).strip()
    except Exception:
        return None


def cmd_render(spec_path, tanpa_suara=False):
    spec = json.load(open(spec_path)); date = spec["date"]
    if not os.path.isdir(os.path.join(RM, "node_modules")):
        subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund"], cwd=RM, check=True)
    run = os.path.join(RM, "public", "run"); os.makedirs(run, exist_ok=True)
    outdir = os.path.join(ROOT, "media", date); os.makedirs(outdir, exist_ok=True)
    man_path = os.path.join(outdir, "manifest.json")
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else []
    for post in spec["posts"]:
        if post.get("engine") != "remotion":
            continue
        vid = voice_id(date, post)
        sentences = [plain(s["narasi"]) for s in post["scenes"]]
        wav = os.path.join(ROOT, "voice", "out", vid, "00.wav")
        voiced = (not tanpa_suara) and os.path.exists(wav) and os.path.exists(os.path.join(ROOT, "voice", "out", vid, "done.json"))
        if voiced:
            times, total = timing_dari_suara(wav, sentences)
            shutil.copy(wav, os.path.join(run, f"{vid}.wav"))
        else:
            if not tanpa_suara:
                sys.exit(f"{vid}: narasi belum ada (jalankan 'suara' dan tunggu workflow), atau pakai --tanpa-suara untuk pratinjau")
            times, total = timing_perkiraan(sentences)
        off = 6 / FPS  # narasi mulai di frame 6
        scenes = []
        for i, sc in enumerate(post["scenes"]):
            a = 0 if i == 0 else times[i][0] + off - 0.08
            b = (times[i + 1][0] + off - 0.08) if i + 1 < len(times) else times[i][1] + off + 1.8
            f0, f1 = round(a * FPS), round(b * FPS)
            spk0, spk1 = (times[i][0] + off) * FPS - f0, (times[i][1] + off) * FPS - f0
            chunks = potong_frasa(sc["narasi"])
            wts = np.array([max(3, len(plain(c))) for c in chunks], float); cum = np.concatenate([[0], np.cumsum(wts) / wts.sum()])
            ch = []
            for j, c in enumerate(chunks):
                c0 = round(spk0 + cum[j] * (spk1 - spk0)); c1 = round(spk0 + cum[j + 1] * (spk1 - spk0))
                if j == len(chunks) - 1: c1 = f1 - f0
                ch.append({"text": c.upper().replace("*", "*"), "from": max(0, c0), "to": max(c0 + 8, c1)})
            d = dict(sc); d.update({"from": f0, "dur": max(24, f1 - f0), "chunks": ch})
            scenes.append(d)
        dur_frames = scenes[-1]["from"] + scenes[-1]["dur"]
        musik(dur_frames / FPS + 0.5, os.path.join(run, "musik.wav")); whoosh(os.path.join(run, "whoosh.wav"))
        props = {"judul": post["judul"], "part": post.get("part", 1), "lokasi": post["lokasi"], "jam": post.get("jam"),
                 "handle": "@ghostrip.app", "durationInFrames": dur_frames, "scenes": scenes,
                 "narasi": f"run/{vid}.wav" if voiced else None, "musik": "run/musik.wav", "whoosh": "run/whoosh.wav"}
        pf = os.path.join(run, "props.json"); json.dump(props, open(pf, "w"), ensure_ascii=False)
        raw = os.path.join(RM, "out", f"{vid}.mp4"); os.makedirs(os.path.dirname(raw), exist_ok=True)
        cmdl = ["npx", "remotion", "render", "src/index.ts", "WhatIf", raw, f"--props={pf}", "--log=error"]
        ch_path = chromium()
        if ch_path: cmdl.append(f"--browser-executable={ch_path}")
        subprocess.run(cmdl, cwd=RM, check=True)
        out = os.path.join(outdir, f"{post['slot']}.mp4")
        # normalisasi loudness -14 LUFS, H.264 veryfast
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", out], check=True)
        cover = os.path.join(outdir, f"{post['slot']}-cover.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.2", "-i", out, "-frames:v", "1", "-q:v", "3", cover], check=True)
        rel = lambda p: os.path.relpath(p, ROOT)
        manifest = [m for m in manifest if m["slot"] != post["slot"]] + [{"slot": post["slot"], "kind": "reel", "media": rel(out), "cover": rel(cover), "dur": round(dur_frames / FPS, 2), "engine": "remotion", "bersuara": voiced}]
        json.dump(manifest, open(man_path, "w"), indent=1)
        print("OK", rel(out), f"{dur_frames / FPS:.1f} dtk", "bersuara" if voiced else "TANPA SUARA (pratinjau)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("suara", "render"):
        print(__doc__); sys.exit(1)
    if a[0] == "suara": cmd_suara(a[1])
    else: cmd_render(a[1], "--tanpa-suara" in a)
