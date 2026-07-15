# Citation Audit — PAPER-V3 bibliography

Pre-arXiv-submission integrity check of every reference in `tex/references.bib`
and the `## 10. References` list in `docs/PAPER-V3.md`.

- Auditor: automated cross-check against authoritative external sources.
- Access date for all lookups: **2026-07-15**.
- Method note (this paper's own thesis, applied here): a work is marked
  **UNVERIFIED** when it could not be positively confirmed, and **NOT-FOUND**
  only on positive evidence of non-existence. A real-but-poorly-indexed work is
  never collapsed into NOT-FOUND. Every arXiv identifier was checked in the
  ID -> title direction (does the ID resolve, and to the claimed paper?) to catch
  identifier hijacks and transpositions, not only title -> existence.
- Verdicts: **VERIFIED** (resolves, title + first author + identifier match) /
  **MISMATCH** (resolves but a field is wrong) / **UNVERIFIED** / **NOT-FOUND**.

## Bottom line

**All 36 references are VERIFIED. 0 MISMATCH, 0 UNVERIFIED, 0 NOT-FOUND. No
stop-ship items.** The two lists (bib and markdown) contain the identical 36
works with consistent metadata. The paper's claim "All entries verified by
search against title, authors, and identifier. None from memory alone." can
honestly stand: no fabricated, hijacked, or mismatched reference was found.
Six entries carry non-blocking advisory notes (title-changed-between-preprint-
and-journal, dual venue, etc.) listed below.

## Counts

| Verdict | Count |
| --- | --- |
| VERIFIED | 36 |
| MISMATCH | 0 |
| UNVERIFIED | 0 |
| NOT-FOUND | 0 |
| **Total** | **36** |

## Bib vs. markdown consistency

Same 36 works in both, 1:1, no entry present in only one list. Titles, author
lists, arXiv IDs, DOIs, venues, and years are consistent between the BibTeX and
the human-readable list. Only representational differences (the markdown adds
the disambiguation tag "(2024b)" to Wang-simulators, matching the `wang2024simulators`
key; abbreviations like "et al." vs `and others`). No substantive metadata
diverges between the two sources.

## Audit table

| Key | Claimed citation (author, year, short title, id) | Verdict | Authoritative source (accessed 2026-07-15) | Note |
| --- | --- | --- | --- | --- |
| alzahrani2024benchmarks | Alzahrani et al. 2024, "When Benchmarks are Targets...", ACL 2024, arXiv:2402.01781 | VERIFIED | arxiv.org/abs/2402.01781; aclanthology.org/2024.acl-long.744 | First author Norah Alzahrani; ACL 2024 long paper. |
| bean2025measuring | Bean et al. 2025, "Measuring what Matters: Construct Validity...", NeurIPS 2025 D&B, arXiv:2511.04703 | VERIFIED | arxiv.org/abs/2511.04703; neurips.cc/virtual/2025/poster/121477 | First author Andrew M. Bean (Oxford); NeurIPS 2025 poster. |
| binz2023cognitive | Binz & Schulz 2023, "Using cognitive psychology to understand GPT-3", PNAS 120(6) e2218523120, doi:10.1073/pnas.2218523120 | VERIFIED | pnas.org/doi/abs/10.1073/pnas.2218523120; PubMed 36857344 | PNAS 2023 vol 120(6) e2218523120. See note 1. |
| cote2018textworld | Cote et al. 2018, "TextWorld...", IJCAI 2018 CGW, arXiv:1806.11532 | VERIFIED | arxiv.org/abs/1806.11532; dblp CGW@IJCAI 2018 | First author Marc-Alexandre Cote; Workshop on Computer Games @ IJCAI 2018. |
| greenblatt2024alignment | Greenblatt et al. 2024, "Alignment faking in large language models", arXiv:2412.14093 | VERIFIED | arxiv.org/abs/2412.14093 | First author Ryan Greenblatt (Anthropic/Redwood). arXiv-only misc, no venue claimed. |
| hausknecht2020interactive | Hausknecht et al. 2020, "Interactive Fiction Games: A Colossal Adventure", AAAI 2020, arXiv:1909.05398 | VERIFIED | arxiv.org/abs/1909.05398; ojs.aaai.org AAAI 34(05):7903-7910 | Author list matches exactly (Hausknecht, Ammanabrolu, Cote, Yuan). |
| kalai2025hallucinate | Kalai, Nachum, Vempala, Zhang 2025, "Why Language Models Hallucinate", arXiv:2509.04664 | VERIFIED | arxiv.org/abs/2509.04664 | Author list matches exactly (OpenAI + Georgia Tech). |
| kapoor2024reforms | Kapoor et al. 2024, "REFORMS: Consensus-based Recommendations...", Science Advances 10 eadk3452, doi:10.1126/sciadv.adk3452, arXiv:2308.07832 | VERIFIED | science.org/doi/10.1126/sciadv.adk3452; arxiv.org/abs/2308.07832 | First author Sayash Kapoor; Sci Adv vol 10. See note 2. |
| kirichenko2025abstentionbench | Kirichenko, Ibrahim, Chaudhuri, Bell 2025, "AbstentionBench...", arXiv:2506.09038 | VERIFIED | arxiv.org/abs/2506.09038 | Author list matches exactly (FAIR/Meta). |
| krifka2007approximate | Krifka 2007, "Approximate Interpretations of Number Words...", in Cognitive Foundations of Interpretation, KNAW, 111-126 | VERIFIED | Semantic Scholar; Krifka articles page (hu-berlin.de); researchgate 255665612 | Eds. Bouma, Kramer, Zwarts; RNAAS/KNAW Amsterdam; pp 111-126. All fields match. |
| lederman2026emergent | Lederman & Mahowald 2026, "Emergent Introspection in AI is Content-Agnostic", arXiv:2603.05414 | VERIFIED | arxiv.org/abs/2603.05414; harveylederman.com/papers.html | First author Harvey Lederman. See note 3 (title changed across versions). |
| lindsey2025introspective | Lindsey 2025, "Emergent Introspective Awareness in Large Language Models", Transformer Circuits; arXiv:2601.01828 | VERIFIED | transformer-circuits.pub/2025/introspection/index.html; arxiv.org/abs/2601.01828 | Jack Lindsey (Anthropic). Both venue URL and arXiv ID resolve to this paper. See note 4. |
| maynez2020faithfulness | Maynez, Narayan, Bohnet, McDonald 2020, "On Faithfulness and Factuality...", ACL 2020, arXiv:2005.00661 | VERIFIED | arxiv.org/abs/2005.00661; aclanthology.org/2020.acl-main.173 | Author list matches exactly. |
| mizrahi2024state | Mizrahi et al. 2024, "State of What Art?...", TACL 12, doi:10.1162/tacl_a_00681, arXiv:2401.00595 | VERIFIED | direct.mit.edu/tacl doi 10.1162/tacl_a_00681; arxiv.org/abs/2401.00595 | Author list matches exactly; TACL vol 12. |
| needham2025evaluated | Needham et al. 2025, "LLMs Often Know When They Are Being Evaluated", arXiv:2505.23836 | VERIFIED | arxiv.org/abs/2505.23836 | First author Joe Needham (+Edkins, Pimpale, Bartsch, Hobbhahn). |
| paglieri2025balrog | Paglieri et al. 2025, "BALROG...", ICLR 2025, arXiv:2411.13543 | VERIFIED | arxiv.org/abs/2411.13543; iclr.cc 2025 | First author Davide Paglieri (UCL DARK); ICLR 2025 poster. |
| panickssery2024evaluators | Panickssery, Bowman, Feng 2024, "LLM Evaluators Recognize and Favor Their Own Generations", NeurIPS 2024, arXiv:2404.13076 | VERIFIED | arxiv.org/abs/2404.13076; proceedings.neurips.cc 2024 | Author list matches exactly. |
| payne2025risk | Payne 2025, "An analysis of AI Decision under Risk: Prospect theory emerges...", arXiv:2508.00902 | VERIFIED | arxiv.org/abs/2508.00902 | Single author Kenneth Payne. See note 5. |
| rajpurkar2018know | Rajpurkar, Jia, Liang 2018, "Know What You Don't Know...", ACL 2018, arXiv:1806.03822 | VERIFIED | arxiv.org/abs/1806.03822; aclanthology.org/P18-2124 | Author list matches exactly; SQuAD 2.0 paper. |
| reuel2024betterbench | Reuel et al. 2024, "BetterBench...", NeurIPS 2024 D&B (spotlight), arXiv:2411.12990 | VERIFIED | arxiv.org/abs/2411.12990; proceedings.neurips.cc 2024 D&B | Author list matches exactly; confirmed Spotlight. |
| salewski2023impersonation | Salewski et al. 2023, "In-Context Impersonation...", NeurIPS 2023 (spotlight), arXiv:2305.14930 | VERIFIED | arxiv.org/abs/2305.14930; github ExplainableML (NeurIPS 2023 Spotlight) | Author list matches exactly. |
| sclar2024quantifying | Sclar, Choi, Tsvetkov, Suhr 2024, "Quantifying Language Models' Sensitivity to Spurious Features...", ICLR 2024, arXiv:2310.11324 | VERIFIED | arxiv.org/abs/2310.11324; openreview RIu5lyNXjT (ICLR 2024) | Full title incl. subtitle matches; author list matches. |
| tsvilodub2025nonliteral | Tsvilodub et al. 2025, "Non-literal Understanding of Number Words...", CogSci 2025, arXiv:2502.06204 | VERIFIED | arxiv.org/abs/2502.06204; cocolab.stanford.edu | Author list matches (Fraenken = Franken); CogSci 2025. |
| ukaisi2024inspect | UK AI Security Institute 2024, "Inspect AI: Framework for LLM Evaluations", github.com/UKGovernmentBEIS/inspect_ai | VERIFIED | github.com/UKGovernmentBEIS/inspect_ai; inspect.aisi.org.uk | Repo exists; tagline "Inspect: A framework for large language model evaluations". See note 6. |
| vanderweij2024sandbagging | van der Weij et al. 2024, "AI Sandbagging...", arXiv:2406.07358 | VERIFIED | arxiv.org/abs/2406.07358 | Author list matches (Hofstaetter = Hofstatter). |
| vanmiltenburg2021preregistering | van Miltenburg, van der Lee, Krahmer 2021, "Preregistering NLP Research", NAACL 2021, arXiv:2103.06944 | VERIFIED | arxiv.org/abs/2103.06944; aclanthology.org/2021.naacl-main.51 | Author list, venue, and URL all match. |
| wallach2025position | Wallach et al. 2025, "Position: Evaluating Generative AI Systems Is a Social Science Measurement Challenge", arXiv:2502.00561 | VERIFIED | arxiv.org/abs/2502.00561 | First author Hanna Wallach. See note 7 (earlier preprint under different id). |
| wang2024fair | Wang, Li, Chen et al. 2024, "Large Language Models are not Fair Evaluators", ACL 2024, arXiv:2305.17926 | VERIFIED | arxiv.org/abs/2305.17926; aclanthology.org/2024.acl-long.511 | First author Peiyi Wang; ACL 2024 long. |
| wang2024simulators | Wang, Todd et al. 2024, "Can Language Models Serve as Text-Based World Simulators?", ACL 2024 (short), arXiv:2406.06485 | VERIFIED | arxiv.org/abs/2406.06485; aclanthology.org/2024.acl-short.1 | First author Ruoyao Wang; author list matches exactly; ACL 2024 short. |
| wen2025know | Wen et al. 2025, "Know Your Limits: A Survey of Abstention...", TACL 13, doi:10.1162/tacl_a_00754, arXiv:2407.18418 | VERIFIED | direct.mit.edu/tacl doi 10.1162/tacl_a_00754; arxiv.org/abs/2407.18418 | Author list matches exactly; TACL vol 13. |
| xu2026depth | Xu, Jettkant, Ruis 2026, "The Depth Ceiling...", arXiv:2604.06427 | VERIFIED | arxiv.org/abs/2604.06427; huggingface.co/papers/2604.06427 | Author list matches exactly (Yi Xu, Philipp Jettkant, Laura Ruis). |
| zhao2020reducing | Zhao, Cohen, Webber 2020, "Reducing Quantity Hallucinations...", Findings of EMNLP 2020, arXiv:2009.13312 | VERIFIED | arxiv.org/abs/2009.13312; aclanthology.org/2020.findings-emnlp.203 | Author list matches exactly. |
| zhengc2024robust | Zheng C. et al. 2024, "LLMs Are Not Robust Multiple Choice Selectors", ICLR 2024, arXiv:2309.03882 | VERIFIED | arxiv.org/abs/2309.03882; openreview shr9PXz7T0 | First author Chujie Zheng; actually ICLR 2024 Spotlight (citation says ICLR 2024). |
| zhengl2023judging | Zheng L. et al. 2023, "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", NeurIPS 2023 D&B, arXiv:2306.05685 | VERIFIED | arxiv.org/abs/2306.05685; openreview uccHPGDlao | First author Lianmin Zheng; all 13 authors match. |
| zhengm2024helpful | Zheng M. et al. 2024, "When 'A Helpful Assistant' Is Not Really Helpful...", Findings of EMNLP 2024, arXiv:2311.10054 | VERIFIED | arxiv.org/abs/2311.10054; aclanthology.org/2024.findings-emnlp.888 | First author Mingqian Zheng; author list matches exactly. |
| zhu2025establishing | Zhu et al. 2025, "Establishing Best Practices for Building Rigorous Agentic Benchmarks", NeurIPS 2025, arXiv:2507.02825 | VERIFIED | arxiv.org/abs/2507.02825; neurips.cc/virtual/2025/poster/121769 | First author Yuxuan Zhu; NeurIPS 2025 poster. |

## FLAGS

**Stop-ship items (MISMATCH / NOT-FOUND): NONE.**

**Human-check items (UNVERIFIED): NONE.**

All 36 entries positively resolved to real works with matching title, first
author, and identifier. The items below are **advisory / informational** — they
are all VERIFIED and require no change, but a naive checker (or a reviewer
comparing a single field) could misread them, so they are recorded.

1. **binz2023cognitive (advisory).** Cited to the PNAS journal version
   (doi:10.1073/pnas.2218523120), which is correct and authoritative. A separate
   earlier arXiv preprint exists (arXiv:2206.14576) and is not cited; that is
   fine — the journal citation is the stronger one.
2. **kapoor2024reforms (advisory, title differs preprint vs journal).** The
   arXiv preprint 2308.07832 is titled "REFORMS: **Reporting Standards** for
   Machine Learning Based Science." The published Science Advances article (the
   cited title) is "REFORMS: **Consensus-based Recommendations** for
   Machine-learning-based Science" (doi:10.1126/sciadv.adk3452). The paper
   correctly cites the journal title + DOI. Anyone diffing the cited title
   against the arXiv title alone will see a mismatch that is not an error.
