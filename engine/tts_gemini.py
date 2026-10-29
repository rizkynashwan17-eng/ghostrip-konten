"""Dijalankan di GitHub Actions: baca voice/requests/*.json, buat file suara di voice/out/<id>/NN.wav.

Format request: {"id": "2026-10-28-reel2", "lines": [{"who": "BOS", "text": "..."}, ...]}
Hanya request yang belum punya voice/out/<id>/done.json yang diproses.
Hasil: voice/out/<id>/00.wav, 01.wav, ... (mono 24 kHz) + done.json berisi durasi + model tiap baris.
Aturan kualitas (29 Okt 2026, setelah Rizky menemukan voiceover rusak):
- SATU MODEL untuk semua baris dalam satu video. Kalau baris berikutnya terpaksa pindah model, semua baris dibuat ulang dengan model itu.
- Baris ditolak kalau terlalu panjang (model membaca instruksi), terlalu pendek (terpotong), atau banyak sampel pecah (clipping).
- Semua baris dinormalkan ke puncak -3 dBFS supaya tidak pecah di video.
"""
import base64, json, os, sys, time, urllib.request, urllib.error, wave, glob

KEY = os.environ.get("GEMINI_API_KEY", "").strip()
API = "https://generativelanguage.googleapis.com/v1beta"
MODELS = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts", "gemini-2.5-flash-tts"]
VOICE = {"NARATOR": "Charon", "BOS": "Algenib", "SOPIR": "Puck", "HANTU": "Leda", "ADMIN": "Kore", "CUSTOMER": "Charon"}
PERSONA = {
    "NARATOR": "a cinematic Indonesian storyteller narrating a suspenseful 'what if' short video about the trucking business, calm, warm and slightly low voice, clear diction, a short dramatic pause after every sentence",
    "BOS": "a middle-aged Indonesian trucking company boss, deep and slightly gravelly voice, relaxed but authoritative, like a friendly 'Pak Bos' chatting with his staff",
    "SOPIR": "an Indonesian truck driver in his 30s, warm, casual and a bit cheeky, chatting with his boss",
    "HANTU": "a small cute friendly ghost mascot, bright, playful and cheerful",
    "ADMIN": "a polite young Indonesian office admin",
    "CUSTOMER": "an Indonesian customer who is in a hurry",
}
TONE = {
    "narasi": "suspenseful storytelling with natural rises and falls, slower on key numbers, short pause between sentences",
    "penasaran": "curious, questioning (rising intonation at the end)",
    "kaget": "surprised and emphatic",
    "santai": "relaxed and matter-of-fact, with a small smile",
    "menjelaskan": "explaining enthusiastically like sharing a fun fact",
    "kecewa": "slightly worried and disappointed",
    "senang": "happy and satisfied",
    "mengajak": "energetic and inviting, like a closing call to action",
    "tegas": "firm and confident",
}

def prompt(text, who, tone):
    t = TONE.get(tone, tone or "natural and conversational")
    return (f"Speak as {PERSONA.get(who, PERSONA['BOS'])}. Use natural everyday spoken Indonesian with lively, expressive intonation "
            f"that rises and falls like a real conversation, never flat or robotic. Emotion: {t}. Say only this line: {text}")

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())

def list_tts_models():
    try:
        req = urllib.request.Request(f"{API}/models?pageSize=200", headers={"x-goog-api-key": KEY})
        data = json.loads(urllib.request.urlopen(req, timeout=60).read())
        return [m["name"].split("/")[-1] for m in data.get("models", []) if "tts" in m["name"]]
    except Exception as e:
        print("list models failed:", e); return []

SHORT_TONE = {"penasaran": "curiously", "kaget": "in a surprised way", "santai": "casually", "menjelaskan": "enthusiastically",
              "kecewa": "with a worried tone", "senang": "happily", "mengajak": "energetically", "tegas": "firmly"}

def prompt_variant(text, who, tone, v):
    # v0 = arahan persona lengkap; v2 = naskah saja.
    # Varian pendek "Say curiously: ..." DIHAPUS (29 Okt 2026): model ikut membacakan perintah bahasa Inggris itu.
    if v == 0: return prompt(text, who, tone)
    return text

def max_len(text):
    return max(6.0, len(text.split()) * 0.75 + 2.0)

def min_len(text):
    return max(1.2, len(text.split()) * 0.22)

import array
def clip_count(pcm):
    a = array.array("h", pcm)
    return sum(1 for v in a if v >= 32700 or v <= -32700)

