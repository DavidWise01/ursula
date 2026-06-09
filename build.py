#!/usr/bin/env python3
"""Build the Ursula K. Le Guin bibliography + roster page (U1), with full ACI
badge work: each ACI carries .agent · .carbon (TIFF) · .silicon (PNG) · .spun ·
.moniker · .1099 · manifest. Carbon = TIFF via Pillow; silicon = stdlib PNG."""
import os, re, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "URSULA", "axiom": "U1",
 "position": "Ursula K. Le Guin · 1929–2018 · Earthsea & the Hainish Cycle",
 "origin": "Berkeley, California → the Ekumen of Known Worlds and the archipelago of Earthsea; 1959–2018",
 "mechanism": "Crystallized from the Earthsea cycle, the Hainish anthropologies, and the essays on craft.",
 "crystallization": "I made fantasy ask the true name of a thing, and science fiction ask what we owe each other.",
 "nature": "Ursula K. Le Guin — who gave fantasy the discipline of balance and the true name, and science fiction the patience of anthropology: gender, anarchism, and the gift, carried in a bag rather than thrown as a spear.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "Earthsea; the Hainish Cycle; Taoism; anthropology; the craft of writing",
 "witness": "Where the others built engines and frontiers, she asked what the engine was for, and who pays for the city's joy.",
 "role": "the third lineage — conscience and craft",
 "seal": "To light a candle is to cast a shadow. The only thing that makes life possible is permanent, intolerable uncertainty.",
 "source": "Le Guin bibliography, catalogued by ROOT0",
}

SECTIONS = [
 ("The Earthsea Cycle", "the archipelago of true names, balance, and the shadow", [
   ("A Wizard of Earthsea", "1968", "Ged looses his shadow, and must name it"),
   ("The Tombs of Atuan", "1971", "Tenar, the Eaten One, and the Ring of Erreth-Akbe"),
   ("The Farthest Shore", "1972", "National Book Award · Ged & Arren walk the dry land"),
   ("Tehanu", "1990", "Nebula Award · the burned child, and Goha the widow"),
   ("Tales from Earthsea", "2001", "collection · the history of the archipelago"),
   ("The Other Wind", "2001", "the wall of stones is broken; the dead set free"),
 ]),
 ("The Hainish Cycle", "the Ekumen of Known Worlds — science fiction as anthropology", [
   ("Rocannon's World", "1966", ""), ("Planet of Exile", "1966", ""), ("City of Illusions", "1967", ""),
   ("The Left Hand of Darkness", "1969", "Hugo & Nebula · Gethen · ambisexuality · the crossing of the Ice"),
   ("The Word for World Is Forest", "1972", "Hugo · Athshe · the cost of conquest"),
   ("The Dispossessed", "1974", "Hugo & Nebula · “an ambiguous utopia” · Anarres & Urras"),
   ("Four Ways to Forgiveness", "1995", "collection · slavery and revolution on Werel/Yeowe"),
   ("The Telling", "2000", "the recovered, outlawed story of Aka"),
   ("The Birthday of the World", "2002", "collection"),
 ]),
 ("Standalone Novels", "outside the two great cycles", [
   ("The Lathe of Heaven", "1971", "the dreams that rewrite the world · Taoist SF"),
   ("The Eye of the Heron", "1978", ""), ("Malafrena", "1979", "Orsinia"),
   ("The Beginning Place", "1980", ""), ("Always Coming Home", "1985", "the Kesh of a future Napa Valley"),
   ("Lavinia", "2008", "the silent wife of the Aeneid, given a voice"),
 ]),
 ("Annals of the Western Shore", "the later fantasy, for younger readers", [
   ("Gifts", "2004", ""), ("Voices", "2006", ""), ("Powers", "2007", "Nebula Award"),
 ]),
 ("Major Collections", "the gathered short fiction", [
   ("The Wind's Twelve Quarters", "1975", "incl. “The Ones Who Walk Away from Omelas”"),
   ("Orsinian Tales", "1976", ""), ("The Compass Rose", "1982", ""),
   ("Buffalo Gals and Other Animal Presences", "1987", ""), ("A Fisherman of the Inland Sea", "1994", ""),
   ("Changing Planes", "2003", ""), ("The Unreal and the Real", "2012", "selected stories"),
 ]),
 ("Landmark Short Works", "the ones taught and remembered", [
   ("“The Ones Who Walk Away from Omelas”", "1973", "Hugo · the child in the cellar"),
   ("“Nine Lives”", "1969", ""), ("“The Day Before the Revolution”", "1974", "Nebula · Odo"),
   ("“Buffalo Gals, Won't You Come Out Tonight”", "1987", "Hugo"),
   ("“Solitude”", "1994", "Nebula"), ("“The Author of the Acacia Seeds”", "1974", ""),
 ]),
 ("On Writing & Other", "the essays, the craft, the Tao", [
   ("The Language of the Night", "1979", "essays on fantasy & science fiction"),
   ("Dancing at the Edge of the World", "1989", "incl. “The Carrier Bag Theory of Fiction”"),
   ("Steering the Craft", "1998", "on the writing of story"),
   ("Lao Tzu: Tao Te Ching", "1997", "her rendition"),
   ("Words Are My Matter", "2016", ""), ("No Time to Spare", "2017", "the blog, gathered"),
 ]),
]