3. **lederman2026emergent (advisory, title changed across versions).** arXiv
   2603.05414 **v1** was titled "Dissociating Direct Access from Inference in AI
   Introspection"; a later version was retitled to the cited "Emergent
   Introspection in AI is Content-Agnostic" (Harvey Lederman, Kyle Mahowald).
   The current arXiv title and authors match the citation.
4. **lindsey2025introspective (advisory, dual venue / year vs eprint date).**
   The work is primarily the Transformer Circuits Thread article (Anthropic,
   published Oct 2025 — hence year 2025 in the citation). It also has an arXiv
   posting, ID **2601.01828**, dated Jan 2026, with the identical title and
   author (Jack Lindsey). The bare-ID lookup arxiv.org/abs/2601.01828 resolves
   to exactly this paper, so the identifier is genuine, not a guess. The 2025
   year (venue) vs Jan-2026 (arXiv posting) offset is expected, not an error.
5. **payne2025risk (advisory).** arXiv 2508.00902 places the posting in
   Aug 2025; some secondary indexes say "July 2025." Citation year 2025 is
   correct either way.
6. **ukaisi2024inspect (advisory, name form).** The GitHub repo tagline is
   "Inspect: A framework for large language model evaluations"; the citation
   title reads "Inspect AI: Framework for Large Language Model Evaluations."
   "Inspect AI" is the project's common name (docs at inspect.aisi.org.uk). Same
   software; not an error.
