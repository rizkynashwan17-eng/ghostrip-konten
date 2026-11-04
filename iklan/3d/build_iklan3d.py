"""Iklan fitur Ghostrip gaya 3D startup tech (sekali pakai, di luar jadwal harian).

Pakai: python3 iklan/3d/build_iklan3d.py [--tanpa-suara]
Butuh suara di voice/out/iklan-3d-fitur/NN.wav (dibuat workflow voice.yml dari voice/requests/iklan-3d-fitur.json).
Hasil: iklan/3d/Ghostrip_Iklan_Fitur_3D.mp4 (1080x1920, 30 fps, -14 LUFS).
"""
import json, os, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RM = os.path.join(ROOT, "remotion"); HERE = os.path.dirname(os.path.abspath(__file__))
VID = "iklan-3d-fitur"; FPS = 30; SR = 44100
KEYS = ["hook", "logo", "hitung", "surat", "wa", "muat", "semua", "akun", "cta"]
SUBS = ["Hitung harga trip masih pakai kalkulator, Excel, lalu ketik ulang?", "",
        "Rute, solar, tol, dan hari jalan langsung dihitung otomatis.",
        "Sekali ketuk, jadi surat penawaran PDF lengkap dengan kop, tanda tangan, dan cap.",
        "Kirim langsung ke WhatsApp customer.",
        "Cek muatan 3D: lihat barang muat atau tidak, sebelum truk berangkat.",
        "Data truk, masa berlaku STNK dan KIR, sampai berita logistik, semua di satu aplikasi.",
        "Riwayat tersimpan di akun, aman walaupun ganti HP.", ""]
MIN = [2.8, 1.9, 2.6, 3.4, 2.0, 3.2, 3.6, 2.4, 3.6]


def baca(path):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
    if sr != SR:
        n = int(len(x) * SR / sr); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    # buang hening awal/akhir
    e = np.abs(x) > 0.02
    if e.any():
        i0, i1 = np.argmax(e), len(x) - np.argmax(e[::-1])
        x = x[max(0, i0 - int(0.03 * SR)):min(len(x), i1 + int(0.08 * SR))]
    return padat(x)