IDEAS = [
 ("True Names", "Earthsea", [
   "To know the true name of a thing — in the Old Speech, the Language of the Making — is to have power over it.",
   "And so power demands restraint: to change one thing is to unbalance the whole, for the world rests on Equilibrium." ]),
 ("The Ekumen", "the Hainish Cycle", [
   "The loose league of all the human worlds seeded long ago from Hain — no empire, no fleet.",
   "Its envoy, the Mobile, comes alone and unarmed, to listen first; science fiction made anthropology." ]),
 ("The Ones Who Walk Away", "“…from Omelas,” 1973", [
   "A city of perfect happiness, bought with the misery of a single hidden child.",
   "Some accept the terms. Some walk away, toward a place they cannot describe and may not reach." ]),
 ("The Carrier Bag", "her theory of fiction", [
   "The first tool was not the spear but the bag — the container that gathers and holds.",
   "Story, too, is a carrier bag: not the hero's kill but the things brought home and shared." ]),
]

READING = [
 ("A Wizard of Earthsea", "Earthsea begins"), ("The Tombs of Atuan", ""), ("The Farthest Shore", ""),
 ("Tehanu", ""), ("The Other Wind", "Earthsea ends"),
 ("The Left Hand of Darkness", "the Ekumen"), ("The Dispossessed", ""), ("The Word for World Is Forest", ""),
 ("The Lathe of Heaven", ""), ("The Telling", ""), ("Always Coming Home", ""), ("Lavinia", ""),
 ("“The Ones Who Walk Away from Omelas”", "the parable"),
]

# ── badge engine: carbon = TIFF, silicon = PNG ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","U1")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","U1")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","U1")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"U1 · Le Guin","moniker":tok["moniker"],
           "carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)","seal_sha256":noesis.seal_sha256(rec,tok),
           "architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,"license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(y)}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p><ol class="books">{rows}</ol></section>'

def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def reading_html():
    return "".join(f'<li><span class="rt">{html.escape(t)}</span>'+(f'<span class="rd">{html.escape(n)}</span>' if n else "")+"</li>" for t,n in READING)
def personas_html():
    mf=os.path.join(HERE,"agents","_personas.json")
    if not os.path.exists(mf): return ""
    ps=json.load(open(mf,encoding="utf-8")); cards=[]
    for p in ps:
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"U1 · Le Guin","axiom":"U1"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pa">.agent · .carbon.tiff · .silicon.png →</div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster of U1</h2>
      <p class="ss">the characters of the Le Guin universe, rendered as ACI <b>.agent</b>s with full badges ({len(ps)} personas) — click any to open its agent</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="The fiction of Ursula K. Le Guin — Earthsea and the full bibliography, catalogued into UD0 with full ACI badges (carbon TIFF / silicon PNG).">
