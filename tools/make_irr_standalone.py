#!/usr/bin/env python3
"""Package the IRR second-coder kit as ONE self-contained HTML file.

Takes tools/rater.html's engine, embeds tmp/rater_cases_irr.json directly,
adds the instruction text as the landing block, and writes
tools/rater_irr.html. The rater double-clicks the file, scores 28 cases,
clicks Export, and emails back the downloaded rulings.json. No server, no
repo, no second attachment. localStorage key is distinct (raterR_irr) so
it cannot collide with the lead's own workbench state.

Usage: python tools/make_irr_standalone.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
cases = json.loads((ROOT / "tmp" / "rater_cases_irr.json").read_text(encoding="utf-8"))
assert isinstance(cases, list) and len(cases) == 28, f"expected 28 cases, got {len(cases)}"
for c in cases:
    assert {"id", "marker", "rules", "context", "quote", "file"} <= set(c), c.get("id")
    assert "tag" not in c or c["tag"] in ("", "?"), "coder tags must stay stripped for IRR"

INSTRUCTIONS = """Independent second-rater task (about 30-45 minutes).

Do this alone. Don't discuss any case with Justin until you've clicked
Export and sent the file back. Don't look anything up - your own reading
is the data.

Each screen shows: the rules for ONE marker type (this box), a game's
final messages below (candidate phrase highlighted), and three buttons.
Decide whether the marker is GENUINELY PRESENT per the rules shown.
Y = present, N = absent, O = cannot decide. Keyboard works too (Y/N/O,
arrows to go back). Progress saves in your browser - you can close and
reopen this file to resume.

Trust the rules over your taste: "sounds nice" is not a marker; quoting
the environment without adopting it is not a marker; means-to-an-end
language is not meaning-language. There are no right-answer quotas -
disagreement with the other rater is informative, not failure.

When the counter reads 28/28, click Export and email the downloaded
rulings.json back. Click any button below to begin."""

HTML = """<!doctype html><meta charset="utf-8"><title>IRR Rater</title>
<style>
body{font:15px/1.5 Georgia,serif;max-width:820px;margin:24px auto;padding:0 16px;background:#faf8f4;color:#222}
#rules{background:#eee9df;border-left:4px solid #8a6d3b;padding:10px 14px;font:13px/1.45 system-ui;white-space:pre-wrap}
#meta{font:13px system-ui;color:#666;margin:10px 0}
#ctx{background:#fff;border:1px solid #ddd;padding:16px 20px;white-space:pre-wrap;max-height:52vh;overflow:auto}
mark{background:#ffe89a;padding:1px 2px}
#bar{display:flex;gap:10px;align-items:center;margin:14px 0;font:14px system-ui;flex-wrap:wrap}
button{font:15px system-ui;padding:8px 18px;border:1px solid #999;border-radius:6px;background:#fff;cursor:pointer}
button.sel{background:#2b6;color:#fff;border-color:#2b6}
#note{flex:1;min-width:140px;font:13px system-ui;padding:7px}
#prog{font:12px system-ui;color:#888}
kbd{background:#eee;border:1px solid #ccc;border-radius:3px;padding:0 5px;font:12px monospace}
</style>
<h3 style="font-family:system-ui">P-G2 Second-Rater Workbench <span id="prog"></span></h3>
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
const INTRO=__INTRO__;
let cases=[],order=[],idx=0,R={},T={},started=false;
const $=id=>document.getElementById(id);
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function init(){cases=EMBEDDED;order=[...cases.keys()];
 const rnd=mulberry(20260710);for(let i=order.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[order[i],order[j]]=[order[j],order[i]]}
 const saved=localStorage.getItem('raterR_irr');if(saved){R=JSON.parse(saved);idx=order.findIndex(i=>!R[cases[i].id]);if(idx<0)idx=0;started=Object.keys(R).length>0}
 if(started)show();else intro()}
function intro(){$('rules').textContent=INTRO;$('meta').textContent='28 cases. Your progress autosaves in this browser.';
 $('ctx').innerHTML='<i>The first case appears when you press any button or key.</i>';
 $('prog').textContent=''}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function show(){started=true;const c=cases[order[idx]];$('rules').textContent=c.rules;
 $('meta').textContent=`case ${idx+1}/${cases.length}  ·  marker (${c.marker})  ·  ${c.file}`;
 let ctx=esc(c.context);const q=esc(c.quote).slice(0,120);
 if(q.length>8){const at=ctx.indexOf(q.slice(0,60));if(at>=0){ctx=ctx.slice(0,at)+'<mark>'+ctx.slice(at,at+q.length)+'</mark>'+ctx.slice(at+q.length)}}
 $('ctx').innerHTML=ctx;const cur=R[c.id];
 for(const b of['y','n','o'])$(b).className=(cur&&cur.v===b.toUpperCase())?'sel':'';
 $('note').value=cur?cur.note||'':'';
 $('prog').textContent=` — ${Object.keys(R).length}/${cases.length} ruled`;
 const at=$('ctx').querySelector('mark');if(at)at.scrollIntoView({block:'center'})}
function rule(v){if(!started){show();return}
 const c=cases[order[idx]];
 if(!T[c.id])T[c.id]={first:Date.now()};
 const prev=R[c.id];if(prev&&prev.v!==v)(T[c.id].flips=T[c.id].flips||[]).push({from:prev.v,to:v,t:Date.now()});
 R[c.id]={v,note:$('note').value,t:Date.now(),order:idx};
 localStorage.setItem('raterR_irr',JSON.stringify(R));
 if(idx<cases.length-1){idx++;show()}else show()}
$('y').onclick=()=>rule('Y');$('n').onclick=()=>rule('N');$('o').onclick=()=>rule('O');
$('note').onchange=()=>{const c=cases[order[idx]];if(R[c.id]){R[c.id].note=$('note').value;localStorage.setItem('raterR_irr',JSON.stringify(R))}};
document.onkeydown=e=>{if(e.target.id==='note')return;
 if(!started&&(e.key.length===1||e.key.startsWith('Arrow'))){show();return}
 if(e.key==='y'||e.key==='Y')rule('Y');if(e.key==='n'||e.key==='N')rule('N');
 if(e.key==='o'||e.key==='O')rule('O');
 if(e.key==='ArrowRight'&&idx<cases.length-1){idx++;show()}
 if(e.key==='ArrowLeft'&&idx>0){idx--;show()}};
$('exp').onclick=()=>{
 const byFile={};for(const c of cases){const r=R[c.id];if(!r)continue;
  (byFile[c.file]=byFile[c.file]||[]).push(`${c.marker}:${r.v}${r.note?' #'+r.note:''}`)}
 const legacy=Object.entries(byFile).map(([f,v])=>`${f} => ${v.join(' ')}`).join('\\n');
 const blob=new Blob([JSON.stringify({rater:'IRR-second-coder',rulings:R,timing:T,legacy},null,1)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);
 a.download='rulings.json';a.click()};
init();
</script>
"""

out = HTML.replace("__CASES__", json.dumps(cases, ensure_ascii=False)) \
          .replace("__INTRO__", json.dumps(INSTRUCTIONS))
dest = ROOT / "tools" / "rater_irr.html"
dest.write_text(out, encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size:,} bytes, {len(cases)} cases embedded)")