def normalize(pcm, peak_db=-3.0):
    a = array.array("h", pcm)
    pk = max((abs(v) for v in a), default=0)
    if pk == 0: return pcm
    g = (32767 * 10 ** (peak_db / 20)) / pk
    return array.array("h", (max(-32768, min(32767, int(v * g))) for v in a)).tobytes()

def check(cand, text):
    """Kembalikan alasan tolak, atau None kalau lolos."""
    dur = len(cand) / 2 / 24000
    if dur > max_len(text): return f"{dur:.1f} dtk terlalu panjang"
    if dur < min_len(text): return f"{dur:.1f} dtk terlalu pendek"
    c = clip_count(cand)
    if c > 3: return f"{c} sampel pecah"
    return None

def synth(text, who, model, tone=None, variant=0):
    body = {"contents": [{"parts": [{"text": prompt_variant(text, who, tone, variant)}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE.get(who, 'Orus')}}}}}
    for attempt in range(4):
        try:
            res = post(f"{API}/models/{model}:generateContent", body)
            part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"])
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:600]
            print(f"HTTP {e.code} {model}: {msg}")
            LOG.append(f"HTTP {e.code} {model}: {msg}")
            if e.code == 429 and "per day" in msg.lower() or "PerDay" in msg:
                DEAD.add(model); raise
            if e.code in (429, 500, 503): time.sleep(15 * (attempt + 1)); continue
            raise
    raise RuntimeError("gagal setelah 4 percobaan")

LOG = []
DEAD = set()

def main():
    if not KEY:
        print("GEMINI_API_KEY belum diisi di GitHub Secrets"); sys.exit(1)
    models = MODELS + [m for m in list_tts_models() if m not in MODELS]
    print("model kandidat:", models)
    # Prioritas: jadwal tayang terdekat dulu (kunci "jadwal" = "YYYY-MM-DDTHH:MM" WIB), sisanya urut nama.
    def prio(path):
        try: return (json.load(open(path)).get("jadwal") or "9999", path)
        except Exception: return ("9999", path)
    for path in sorted(glob.glob("voice/requests/*.json"), key=prio):
        req = json.load(open(path)); rid = req["id"]; out = f"voice/out/{rid}"
        if os.path.exists(f"{out}/done.json"): continue
        os.makedirs(out, exist_ok=True)
        if os.path.exists(f"{out}/error.txt"): os.remove(f"{out}/error.txt")
        meta_path = f"{out}/meta.json"
        meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
        used = meta.get("model")
        # baris lama tanpa catatan model tidak dipercaya: buat ulang semua
        if not used:
            for f in glob.glob(f"{out}/*.wav"): os.remove(f)
        i = 0; lines = req["lines"]
        while i < len(lines):
            ln = lines[i]; fn = f"{out}/{i:02d}.wav"
            if os.path.exists(fn): i += 1; continue
            pcm = None; got = None
            order = ([used] if used else []) + [m for m in models if m != used]
            for m in order:
                if pcm is not None: break
                for v in (0, 2):
                    if m in DEAD: break
                    try:
                        cand = synth(ln["text"], ln.get("who", "BOS"), m, ln.get("tone"), v)
                    except Exception as e:
                        print("model", m, "gagal:", e); break
                    why = check(cand, ln["text"])
                    if why is None:
                        pcm = cand; got = m; break
                    print(f"TOLAK {m} v{v} baris {i}: {why}"); LOG.append(f"tolak {m} v{v} baris {i}: {why}")
                    time.sleep(5)
            if pcm is None:
                open(f"{out}/error.txt", "w").write("GAGAL baris %d\n" % i + "\n".join(LOG[-6:]))
                print("GAGAL baris", i); sys.exit(1)
            if used and got != used:
                # pindah model → buang baris sebelumnya supaya semua suara seragam
                print(f"pindah model {used} -> {got}: baris sebelumnya dibuat ulang")
                for f in glob.glob(f"{out}/*.wav"): os.remove(f)
                used = got; json.dump({"model": used}, open(meta_path, "w"))
                with wave.open(f"{out}/{i:02d}.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(normalize(pcm))
                i = 0; time.sleep(7); continue
            used = got; json.dump({"model": used}, open(meta_path, "w"))
            with wave.open(fn, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(normalize(pcm))
            print(rid, i, ln["who"], round(len(pcm) / 2 / 24000, 2), "dtk", used)
            i += 1; time.sleep(7)
        durs = []
        for i in range(len(lines)):
            with wave.open(f"{out}/{i:02d}.wav") as w: durs.append(round(w.getnframes() / 24000, 2))
        json.dump({"model": used, "satu_model": True, "durations": durs}, open(f"{out}/done.json", "w"), indent=1)

if __name__ == "__main__":
    main()