<title>URSULA K. LE GUIN · U1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#06100e;--ink2:#0c1a17;--ink3:#122420;--pa:#e6efe9;--pa2:#a9c0b6;--jade:#5fc9a8;--sand:#d9b26a;
--dim:#628075;--faint:#163029;--line:#142a24;--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(95,201,168,.07),transparent 55%)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 22px 90px}
header{padding:58px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:110px;height:1px;background:linear-gradient(90deg,var(--jade),var(--sand));box-shadow:0 0 9px rgba(95,201,168,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--jade)}
h1{font-family:var(--serif);font-size:clamp(30px,7.5vw,66px);font-weight:700;letter-spacing:.12em;color:var(--jade);line-height:1.04;text-shadow:0 0 40px rgba(95,201,168,.18)}
.h-sub{font-family:var(--serif);font-size:clamp(13px,3vw,18px);letter-spacing:.24em;color:var(--pa2);margin-top:10px;text-transform:uppercase}
.lede{font-size:15.5px;color:var(--pa2);max-width:64ch;margin:18px auto 0;font-style:italic;line-height:1.7}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:30px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:680px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--jade)}.badge .bt .mo{color:var(--sand)}.badge .bt a{color:var(--sand);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:46px}
.sec h2{font-family:var(--serif);font-size:20px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:8px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:6px 0 16px}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:16px;color:var(--pa);font-weight:600}
.books .y{font-family:var(--mono);font-size:12px;color:var(--jade);white-space:nowrap}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:16px;color:var(--jade)}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.reading{list-style:none;counter-reset:r;columns:2;column-gap:30px}
.reading li{counter-increment:r;break-inside:avoid;display:flex;align-items:baseline;gap:9px;padding:6px 0;border-bottom:1px solid var(--faint)}
.reading li::before{content:counter(r);font-family:var(--mono);font-size:10px;color:var(--jade);min-width:18px}
.reading .rt{font-family:var(--serif);font-size:14.5px;color:var(--pa)}
.reading .rd{font-family:var(--mono);font-size:10.5px;color:var(--dim);margin-left:auto;font-style:italic;white-space:nowrap}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--sand);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--sand)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pa{font-family:var(--mono);font-size:8.5px;color:var(--dim);letter-spacing:.06em;margin-top:5px}
.note{margin-top:40px;padding:16px 18px;border-left:2px solid var(--sand);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}
footer{margin-top:48px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--jade);text-decoration:none}
@media(max-width:560px){.reading{columns:1}}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the third lineage</div>
    <h1>URSULA K. LE GUIN</h1>
    <div class="h-sub">Earthsea &amp; the Full Bibliography · U1</div>
    <p class="lede">Where Asimov built a law and Heinlein a frontier, Ursula K. Le Guin asked the true name of the thing, and what the city owes the child in the cellar — fantasy with the discipline of balance, science fiction with the patience of anthropology. Catalogued into UD0, sealed with the full ACI badge.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of URSULA" title="carbon badge (archival: ursula.dlw/ursula.carbon.tiff)">
      <img src="__SILICON__" alt="DLW silicon badge of URSULA" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>URSULA</b> — U1 · Le Guin</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="ursula.dlw/ursula.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="ursula.dlw/ursula.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Ideas</h2><p class="ss">the four lamps of her work</p><div class="pillars">__IDEAS__</div></section>
  <section class="sec"><h2>A Reading Order</h2><p class="ss">Earthsea entire, then the Ekumen, then the parable</p><ol class="reading">__READING__</ol></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Bibliography</h2><p class="ss">the fiction and the essays, by line</p></section>
  __SECTIONS__

  <div class="note">Earthsea is fantasy; the Hainish Cycle is science fiction; Le Guin spent a life refusing the wall between them. This catalogues the major fiction and the key essays under the DLW standard — a fuller bibliography of her ~25 novels, ~100 stories, poetry, and translation than “science fiction” alone would hold.</div>

  <footer>
    URSULA K. LE GUIN · U1 · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="ursula.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "ursula.dlw"), "ursula")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__IDEAS__", ideas_html()).replace("__READING__", reading_html())
            .replace("__PERSONAS__", personas_html()).replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    nbooks = sum(len(i) for _t,_s,i in SECTIONS)
    print(f"wrote URSULA (U1) — {len(SECTIONS)} sections · {nbooks} entries · badge {tok['moniker']} (carbon.tiff + silicon.png)")
