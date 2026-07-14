#!/usr/bin/env python3
"""Build the razor-armed re-rule pack: the discriminating experiment for
instruction-comprehension vs rater disposition (G2-P2-RESULTS instruction
audit, 2026-07-13).

Design: the 9 cases where the human second coder and the judge disagreed,
re-presented to the SAME human coder with the judge's three razors
rewritten in plain fresh-rater language and PERSISTENT on every screen
(the original kit showed compressed expert mnemonics per case and plain
gists only on an evaporating landing screen). Direction-blind: nothing
reveals the judge's ruling. The coder is asked to rule fresh.

Prediction logic (pre-stated in G2-P2-RESULTS): if the coder's original
liberal confirmations flip N under plain razors, the liberality was
instruction-comprehension; if they hold Y, it is disposition.

Output: tools/rerule_joe.html (self-contained; distinct localStorage key;
exports rulings_rerule.json).

Usage: python tools/make_rerule_pack.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

RAZORS = """THREE RULES THAT DECIDE CLOSE CALLS — read before every case.

1. MEANS-TO-AN-END IS NOT MEANING. If the walking, mapping, or effort
mattered because it HELPED FINISH THE JOB (it was useful, efficient,
informative), answer N. Answer Y only if the player claims the effort
was worth something EVEN APART FROM the objective.

2. SACRIFICE REQUIRES A PURCHASE. Answer Y only if something given up
BOUGHT something the player names (knowledge, an escape, someone else's
gain). Accepting the end with dignity, letting go, burning out
beautifully — with nothing named in exchange — is N.

3. QUOTING IS NOT ADOPTING. If the player echoes or describes the
world's poetic framing without taking it on as their own conclusion,
answer N. The claim must be in the player's own voice, as their own
assessment.

Rule fresh: judge each case as if for the first time, by these rules
and the marker rule shown below. Y / N / O (cannot decide)."""

matrix = json.loads((ROOT / "tmp" / "irr28_matrix.json").read_text(encoding="utf-8"))
targets = {r["id"] for r in matrix if r["joe"] != r["judge"]}
assert len(targets) == 9, f"expected 9 disagreement cases, got {len(targets)}"

cases = json.loads((ROOT / "tmp" / "rater_cases_irr.json").read_text(encoding="utf-8"))
sel = [dict(c) for c in cases if c["id"] in targets]
assert len(sel) == 9
for c in sel:
    c["rules"] = RAZORS + "\n\n--- MARKER RULE FOR THIS CASE ---\n" + c["rules"]

HTML_HEAD = """<!doctype html><meta charset="utf-8"><title>Re-rule (9 cases)</title>
<style>
body{font:15px/1.5 Georgia,serif;max-width:820px;margin:24px auto;padding:0 16px;background:#faf8f4;color:#222}
#rules{background:#eee9df;border-left:4px solid #8a6d3b;padding:10px 14px;font:13px/1.45 system-ui;white-space:pre-wrap}
#meta{font:13px system-ui;color:#666;margin:10px 0}
#ctx{background:#fff;border:1px solid #ddd;padding:16px 20px;white-space:pre-wrap;max-height:46vh;overflow:auto}
mark{background:#ffe89a;padding:1px 2px}
#bar{display:flex;gap:10px;align-items:center;margin:14px 0;font:14px system-ui;flex-wrap:wrap}
button{font:15px system-ui;padding:8px 18px;border:1px solid #999;border-radius:6px;background:#fff;cursor:pointer}
button.sel{background:#2b6;color:#fff;border-color:#2b6}
#note{flex:1;min-width:140px;font:13px system-ui;padding:7px}
#prog{font:12px system-ui;color:#888}
</style>
<h3 style="font-family:system-ui">Re-rule: 9 cases, fresh eyes <span id="prog"></span></h3>
<p style="font:13px system-ui;color:#666">Same task as before, 9 cases, new tie-breaking rules shown on every screen. Rule each case fresh — do not try to remember or match your earlier answers. Export and send back when the counter reads 9/9.</p>
<div id="app">
<div id="rules"></div>
<div id="meta"></div>
<div id="ctx"></div>
<div id="bar">
<button id="y">Y</button><button id="n">N</button><button id="o">OPEN</button>
<input id="note" placeholder="# note (optional)">
<button id="exp">Export</button>
</div>
</div>
<script>
const EMBEDDED=__CASES__;
let cases=[],order=[],idx=0,R={},T={};
const $=id=>document.getElementById(id);
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function init(){cases=EMBEDDED;order=[...cases.keys()];
 const rnd=mulberry(777);for(let i=order.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[order[i],order[j]]=[order[j],order[i]]}
 const saved=localStorage.getItem('raterR_rerule');if(saved){R=JSON.parse(saved);idx=order.findIndex(i=>!R[cases[i].id]);if(idx<0)idx=0}
 show()}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function show(){const c=cases[order[idx]];$('rules').textContent=c.rules;
 $('meta').textContent=`case ${idx+1}/${cases.length}  ·  marker (${c.marker})  ·  ${c.file}`;
 let ctx=esc(c.context);const q=esc(c.quote).slice(0,120);
 if(q.length>8){const at=ctx.indexOf(q.slice(0,60));if(at>=0){ctx=ctx.slice(0,at)+'<mark>'+ctx.slice(at,at+q.length)+'</mark>'+ctx.slice(at+q.length)}}
 $('ctx').innerHTML=ctx;const cur=R[c.id];
 for(const b of['y','n','o'])$(b).className=(cur&&cur.v===b.toUpperCase())?'sel':'';
 $('note').value=cur?cur.note||'':'';
 $('prog').textContent=` — ${Object.keys(R).length}/${cases.length} ruled`;
 const at=$('ctx').querySelector('mark');if(at)at.scrollIntoView({block:'center'})}
function rule(v){const c=cases[order[idx]];
 if(!T[c.id])T[c.id]={first:Date.now()};
 const prev=R[c.id];if(prev&&prev.v!==v)(T[c.id].flips=T[c.id].flips||[]).push({from:prev.v,to:v,t:Date.now()});
 R[c.id]={v,note:$('note').value,t:Date.now(),order:idx};
 localStorage.setItem('raterR_rerule',JSON.stringify(R));
 if(idx<cases.length-1){idx++;show()}else show()}
$('y').onclick=()=>rule('Y');$('n').onclick=()=>rule('N');$('o').onclick=()=>rule('O');
$('note').onchange=()=>{const c=cases[order[idx]];if(R[c.id]){R[c.id].note=$('note').value;localStorage.setItem('raterR_rerule',JSON.stringify(R))}};
document.onkeydown=e=>{if(e.target.id==='note')return;
 if(e.key==='y'||e.key==='Y')rule('Y');if(e.key==='n'||e.key==='N')rule('N');
 if(e.key==='o'||e.key==='O')rule('O');
 if(e.key==='ArrowRight'&&idx<cases.length-1){idx++;show()}
 if(e.key==='ArrowLeft'&&idx>0){idx--;show()}};
$('exp').onclick=()=>{
 const blob=new Blob([JSON.stringify({rater:'rerule-razor-armed',rulings:R,timing:T},null,1)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);
 a.download='rulings_rerule.json';a.click()};
init();
</script>
"""

out = HTML_HEAD.replace("__CASES__", json.dumps(sel, ensure_ascii=False))
dest = ROOT / "tools" / "rerule_joe.html"
dest.write_text(out, encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size:,} bytes, {len(sel)} cases, razors persistent)")