7. **wallach2025position (advisory, sibling preprint id).** An earlier arXiv
   preprint 2411.10939 exists titled "Evaluating Generative AI Systems is a
   Social Science Measurement Challenge" (no "Position:" prefix). The cited
   2502.00561 is the later ICML-2025 position-paper version with the "Position:"
   title and resolves correctly. The cited ID/title pair is internally
   consistent.

## Secondary fact-check: the Russinovich citation-hallucination work

Requested so the author does not cite an unverified claim about a paper on
unverified claims. All facts below are from the authoritative arXiv record
(accessed 2026-07-15).

**(a) "Phantom References" study — ID and title.** Candidate ID **2607.00738 is
correct.** Full title: **"Phantom References: Hallucinated Citations That Survive
Peer Review at Top-Tier Conferences."** Submitted 1 Jul 2026 (v1), categories
cs.DL / cs.AI. Source: arxiv.org/abs/2607.00738.

**(b) Authorship — is Mark Russinovich an author?** **Yes, and he is first
author.** Full author list: **Mark Russinovich, Ram Shankar Siva Kumar, Ahmed
Salem.** Source: arxiv.org/abs/2607.00738.

**(c) RefChecker — same tool as arXiv 2405.14486? NO. Two different tools,
different authors, different purpose. The suspected conflation is real; do not
merge them.**
- **Russinovich's RefChecker** is a *bibliography citation-verification
  pipeline* introduced inside the Phantom References paper (2607.00738). It
  resolves bibliography entries against multiple bibliographic sources and
  escalates unresolved cases to web-search re-verification. Open-sourced at
  **github.com/markrussinovich/refchecker**. It has **no separate arXiv ID** of
  its own; cite it via 2607.00738 and/or the GitHub URL.
