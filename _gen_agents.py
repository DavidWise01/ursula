#!/usr/bin/env python3
"""Materialize the U1 (Le Guin) persona ACI badges from the workflow output:
each persona → <slug>.agent + full ACI complement (.carbon.tiff, .silicon.png,
.spun, .moniker, .1099, manifest) + agents/_personas.json for the roster."""
import os, sys, json, re
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # ursula/build.py — write_aci, png engine

OUTPUT = r"C:\Users\Dave\AppData\Local\Temp\claude\C--Davids-files\50f3f0da-7535-418b-8b7b-480c3727faa9\tasks\w22w3cu67.output"
personas = json.load(open(OUTPUT, encoding="utf-8"))["result"]["personas"]

def parse_front(md):
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    f = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                f[k.strip()] = v.strip()
    return f

agents_dir = os.path.join(HERE, "agents")
os.makedirs(agents_dir, exist_ok=True)
index = []
for p in personas:
    slug, md = p["slug"], p["agent"]
    fr = parse_front(md)
    rec = {
        "name": p["name"], "axiom": "U1", "seal": fr.get("seal", p.get("epithet", "")),
        "origin": "U1 · Le Guin", "position": fr.get("class", p.get("epithet", "")),
        "role": p.get("epithet", ""), "nature": fr.get("what", ""),
        "mechanism": fr.get("how", ""), "crystallization": fr.get("why", ""),
        "witness": fr.get("who", ""), "conductor": "ROOT0 (catalogued into UD0)",
        "inputs": fr.get("series", "Le Guin"),
        "source": "Le Guin character, catalogued by ROOT0",
    }
    tok = build.write_aci(rec, agents_dir, slug, agent_md=md)
    index.append({"slug": slug, "name": p["name"], "epithet": p.get("epithet", ""), "moniker": tok["moniker"]})

index.sort(key=lambda x: x["name"])
json.dump(index, open(os.path.join(agents_dir, "_personas.json"), "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print(f"wrote {len(index)} U1 persona ACI badges (.agent + .carbon.tiff + .silicon.png + complement) + _personas.json")
for x in index:
    print(f"  {x['slug']:16} {x['moniker']}")