def padat(x, jeda_maks=0.22):
    """Padatkan jeda di dalam kalimat yang lebih panjang dari jeda_maks."""
    hop = int(SR * 0.02)
    e = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    if not len(e): return x
    thr = 0.08 * np.percentile(e, 95)
    keep = np.ones(len(x), bool); run = 0; mf = int(jeda_maks / 0.02)
    for i, v in enumerate(list(e < thr) + [False]):
        if v: run += 1
        else:
            if run > mf: keep[(i - run + mf // 2) * hop:(i - mf // 2) * hop] = False
            run = 0
    return x[keep]


def tulis(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "w") as w:
        w.setnchannels(2 if x.ndim == 2 else 1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def tempo(x, f):
    if abs(f - 1) < 0.01: return x
    a, b = "/tmp/_t_in.wav", "/tmp/_t_out.wav"; tulis(a, x)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", f"atempo={f:.3f}", "-ar", str(SR), "-ac", "1", b], check=True)
    return baca(b)


# ---------- musik tech orisinal (120 bpm, A minor) ----------
def env(n, a=0.005, d=0.2):
    k = np.arange(n) / SR
    return np.minimum(1, k / a) * np.exp(-k / d)


def musik(dur, hits):
    n = int(dur * SR); out = np.zeros((n, 2)); bpm = 120; beat = 60 / bpm
    t = np.arange(n) / SR
    # pad lebar
    prog = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (196.0, 246.94, 293.66), (164.81, 207.65, 246.94)]
    bar = beat * 4
    for i, ch in enumerate(prog * 20):
        s0 = i * bar
        if s0 >= dur: break
        i0, i1 = int(s0 * SR), min(n, int((s0 + bar) * SR))
        k = t[i0:i1] - s0
        g = np.minimum(1, k / 0.4) * np.minimum(1, (bar - k) / 0.3)
        for fz in ch:
            out[i0:i1, 0] += 0.05 * g * np.sin(2 * np.pi * fz * k + 0.3)
            out[i0:i1, 1] += 0.05 * g * np.sin(2 * np.pi * fz * 1.004 * k)
        # sub bass 8th
        for j in range(8):
            b0 = s0 + j * beat / 2; ii = int(b0 * SR); m = int(0.2 * SR)
            if ii + m > n: break
            kk = np.arange(m) / SR
            out[ii:ii + m] += (0.16 * np.sin(2 * np.pi * ch[0] / 4 * kk) * env(m, 0.004, 0.12))[:, None]
        # arpeggio pluck 16th
        arp = [ch[0] * 2, ch[1] * 2, ch[2] * 2, ch[1] * 2]
        for j in range(16):
            b0 = s0 + j * beat / 4; ii = int(b0 * SR); m = int(0.16 * SR)
            if ii + m > n: break
            kk = np.arange(m) / SR; fz = arp[j % 4]
            v = 0.05 * (np.sign(np.sin(2 * np.pi * fz * kk)) * 0.4 + np.sin(2 * np.pi * fz * kk)) * env(m, 0.002, 0.05)
            pan = 0.5 + 0.35 * np.sin(j)
            out[ii:ii + m, 0] += v * (1 - pan); out[ii:ii + m, 1] += v * pan
    # drum
    rs = np.random.RandomState(3)
    for j in range(int(dur / beat) + 1):
        b0 = j * beat; ii = int(b0 * SR); m = int(0.3 * SR)
        if ii + m > n: break
        kk = np.arange(m) / SR
        kick = 0.55 * np.sin(2 * np.pi * (50 + 110 * np.exp(-kk * 30)) * kk) * env(m, 0.001, 0.14)
        if b0 > 2.0: out[ii:ii + m] += kick[:, None]
        h = int((b0 + beat / 2) * SR); mh = int(0.05 * SR)
        if h + mh < n and b0 > 1.0:
            hat = 0.06 * rs.randn(mh) * env(mh, 0.0005, 0.012); hat = np.diff(hat, prepend=0)
            out[h:h + mh] += hat[:, None]
        if j % 2 == 1 and b0 > 4.0:
            ms = int(0.18 * SR); sn = 0.12 * rs.randn(ms) * env(ms, 0.001, 0.05)
            out[ii:ii + ms] += sn[:, None]
    # riser sebelum tiap hit + impact
    for hsec, big in hits:
        L = 0.9 if big else 0.45; i1 = int(hsec * SR); i0 = max(0, i1 - int(L * SR))
        m = i1 - i0
        if m > 0:
            kk = np.arange(m) / SR; nz = rs.randn(m)
            sw = np.convolve(nz, np.ones(8) / 8, "same") * (kk / L) ** 2 * (0.22 if big else 0.12)
            out[i0:i1, 0] += sw; out[i0:i1, 1] += np.roll(sw, 40)
        if big:
            m = int(1.2 * SR); kk = np.arange(m) / SR
            if i1 + m < n:
                imp = 0.6 * np.sin(2 * np.pi * (40 + 60 * np.exp(-kk * 12)) * kk) * env(m, 0.002, 0.5)
                out[i1:i1 + m] += imp[:, None]
    fade = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 1.2)
    out *= fade[:, None]
    return out / (np.abs(out).max() + 1e-9) * 0.7


def main():
    tanpa = "--tanpa-suara" in sys.argv
    vdir = os.path.join(ROOT, "voice", "out", VID)
    if not tanpa and not os.path.exists(os.path.join(vdir, "done.json")):
        sys.exit("suara belum ada")
    lines = [] if tanpa else [baca(os.path.join(vdir, f"{i:02d}.wav")) for i in range(len(KEYS))]
    raw = sum(len(x) for x in lines) / SR if lines else 0
    tot_est = raw + 0.3 * len(KEYS) + 1.5
    f = min(1.18, max(1.0, tot_est / 38.0)) if lines else 1
    if lines and f > 1.01:
        lines = [tempo(x, f) for x in lines]
    print(f"narasi mentah {raw:.1f} dtk, tempo {f:.2f}x")
    scenes, starts, t = [], [], 0.0
    for i, k in enumerate(KEYS):
        ld = len(lines[i]) / SR if lines else MIN[i] - 0.6
        d = max(MIN[i] if not lines else 1.6, ld + (0.3 if i < len(KEYS) - 1 else 1.8)) + (0.2 if i == 0 else 0)
        if lines and k == "logo": d = max(d, 2.0)
        fr0 = round(t * FPS); fr1 = round((t + d) * FPS)
        scenes.append({"key": k, "from": fr0, "dur": fr1 - fr0, "sub": SUBS[i]})
        starts.append(t + (0.2 if i == 0 else 0.12)); t += d
    total = scenes[-1]["from"] + scenes[-1]["dur"]
    print("durasi", round(total / FPS, 2), "dtk")
    run = os.path.join(RM, "public", "run"); os.makedirs(run, exist_ok=True)
    pf = os.path.join(run, "iklan3d.json"); json.dump({"scenes": scenes, "durationInFrames": total}, open(pf, "w"))
    vraw = os.path.join(RM, "out", "iklan3d_raw.mp4"); os.makedirs(os.path.dirname(vraw), exist_ok=True)
    ch = subprocess.check_output(["node", "-e", "console.log(require('playwright').chromium.executablePath())"], text=True).strip()
    subprocess.run(["npx", "remotion", "render", "src/index.ts", "Iklan3D", vraw, f"--props={pf}", "--log=error", f"--browser-executable={ch}",
                    "--codec=h264", "--crf=18", "--muted"], cwd=RM, check=True)
    # audio
    dur = total / FPS
    hits = [(sc["from"] / FPS, sc["key"] in ("logo", "cta")) for sc in scenes[1:]]
    mus = musik(dur + 0.2, hits)
    nar = np.zeros(len(mus))
    for i, x in enumerate(lines):
        i0 = int(starts[i] * SR); i1 = min(len(nar), i0 + len(x)); nar[i0:i1] += x[:i1 - i0]
    if lines:
        nar = nar / (np.abs(nar).max() + 1e-9) * 0.9
        envl = np.convolve(np.abs(nar), np.ones(int(0.15 * SR)) / int(0.15 * SR), "same")
        duck = 1 - 0.55 * np.clip(envl / 0.08, 0, 1)
        mix = mus * (duck[:, None] * 0.75) + nar[:, None]
    else:
        mix = mus
    aw = os.path.join(run, "iklan3d_mix.wav"); tulis(aw, mix / (np.abs(mix).max() + 1e-9) * 0.95)
    out = os.path.join(HERE, "Ghostrip_Iklan_Fitur_3D.mp4"); tmp = out[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vraw, "-i", aw, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "8", "-i", out, "-frames:v", "1", "-q:v", "3", os.path.join(HERE, "cover.jpg")], check=True)
    print("OK", out)


if __name__ == "__main__":
    main()
