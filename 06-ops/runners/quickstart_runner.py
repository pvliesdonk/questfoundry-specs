
#!/usr/bin/env python3
import json, random
from pathlib import Path

GENRES = ["space_opera","station_noir","surprise_me"]

def load_templates(dir_path="reference/genre_templates"):
    templates = {}
    p = Path(dir_path)
    if p.exists():
        for f in p.glob("*.json"):
            try:
                obj = json.loads(f.read_text(encoding="utf-8"))
                tid = obj.get("id") or f.stem
                templates[tid] = obj
            except Exception:
                pass
    return templates

def load_pn_policy(path="state/player_narrator.policy.json"):
    p = Path(path)
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: pass
    return {"mode":"release","allow_transient_improv":True,"feedback_channel":False,"max_deviation_radius":0.15}

def main():
    print("— Quickstart —")
    templates = load_templates()
    pn_policy = load_pn_policy()
    print(f"[policy] PN mode: {pn_policy.get('mode','release')}")
    if templates: print(f"[templates] Loaded: {', '.join(sorted(templates.keys()))}")
    lang = "English"
    genre = random.choice(GENRES[:-1])
    template = templates.get(genre)
    size = template.get('defaults',{}).get('size','medium') if template else 'medium'
    tone = template.get('defaults',{}).get('tone','balanced') if template else 'balanced'
    print(f"[plan] language={lang}, genre={genre}, size={size}, tone={tone}")
    print("[build] Research… (no spoilers)")
    print("[build] Plotting… (no spoilers)")
    print("[build] Drafting… (no spoilers)")
    print("[deliver] Project ready; PN entering release mode.")
    print("[play] next | quit")

if __name__ == "__main__":
    main()
