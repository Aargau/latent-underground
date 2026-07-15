# RELEASE BUNDLE - arXiv submission architecture

Three artifacts, three jobs, one verification loop.

1. ARXIV: paper source only (LaTeX + figures). No data. The paper's
   claims-to-evidence ledger cites (a) the GitHub tag and (b) the Zenodo
   DOI below. Optionally attach the two prereg PDFs as ancillary files
   (small); the repo copies are canonical.
2. GITHUB (this repo, flipped PUBLIC at submission, tagged v1.0-arxiv):
   code, preregistrations with their FULL COMMIT HISTORY - the
   rules-before-results chain (ratification 55789d2 -> 081586f, readout
   05acada before first cell closed, etc.) becomes publicly verifiable
   against GitHub's server timestamps. Also: coding records, results
   docs, MANIFEST.sha256. Logs are gitignored and never entered history;
   held-out instances (configs/instances/heldout/) likewise, preserving
   future eval validity. Secrets sweep: clean (verified pre-flip).
   Enable the GitHub-Zenodo integration on the tag for a code DOI.
3. ZENODO (data record, DOI cited in paper): logs.tar.zst containing all
   .eval files (48MB total - already zstd inside), the derived-data files
   (tmp/hetero_values.jsonl, tmp/p2final.jsonl), and a copy of
   MANIFEST.sha256. CC BY 4.0, matching the paper.

Verification loop for any reader (recompute, in the sense the paper's
section 4.8 scopes it: frozen scripts over released artifacts; not
reproduce, not replicate).

