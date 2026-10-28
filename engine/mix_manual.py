"""Tambah vokal (voice/out/<id>/NN.wav) ke video manual yang sudah jadi.

Pakai: python3 engine/mix_manual.py <video_in.mp4> <voice_id> <video_out.mp4> "0.2,3.6,8.1,12.6,17.6,20.6" "3.5,8.0,12.5,17.0,20.5,24.5"
Baris ke-i diletakkan di start[i]; kalau lebih panjang dari jendela (end[i]-start[i]) dipercepat maks 1.3x.
"""
import os, subprocess, sys, wave, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vin, vid, vout, st, en = sys.argv[1:6]
st = [float(x) for x in st.split(",")]; en = [float(x) for x in en.split(",")]
d = os.path.join(ROOT, "voice", "out", vid); SR = 44100
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vin]))
track = np.zeros(int((dur + 1) * SR))
for i, (a, b) in enumerate(zip(st, en)):
    fn = os.path.join(d, f"{i:02d}.wav")
    if not os.path.exists(fn): continue
    with wave.open(fn) as w: sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    nz = np.where(np.abs(x) > .01)[0]
    if len(nz): x = x[max(0, nz[0] - 400): nz[-1] + 800]
    L = len(x) / sr; win = b - a - .15
    speed = min(1.3, max(1.0, L / win)) if win > 0 else 1.0
    n2 = int(len(x) * SR / sr / speed); x = np.interp(np.linspace(0, len(x) - 1, n2), np.arange(len(x)), x)
    x = x * (.9 / max(.05, np.abs(x).max())); s0 = int(a * SR); e0 = min(len(track), s0 + len(x)); track[s0:e0] += x[:e0 - s0]
    print(i, f"{L:.2f}s speed {speed:.2f}")
tmp = vout + ".vo.wav"
pcm = (np.clip(track, -1, 1) * 32000).astype(np.int16)
with wave.open(tmp, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", vin, "-i", tmp, "-filter_complex",
    "[0:a]volume=0.55[a0];[a0][1:a]amix=inputs=2:duration=first:normalize=0[a]", "-map", "0:v", "-map", "[a]",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", vout])
os.remove(tmp)
