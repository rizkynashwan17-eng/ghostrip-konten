"""Cek kualitas Reels sebelum tayang (dipakai untuk /updatekonten).

Pakai: python3 engine/cek_konten.py <video.mp4> [voice_id] [jumlah_baris_dialog]
Keluaran JSON per video:
- durasi, puncak audio (dBFS), persen sampel terpotong (clipping), jumlah "klik/kresek" (lonjakan mendadak)
- voiceover: ada/tidak + jumlah file suara vs jumlah dialog
- intonasi: rentang nada (semitone) per baris suara; < 4.0 = cenderung datar (bicara natural biasanya 5–12)
Status: AMAN jika ada voiceover lengkap, clipping < 0.05%, klik <= 3, dan intonasi tidak datar.
"""
import json, os, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def audio_of(mp4, sr=44100):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768, sr

def clicks(x, sr):
    # lonjakan sampel ke sampel yang jauh di atas kebiasaan sinyal sekitarnya
    d = np.abs(np.diff(x))
    if len(d) == 0: return 0
    win = int(sr * .01); env = np.convolve(d, np.ones(win) / win, "same") + 1e-4
    spikes = np.where((d > .25) & (d > 12 * env))[0]
    if len(spikes) == 0: return 0
    return int(1 + np.sum(np.diff(spikes) > sr * .05))

def f0_track(x, sr):
    fr = int(sr * .04); hop = int(sr * .02); out = []
    for i in range(0, len(x) - fr, hop):
        s = x[i:i + fr] - x[i:i + fr].mean()
        if np.sqrt((s ** 2).mean()) < .02: continue
        ac = np.correlate(s, s, "full")[fr - 1:]
        lo, hi = int(sr / 400), int(sr / 70)
        if hi >= len(ac): continue
        k = lo + np.argmax(ac[lo:hi])
        if ac[k] > .35 * ac[0]: out.append(sr / k)
    return np.array(out)

def intonation(wav):
    with wave.open(wav) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    f = f0_track(x, sr)
    if len(f) < 8: return None
    st = 12 * np.log2(f / np.median(f))
    st = st[np.abs(st) < 9]                      # buang loncatan oktaf (salah deteksi)
    if len(st) < 8: return None
    st = np.convolve(st, np.ones(3) / 3, "valid")  # haluskan
    return round(float(np.percentile(st, 90) - np.percentile(st, 10)), 1)

def check(mp4, voice_id=None, n_lines=None):
    r = {"video": os.path.relpath(mp4, ROOT)}
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]))
    x, sr = audio_of(mp4); r["durasi_dtk"] = round(dur, 1)
    peak = np.abs(x).max() if len(x) else 0
    r["puncak_dbfs"] = round(20 * np.log10(max(peak, 1e-6)), 1)
    r["clipping_persen"] = round(100 * float(np.mean(np.abs(x) > .995)) if len(x) else 0, 3)
    r["klik_kresek"] = clicks(x, sr)
    issues = []
    if r["clipping_persen"] >= .05: issues.append("suara pecah (clipping)")
    if r["klik_kresek"] > 3: issues.append(f"{r['klik_kresek']} bunyi klik/kresek")
    if voice_id:
        d = os.path.join(ROOT, "voice", "out", voice_id)
        wavs = sorted(f for f in os.listdir(d) if f.endswith(".wav")) if os.path.isdir(d) else []
        done = os.path.exists(os.path.join(d, "done.json"))
        r["voiceover"] = f"{len(wavs)}/{n_lines or '?'} baris" + ("" if done else " (belum lengkap)")
        if not done or (n_lines and len(wavs) < n_lines): issues.append("voiceover belum lengkap")
        ints = [intonation(os.path.join(d, w)) for w in wavs]
        r["intonasi_semitone"] = ints
        flat = [i for i, v in enumerate(ints) if v is not None and v < 4.0]
        if flat: issues.append(f"intonasi datar di baris {', '.join(str(i + 1) for i in flat)}")
    else:
        r["voiceover"] = "tidak dicek (tanpa voice_id)"
    r["masalah"] = issues
    r["status"] = "AMAN" if not issues else "PERLU DICEK"
    return r

if __name__ == "__main__":
    a = sys.argv[1:]
    print(json.dumps(check(a[0], a[1] if len(a) > 1 else None, int(a[2]) if len(a) > 2 else None), ensure_ascii=False, indent=1))