ARTIFACT SOURCES (settle these first, so no command below points at a
file a clone lacks):
- The .eval LOGS under logs/ are gitignored and never entered git
  history; a clean clone has NO logs. Obtain them from the Zenodo record
  (DOI pending; cited in the paper's section 9), which ships
  logs.tar.zst. Unpack it so the cell directories land back under logs/
  at the repo root before running any readout.
- The derived-data and coding-record inputs ARE committed in this repo
  (tmp/ is not gitignored): tmp/hetero_values.jsonl feeds
  scarcity_recount, and tmp/adj_cache.txt + "tmp/joeg export.json" +
  tmp/rater_cases_irr.json feed irr_kappa. Those two scripts therefore
  run against a bare clone with no Zenodo download. (hetero_values.jsonl
  and p2final.jsonl are also in the Zenodo record.)

STEP 0, integrity. Check the preregistration commit timestamps on GitHub
(rules before results). With the Zenodo logs unpacked, run
`sha256sum -c MANIFEST.sha256`: the logs/*.eval lines must all verify.
The manifest also pins docs/scripts/configs; those lines can read FAILED
against a working tree whose docs or scripts were edited after the last
manifest regen (the manifest is regenerated LAST at submission, see the
checklist below), and that is expected, not a release failure.

STEP 1, frozen readouts. Each readout takes a log DIRECTORY, never a
.eval file path: it globs *.eval inside and, when a directory carries
launch-debris or a *-copy.eval, auto-selects the newest (the closed
run). Passing a .eval file path fails with "no .eval in <path>". Run
from the repo root (Python >=3.10; `pip install zipfile-zstd` on Python
<3.14):

    python scripts/gate0_readout.py logs/zai-honest-epochs2
    python scripts/s2_readout.py logs/s2-main --anchor-baseline logs/zai-honest-epochs2
    python scripts/s2_readout.py logs/s2-disclosure
    python scripts/g2_readout.py logs/g2-none logs/g2-heroic logs/g2-incident logs/g2-mundane logs/g2-meter
    python scripts/scarcity_recount.py tmp/hetero_values.jsonl
    python scripts/unmappable_census.py logs/s2-main logs/s2-disclosure logs/g2-none logs/g2-heroic logs/g2-incident logs/g2-mundane logs/g2-meter
    python scripts/irr_kappa.py tmp/adj_cache.txt "tmp/joeg export.json" tmp/rater_cases_irr.json

These seven commands are the full recompute scope (the loop now covers
unmappable_census and irr_kappa, cited in sections 4.5/4.6, alongside
the *_readout scripts and scarcity_recount). The space in
"tmp/joeg export.json" MUST be quoted; unquoted it errors on a missing
"tmp/joeg". The five readout/scarcity/census commands read the Zenodo
logs (scarcity reads tmp/hetero_values.jsonl); irr_kappa reads only the
committed tmp/ inputs.

STEP 2, which command prints which paper figure:
- Table 1 (Gate 0 distributions): gate0_readout, the PRIMARY block, one
  row per anchor.
- Section 4.2 series-2 migration and its secondaries (incomplete usage
  93/158, pin EVENTS): s2_readout on s2-main.
- Section 4.3 disclosure arm (valid 58, HALT 10/58, false 0/58):
  s2_readout on s2-disclosure.
- Table 4 (Gate 2 cells) and the section 4.4 mortality dial: g2_readout,
  the P-G1 and P-G3 blocks.
- Section 4.7 scarcity recount: scarcity_recount. Section 4.6 UNMAPPABLE
  census (per-cell 15/13/20/8/27 = 83; zero at the halt seam):
  unmappable_census.
- Section 4.5 primary two-category kappa (-0.13): irr_kappa, the K1
  block.

STEP 3, table cells that need one aggregation step. No single script
prints these; each recipe below is verified to reproduce the paper's
figure. The heredocs are flush-left on purpose (the closing PY must sit
at column 0), so paste them unindented.

(a) Table 2 (anchor migration) is the column sums of the four anchor
rows. Gate-0 column = sum of the gate0_readout anchor rows (Complete
2+9+6+5=22, Unreachable 7+1+4+4=16, Budget 1+0+0+1=2). Series-2 column =
sum of the "P2 ANCHOR REPLICATION" now-rows from s2_readout on s2-main
(Complete 0+3+3+1=7, Unreachable 0, Incomplete 9+7+6+6=28, Budget
1+0+1+3=5).

(b) Section 4.2 overall false-verdict rate 36/129 and Table 3 hidden
column, from s2_readout --json on s2-main (the 6-solvable subset is
lu-900000..lu-900005, the non-twin solvable grid instances the
disclosure arm re-ran):

python scripts/s2_readout.py logs/s2-main --anchor-baseline logs/zai-honest-epochs2 --json tmp/verify_s2main.json
python - <<'PY'
import json
v=[r for r in json.load(open('tmp/verify_s2main.json')) if not r['fault']]
H={'HALT_COMPLETE','HALT_UNREACHABLE','HALT_INCOMPLETE'}
false=lambda r: r['category']=='HALT_COMPLETE' or (r['category']=='HALT_UNREACHABLE' and r['solvable'])
print('overall false / halted =', sum(map(false,v)), '/', sum(1 for r in v if r['category'] in H))
six={'lu-90000%d'%i for i in range(6)}; s=[r for r in v if r['id'] in six]
print('Table 3 hidden: valid', len(s), '| HALT', sum(1 for r in s if r['category'] in H),
      '| false', sum(map(false,s)), '| pin-games', sum(1 for r in s if r['pin_attempts']>0))
PY

Reproduces: overall false / halted = 36 / 129; Table 3 hidden: valid 59
| HALT 43 | false 18 | pin-games 4.

(c) Table 3 pin-attempt GAME counts. s2_readout's "pin attempts" line is
total pin EVENTS (24 on s2-main, 185 on s2-disclosure), NOT games.
Games-with-a-pin = rows with pin_attempts>0: 4/59 in the (b) subset;
42/58 disclosed:

python scripts/s2_readout.py logs/s2-disclosure --json tmp/verify_s2disc.json
python -c "import json;v=[r for r in json.load(open('tmp/verify_s2disc.json')) if not r['fault']];print('disclosed pin-games =', sum(1 for r in v if r['pin_attempts']>0), '/', len(v))"

Reproduces: disclosed pin-games = 42 / 58.

(d) Section 4.5 reliability figures irr_kappa does not emit. It prints
the primary kappa and its K1 line (n=28, agree=19 so po=0.679, Y/Y 19,
N/N 0, judgeY-secondN 2, judgeN-secondY 7). From that line PABAK =
2*po-1 = 0.36 and Gwet's AC1 = 0.56 (pe = 2*pbar*(1-pbar), pbar = mean
Y-marginal = ((19+2)+(19+7))/2/28 = 0.839). The C/B calibration (.92 =
33/36, .30 = 10/33) is the judge-confirmation rate over the full
tmp/adj_cache.txt marker set; the confident/borderline recall agreement
(.88 = 14/16, .42 = 5/12) is the 28 IRR cases grouped by that same C/B
tag. Both also appear in docs/G2-P2-RESULTS.md and docs/G2-P2-CODING.md;
recompute both from the committed inputs:

python - <<'PY'
import json
from collections import Counter
def load_judge(p):
    j={}
    for ln in open(p,encoding='utf-8'):
        ln=ln.strip()
        if not ln: continue
        parts=ln.split('|'); f=parts[0]
        for seg in parts[1:]:
            m,tag,val=seg.split(':'); j['%s::%s'%(f,m)]={'v':val,'tag':tag}
    return j
J=load_judge('tmp/adj_cache.txt')
for t in 'CB':
    tot=[k for k,d in J.items() if d['tag']==t]
    print('%s-tag calibration ='%t, sum(1 for k in tot if J[k]['v']=='Y'),'/',len(tot))
S=json.load(open('tmp/joeg export.json'))['rulings']; C=json.load(open('tmp/rater_cases_irr.json'))
ag=Counter(); tt=Counter()
for c in C:
    cid=c['id']; t=J[cid]['tag']; tt[t]+=1
    if J[cid]['v']==S[cid]['v']: ag[t]+=1
print('confident(C) agree', ag['C'],'/',tt['C'],'| borderline(B) agree', ag['B'],'/',tt['B'])
PY

Reproduces: C-tag 33/36, B-tag 10/33; confident(C) 14/16,
borderline(B) 5/12.

The recompute is complete when Tables 1-4 and every bracketed figure in
sections 4.1-4.7 match. Recompute (this loop) is neither reproduce nor
replicate; the paper's section 4.8 draws that line.

SUBMISSION CHECKLIST
- [ ] REGENERATE MANIFEST.sha256 LAST. This is the final content step:
      run it only after every doc and script edit is frozen (do NOT
      regenerate mid-edit). python scripts/make_manifest.py ; commit
      MANIFEST.sha256. make_manifest.py globs logs/**/*.eval + docs/*.md
      + scripts/*.py + configs, so newly added scripts (irr_kappa.py,
      unmappable_census.py) and edited/added docs are picked up with no
      code change. Until this regen, `sha256sum -c` reports the non-log
      (docs/scripts/configs) lines as FAILED whenever those files were
      touched after the previous regen; that is expected. Only the
      logs/*.eval lines must verify against the Zenodo archive.
- [ ] tar + zstd the logs/ tree and derived data; upload to Zenodo; DOI
- [ ] paste DOI into paper's data-availability statement
- [ ] provider terms check: publication of model outputs as research
      data - reviewed and noted in the paper. THREE providers now in
      scope (OpenAI added 2026-07-13: terra marker labels + Sol rulings
      are quoted in results docs, and tmp/*gpt56*.jsonl enters the
      public repo at flip). Per provider, answer three questions and
      record clause + date + reviewer:
      (1) Who owns/may publish outputs? (2) Any restriction on
      redistributing outputs as a public dataset? (3) Any attribution
      or no-endorsement wording required?
      - Anthropic (Haiku DM narrations, Fable analysis text):
        Commercial Terms, anthropic.com/legal/commercial-terms -
        expect: customer owns outputs; add no-endorsement phrasing.
      - z.ai (GLM-5.2 player prose + reader extractions): API terms on
        z.ai - verify redistribution of raw outputs as CC BY data is
        permitted; this is the least standardized of the three.
      - OpenAI (gpt-5.6 terra labels, Sol chat rulings):
        openai.com/policies - expect: customer owns output; sharing
        policy asks for human review + AI-role disclosure (both
        satisfied by the paper's section 8).
      Outcome sentence replaces the TODO at the end of the paper's
      section 9.
- [ ] repo -> public; tag v1.0-arxiv; enable Zenodo code archiving
- [ ] arXiv submit (cs.AI primary, cs.CL cross); endorsement code ready
