"""Dijalankan di GitHub Actions: baca voice/requests/*.json, buat file suara di voice/out/<id>/NN.wav.

Format request: {"id": "2026-10-28-reel2", "lines": [{"who": "BOS", "text": "..."}, ...]}
Hanya request yang belum punya voice/out/<id>/done.json yang diproses.
Hasil: voice/out/<id>/00.wav, 01.wav, ... (mono 24 kHz) + done.json berisi durasi tiap baris.
"""
import base64, json, os, sys, time, urllib.request, urllib.error, wave, glob

KEY = os.environ.get("GEMINI_API_KEY", "").strip()
API = "https://generativelanguage.googleapis.com/v1beta"
MODELS = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts", "gemini-2.5-flash-tts"]
VOICE = {"BOS": "Algenib", "SOPIR": "Puck", "HANTU": "Leda", "ADMIN": "Kore", "CUSTOMER": "Charon"}
PERSONA = {
    "BOS": "a middle-aged Indonesian trucking company boss, deep and slightly gravelly voice, relaxed but authoritative, like a friendly 'Pak Bos' chatting with his staff",
    "SOPIR": "an Indonesian truck driver in his 30s, warm, casual and a bit cheeky, chatting with his boss",
    "HANTU": "a small cute friendly ghost mascot, bright, playful and cheerful",
    "ADMIN": "a polite young Indonesian office admin",
    "CUSTOMER": "an Indonesian customer who is in a hurry",
}
TONE = {
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
    if v == 0: return prompt(text, who, tone)
    if v == 1: return f"Say {SHORT_TONE.get(tone, 'naturally')}: {text}"
    return text

def max_len(text):
    return max(6.0, len(text.split()) * 0.75 + 2.0)

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
    for path in sorted(glob.glob("voice/requests/*.json")):
        req = json.load(open(path)); rid = req["id"]; out = f"voice/out/{rid}"
        if os.path.exists(f"{out}/done.json"): continue
        os.makedirs(out, exist_ok=True); durs = []; used = None
        if os.path.exists(f"{out}/error.txt"): os.remove(f"{out}/error.txt")
        for i, ln in enumerate(req["lines"]):
            fn = f"{out}/{i:02d}.wav"
            if os.path.exists(fn):
                with wave.open(fn) as w: durs.append(round(w.getnframes() / 24000, 2))
                continue
            pcm = None
            order = ([used] if used else []) + [m for m in models if m != used]
            for m in order:
                if pcm is not None: break
                for v in (0, 1, 2):
                    if m in DEAD: break
                    try:
                        cand = synth(ln["text"], ln.get("who", "BOS"), m, ln.get("tone"), v)
                    except Exception as e:
                        print("model", m, "gagal:", e); break
                    dur = len(cand) / 2 / 24000
                    if dur <= max_len(ln["text"]):
                        pcm = cand; used = m; break
                    print(f"TOLAK {m} v{v}: {dur:.1f} dtk terlalu panjang"); LOG.append(f"tolak {m} v{v} {dur:.1f}s")
                    time.sleep(5)
            if pcm is None:
                open(f"{out}/error.txt", "w").write("GAGAL baris %d\n" % i + "\n".join(LOG[-6:]))
                print("GAGAL baris", i); sys.exit(1)
            fn = f"{out}/{i:02d}.wav"
            with wave.open(fn, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            durs.append(round(len(pcm) / 2 / 24000, 2)); print(rid, i, ln["who"], durs[-1], "dtk")
            time.sleep(7)
        json.dump({"model": used, "durations": durs}, open(f"{out}/done.json", "w"), indent=1)

if __name__ == "__main__":
    main()