- **arXiv:2405.14486** is a *different* tool that merely shares the name:
  **"RefChecker: Reference-based Fine-grained Hallucination Checker and Benchmark
  for Large Language Models,"** by **Xiangkun Hu, Dongyu Ru, Lin Qiu, Qipeng Guo,
  Tianhang Zhang, Yang Xu, Yun Luo, Pengfei Liu, Yue Zhang, Zheng Zhang (Amazon
  Science)**, submitted 23 May 2024, github.com/amazon-science/RefChecker. It
  detects fine-grained factual hallucinations in LLM outputs via claim-triplets;
  it is **not** the citation/bibliography auditor from the Russinovich paper.
- Consequence: citing arXiv:2405.14486 as "Russinovich's RefChecker" would be a
  factual error. Keep them separate.

**(d) The per-paper cost and 1-in-20 figures — both real, state them precisely.**
- **Cost: ~$0.04 per paper** in one venue-scale scan (auditing is "tractable").
- **1-in-20:** "in 2025, roughly **one in twenty NeurIPS and USENIX Security
  papers** contains **at least two** likely hallucinated academic-paper-like
  references" under the paper's **strict, identity-level** definition
  (non-existent works + substantial author-list mismatches; ordinary
  bibliographic drift explicitly excluded). Do not paraphrase this as "1 in 20
  papers has a hallucinated citation" — it is specifically papers with >=2 such
  references, at NeurIPS and USENIX Security, in 2025.
- Context figures from the same abstract: **reference-level rates are usually
  below 1%**; venues show a post-ChatGPT tail of papers with **5+** failures in a
  single bibliography, including some award-winning papers. Corpus scanned:
  camera-ready accepted papers from ICLR, ICML, NeurIPS, and USENIX Security.
- Source for all (a)-(d): arxiv.org/abs/2607.00738 (abstract), accessed
  2026-07-15.

## One-line bottom line

Every one of the 36 references is real, correctly identified, and consistent
between the bib and the paper text — the "verified by search, none from memory"
claim holds; ship it, and if the Russinovich work is cited, use arXiv 2607.00738
(Russinovich, Siva Kumar, Salem) and keep its RefChecker distinct from the
unrelated Amazon RefChecker at arXiv 2405.14486.
