"""Pemeriksa "dengar": Gemini mendengarkan tiap baris suara lalu dicocokkan dengan naskah.

Dijalankan di GitHub Actions setelah engine/tts_gemini.py (secret GEMINI_API_KEY, model teks — kuota terpisah dari TTS).
Untuk tiap voice/out/<id>/ yang sudah punya done.json tapi belum punya dengar.json yang cocok:
- transkripsi tiap NN.wav + penilaian bunyi rusak (kresek, distorsi, kata terpotong, membaca instruksi, bahasa salah)
- cocokkan kata dengan naskah (kemiripan >= 0.75)
- tulis dengar.json {lolos, lines:[{naskah, transkrip, kemiripan, rusak, alasan}]}
Baris yang gagal dihapus (wav + done.json) supaya tts_gemini.py membuatnya ulang dengan model yang sama.
Keluar dengan kode 3 kalau ada baris yang dihapus (workflow lalu menjalankan TTS + dengar sekali lagi).
Hanya memeriksa request yang jadwalnya belum lewat lebih dari 1 hari (atau tanpa jadwal).
"""
import base64, datetime as dt, difflib, glob, json, os, re, sys, time, urllib.request, urllib.error

KEY = os.environ.get("GEMINI_API_KEY", "").strip()
API = "https://generativelanguage.googleapis.com/v1beta"
MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.0-flash", "gemini-2.5-flash-lite"]
AMBANG = 0.8
WIB = dt.timezone(dt.timedelta(hours=7))

PROMPT = """Kamu pemeriksa kualitas voiceover iklan berbahasa Indonesia.
Dengarkan audio ini lalu:
1. Tulis transkrip PERSIS kata per kata yang benar-benar diucapkan (bahasa Indonesia, tulis angka sebagai kata, singkatan seperti MST/DEMO/CDD tulis huruf kapital).
2. Nilai apakah audio rusak: ada kresek/derau/distorsi, suara pecah, kata terpotong atau tertelan, suara seperti robot rusak, ada suara lain selain satu orang bicara, membaca instruksi berbahasa Inggris, atau bahasanya bukan Indonesia.
Naskah yang seharusnya diucapkan: "{naskah}"
Jawab hanya JSON: {{"transkrip": "...", "rusak": true/false, "alasan": "kosong kalau tidak rusak"}}"""


def norm(t):
    t = t.lower().replace("&", " dan ")
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    rep = {"nggak": "gak", "enggak": "gak", "ngga": "gak", "nggk": "gak", "em es te": "mst", "m s t": "mst"}
    t = " " + re.sub(r"\s+", " ", t).strip() + " "
    for a, b in rep.items():
        t = t.replace(f" {a} ", f" {b} ")
    return t.split()


# kata perintah bahasa Inggris yang tidak boleh terdengar (tanda model membacakan instruksi)
INSTRUKSI = {"say", "speak", "curiously", "casually", "enthusiastically", "energetically", "happily", "firmly",
             "surprised", "worried", "tone", "emotion", "line", "this", "only", "natural", "indonesian", "voice",
             "boss", "driver", "ghost", "like", "with", "the", "way", "in", "a", "an", "and", "intonation", "expressive"}


def kata_asing(naskah, transkrip):
    n = set(norm(naskah))
    return [w for w in norm(transkrip) if w in INSTRUKSI and w not in n]


def mirip(a, b):
    return round(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(), 2)


def ask(model, wav_b64, naskah):
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": wav_b64}},
                                    {"text": PROMPT.format(naskah=naskah)}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    req = urllib.request.Request(f"{API}/models/{model}:generateContent", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=120) as r:
        res = json.loads(r.read())
    txt = res["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(txt)


DEAD = set()


def listen(path, naskah):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    for m in MODELS:
        if m in DEAD:
            continue
        for attempt in range(3):
            try:
                return ask(m, b64, naskah), m
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:300]
                print(f"HTTP {e.code} {m}: {msg}")
                if e.code in (404, 400) or (e.code == 429 and ("day" in msg.lower())):
                    DEAD.add(m); break
                time.sleep(10 * (attempt + 1))
            except Exception as e:
                print("gagal", m, e); time.sleep(5)
    return None, None


def relevant(req):
    j = req.get("jadwal")
    if not j:
        return True
    try:
        t = dt.datetime.fromisoformat(j).replace(tzinfo=WIB)
    except Exception:
        return True
    return t > dt.datetime.now(WIB) - dt.timedelta(days=1)


def main():
    if not KEY:
        print("GEMINI_API_KEY kosong"); sys.exit(1)
    removed = False
    for path in sorted(glob.glob("voice/requests/*.json")):
        req = json.load(open(path)); rid = req["id"]; out = f"voice/out/{rid}"
        if not os.path.exists(f"{out}/done.json") or not relevant(req):
            continue
        done = json.load(open(f"{out}/done.json"))
        sig = [done.get("durations"), req.get("rev")]
        if os.path.exists(f"{out}/dengar.json"):
            old = json.load(open(f"{out}/dengar.json"))
            if old.get("sig") == sig:
                continue
        lines, gagal = [], []
        for i, ln in enumerate(req["lines"]):
            fn = f"{out}/{i:02d}.wav"
            res, model = listen(fn, ln["text"])
            if res is None:
                lines.append({"naskah": ln["text"], "transkrip": None, "catatan": "tidak bisa didengar (kuota/model)"})
                continue
            k = mirip(ln["text"], res.get("transkrip", ""))
            rusak = bool(res.get("rusak"))
            asing = kata_asing(ln["text"], res.get("transkrip", ""))
            if asing:
                rusak = True
                res["alasan"] = (res.get("alasan", "") + f" | terdengar kata perintah Inggris: {' '.join(asing)}").strip(" |")
            ok = k >= AMBANG and not rusak
            lines.append({"naskah": ln["text"], "transkrip": res.get("transkrip"), "kemiripan": k,
                          "rusak": rusak, "alasan": res.get("alasan", ""), "lolos": ok, "model": model})
            print(rid, i, "OK" if ok else "GAGAL", k, res.get("transkrip"), "|", res.get("alasan", ""))
            if not ok:
                gagal.append(i)
            time.sleep(2)
        unchecked = any(l.get("transkrip") is None for l in lines)
        lolos = not gagal and not unchecked
        json.dump({"sig": sig, "lolos": lolos, "belum_dicek": unchecked, "lines": lines},
                  open(f"{out}/dengar.json", "w"), ensure_ascii=False, indent=1)
        if gagal:
            # buang baris gagal agar dibuat ulang (model tetap sama lewat meta.json)
            up = f"{out}/ulang.json"
            tries = json.load(open(up)).get("ulang", 0) if os.path.exists(up) else 0
            if tries < 2:
                for i in gagal:
                    os.remove(f"{out}/{i:02d}.wav")
                os.remove(f"{out}/done.json")
                json.dump({"ulang": tries + 1}, open(f"{out}/ulang.json", "w"))
                removed = True
                print(rid, "baris dibuat ulang:", gagal)
    sys.exit(3 if removed else 0)


if __name__ == "__main__":
    main()
