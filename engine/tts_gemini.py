"""Dijalankan di GitHub Actions: baca voice/requests/*.json, buat file suara di voice/out/<id>/NN.wav.

Format request: {"id": "2026-10-28-reel2", "lines": [{"who": "BOS", "text": "..."}, ...]}
Hanya request yang belum punya voice/out/<id>/done.json yang diproses.
Hasil: voice/out/<id>/00.wav, 01.wav, ... (mono 24 kHz) + done.json berisi durasi tiap baris.
"""
import base64, json, os, sys, time, urllib.request, urllib.error, wave, glob

KEY = os.environ.get("GEMINI_API_KEY", "").strip()
API = "https://generativelanguage.googleapis.com/v1beta"
MODELS = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts", "gemini-2.5-flash-tts"]
VOICE = {"BOS": "Orus", "SOPIR": "Puck", "HANTU": "Leda", "ADMIN": "Kore", "CUSTOMER": "Charon"}
STYLE = {
    "BOS": "Ucapkan dalam bahasa Indonesia, gaya bos ekspedisi yang santai tapi tegas",
    "SOPIR": "Ucapkan dalam bahasa Indonesia, gaya sopir truk yang akrab dan polos",
    "HANTU": "Ucapkan dalam bahasa Indonesia, suara hantu kecil yang ceria dan ramah",
    "ADMIN": "Ucapkan dalam bahasa Indonesia, gaya admin kantor yang sopan",
    "CUSTOMER": "Ucapkan dalam bahasa Indonesia, gaya customer yang buru-buru",
}

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

def synth(text, who, model):
    body = {"contents": [{"parts": [{"text": f"{STYLE.get(who, STYLE['BOS'])}: {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE.get(who, 'Orus')}}}}}
    for attempt in range(4):
        try:
            res = post(f"{API}/models/{model}:generateContent", body)
            part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"])
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            print(f"HTTP {e.code} {model}: {msg}")
            if e.code in (429, 500, 503): time.sleep(20 * (attempt + 1)); continue
            raise
    raise RuntimeError("gagal setelah 4 percobaan")

def main():
    if not KEY:
        print("GEMINI_API_KEY belum diisi di GitHub Secrets"); sys.exit(1)
    models = MODELS + [m for m in list_tts_models() if m not in MODELS]
    print("model kandidat:", models)
    for path in sorted(glob.glob("voice/requests/*.json")):
        req = json.load(open(path)); rid = req["id"]; out = f"voice/out/{rid}"
        if os.path.exists(f"{out}/done.json"): continue
        os.makedirs(out, exist_ok=True); durs = []; used = None
        for i, ln in enumerate(req["lines"]):
            pcm = None
            for m in ([used] if used else models):
                try: pcm = synth(ln["text"], ln.get("who", "BOS"), m); used = m; break
                except Exception as e: print("model", m, "gagal:", e)
            if pcm is None: print("GAGAL baris", i); sys.exit(1)
            fn = f"{out}/{i:02d}.wav"
            with wave.open(fn, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            durs.append(round(len(pcm) / 2 / 24000, 2)); print(rid, i, ln["who"], durs[-1], "dtk")
            time.sleep(7)
        json.dump({"model": used, "durations": durs}, open(f"{out}/done.json", "w"), indent=1)

if __name__ == "__main__":
    main()
