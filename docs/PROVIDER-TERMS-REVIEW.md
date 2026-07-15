# Provider Terms Review — model outputs as openly-licensed research data

**Purpose.** Close the release-checklist item "provider terms check" (docs/RELEASE.md)
and supply the outcome sentence that replaces the section-9 TODO in docs/PAPER-V3.md.
The paper releases model *outputs* as public data under CC BY 4.0 across arXiv (paper),
a public GitHub repo (code, derived-data files, coding records), and a Zenodo archive
(raw .eval run logs). Before signing arXiv's submission agreement (which warrants the
author "has the right to include third-party materials" and indemnifies arXiv on it),
the author needs to know what each provider's terms say about owning, publishing, and
open-licensing those outputs.

**What this is / is not.** This is a reading and report of what the terms say, quoting
the operative clauses so the human can decide. It is **not legal advice and issues no
legal conclusion.** The author retains full responsibility for the submission warranty.

**Access date:** 2026-07-15. All three sets of terms were fetched live on this date;
where that supersedes the assistant's training-knowledge cutoff (January 2026), the
live text governs. **Terms can change; this review is accurate only as of the access
date and should be re-checked at submission if that is materially later.**

---

## Scope — what is released, and under which provider regime

| Provider / model | Released output | Where | Assumed access path |
|---|---|---|---|
| Anthropic — Claude Haiku-4.5 | DM narration/interpretation text inside .eval logs | Zenodo (+ quoted snippets in repo docs) | API (Inspect AI harness) → **Commercial Terms** |
| Anthropic — Claude Fable-5 | analysis + substantial paper text | arXiv paper, repo docs | API → **Commercial Terms** |
| z.ai / Zhipu — GLM-5.2 | player prose in .eval logs; derived extractions `tmp/hetero_values.jsonl` (budget mentions) and `tmp/p2final.jsonl` (marker codings) | Zenodo + GitHub repo | **z.ai model-api** → Terms of Use **+ Additional Terms for API Services** |
| OpenAI — GPT-5.6 | marker labels `tmp/hetero_p2_gpt56.jsonl` / `tmp/p2gpt56_final.jsonl`; rater rulings `tmp/sol_rulings.json`; review memo `docs/SOL-REVIEW-2.md` | GitHub repo | chat/Codex tier → **Terms of Use** + Sharing & Publication Policy |

All four `tmp/` files and `docs/SOL-REVIEW-2.md` were confirmed present in the working tree.
The regime assumptions above (API vs. consumer) match the task framing and the eval
harness; they matter most for z.ai (see its section). If any GPT-5.6 output was in fact
obtained via the OpenAI API rather than ChatGPT/Codex, OpenAI's **Business Terms** would
govern that portion instead, with the same output-ownership result (customer owns Output).

Section 8 of the paper ("AI-use and contribution statement") is the attribution/disclosure
instrument evaluated against each provider's conditions below. Its load-bearing sentences:
it declares all four model lines and their roles by name, states "The human author held
every irreversible seam ... and takes full responsibility for all contents," and treats
the authorship pipeline as disclosed provenance.

---

## 1. Anthropic (Claude Haiku-4.5, Claude Fable-5) — Commercial Terms of Service

- **Source:** https://www.anthropic.com/legal/commercial-terms
- **Effective:** June 17, 2025. **Accessed:** 2026-07-15. **Counterparty:** Anthropic, PBC (or Anthropic Ireland for EEA/CH/UK).

**1. Output ownership — user owns.** Section B (Customer Content): *"Anthropic agrees that
Customer (a) retains all rights to its Inputs, and (b) owns its Outputs."* Anthropic further
*"hereby assigns to Customer its right, title and interest (if any) in and to Outputs"* and
*"Anthropic disclaims any rights it receives to the Customer Content."* Clear affirmative
assignment to the user.

**2. Redistribution — permitted; no dataset/open-license bar.** No clause restricts
publishing or open-licensing Outputs. The only use restriction (D.4) is on the *Services*:
the Customer may not *"access the Services to build a competing product or service, including
to train competing AI models or resell the Services."* This binds the Customer's own conduct
(building a competitor); it does not bar publishing owned Outputs as research data, and it is
narrower than z.ai's clause (competing models only — see FLAGS for the CC-BY downstream point).
Note D.3: Outputs should be human-reviewed before sharing — satisfied by the paper's audit
record.

**3. Required conditions — met by section 8.** No mandatory attribution to Anthropic is
imposed. The one relevant condition is no-endorsement: L.2 states *"REFERENCES TO A THIRD
PARTY IN THE OUTPUTS MAY NOT MEAN THEY ENDORSE OR ARE OTHERWISE WORKING WITH ANTHROPIC."*
Publicity (Section G) runs the other way (Anthropic naming the Customer). Section 8 names
Anthropic/Claude factually as tools and implies no endorsement or partnership — condition met.
(The Usage Policy is incorporated by reference; nothing in it bars benign research narration.)

**4. Conflict with arXiv perpetual license + CC BY 4.0 — none for the release itself.**
Because the user owns the Outputs, granting arXiv a non-exclusive perpetual license and
applying CC BY 4.0 are within the user's rights. Residual downstream point is common to all
three providers and collected under FLAGS.

---

## 2. OpenAI (GPT-5.6 marker labels, rater rulings, review memo) — Terms of Use + Sharing & Publication Policy

- **Source (terms):** https://openai.com/policies/terms-of-use (resolves to .../row-terms-of-use/). **Effective:** January 1, 2026. **Accessed:** 2026-07-15. **Counterparty:** OpenAI OpCo, LLC.
- **Source (policy):** https://openai.com/policies/sharing-publication-policy/. **Updated:** November 14, 2022 (still the live, currently-linked policy). **Accessed:** 2026-07-15.

**1. Output ownership — user owns.** Content › Ownership: *"you (a) retain your ownership
rights in Input and (b) own the Output. We hereby assign to you all our right, title, and
interest, if any, in and to Output."* Affirmative assignment, mirroring Anthropic.

**2. Redistribution — permitted, with disclosure.** The "What you cannot do" list restricts
distributing the *Services* (not Output); the Output-specific restrictions are: *"Represent
that Output was human-generated when it was not"* (a disclosure duty, not a bar), *"Use Output
to develop models that compete with OpenAI"* (competing-model restriction — see FLAGS), and
*"Automatically or programmatically extract data or Output"* (reasonably an anti-scraping /
anti-circumvention clause; the released items are the model's own responses saved from normal
use, not data scraped from the Service — worth the human's eye but not a publication bar).
The Sharing & Publication Policy affirmatively *welcomes* the use case: *"we welcome research
publications related to the OpenAI API,"* and for co-authored written content permits
publication provided it is *"attributed to your name or company,"* the *"role of AI ... is
clearly disclosed in a way that no reader could possibly miss,"* and *"a human ... take[s]
ultimate responsibility."*

**3. Required conditions — met by section 8.** Attribution to author ✓ (single-author paper +
section 8). AI-role disclosure "no reader could miss" ✓ (section 8 spells out GPT-5.6/"Sol"
as external reviewer and rater). Human ultimate responsibility ✓ (section 8 verbatim "takes
full responsibility"). No-misrepresentation-as-human ✓ (section 8 discloses AI authorship).
Name/brand use falls under Brand Guidelines; factual naming of "GPT-5.6" in an academic
disclosure is nominative and does not imply endorsement.

**4. Conflict with arXiv perpetual license + CC BY 4.0 — none for the release itself.** User
owns Output; may license. Residual downstream-training point under FLAGS.

---

## 3. z.ai / Zhipu (GLM-5.2 player prose + derived extractions) — Terms of Use + Additional Terms for API Services

- **Source:** https://docs.z.ai/legal-agreement/terms-of-use (identical text also at https://chat.z.ai/legal-agreement/terms-of-service). **Last update:** April 14, 2026. **Accessed:** 2026-07-15. **Counterparty:** JINGSHENG HENGXING TECHNOLOGY PTE. LTD (Singapore). **Governing law:** Singapore; SIAC arbitration.
- This is the least-standardized of the three; findings scrutinized most carefully here. For API users the **Additional Terms for API Services** prevail on any inconsistency, and the eval harness implies API access, so both layers are read together below.

**1. Output ownership — user retains; z.ai disclaims (not an assignment).** Base Terms IV.4:
*"you retain all rights, title, and interest in the Prompts you submit and the Outputs
generated specifically at your request and provided to you as a response to your submitted
Prompts."* Additional Terms 3.a (API): *"We won't claim ownership over your Input and End User
Content."* Net effect: the user owns the outputs. Two nuances vs. Anthropic/OpenAI: (i) z.ai
*disclaims a claim* rather than affirmatively *assigning* rights, and (ii) IV.4 hedges "your
rights in specific Outputs, **if any**" and excludes outputs generated for other users
(standard non-uniqueness carve-out). Practically equivalent to user ownership; the wording is
weaker.

**2. Redistribution — publication of benign outputs is permitted, but open-licensing hits a
real restriction.** No clause bars publishing the player prose as such: the only distribution
bar is III.5.b — *"you may not distribute or publish **inappropriate** Outputs"* — which does
not reach benign game narration. **However**, Additional Terms 1.f.xii restricts what may be
done with the outputs downstream: *"any use of the Z.ai's models, prompts, or model-generated
content for the development, training, labeling, fine-tuning, optimization, iteration, or
similar activities related to external models is strictly prohibited."* This is **broader than
the OpenAI/Anthropic competing-model clauses** — it reaches *any external model*, not only
competitors, and it names *labeling*. See FLAGS for the CC-BY-4.0 tension and the (narrower)
question about the released codings. Favorable counterweight for API use: base Terms IV.7 and
Additional Terms 3.b state z.ai will **not** train on API "End User Content" unless the user
agrees, so the broad content-license/training grant that Section IV.5 imposes on *individual*
(consumer) users does **not** apply to the API path assumed here.

**3. Required conditions — disclosure met; one residual marking step.** z.ai imposes more
explicit conditions than the other two:
- **Disclose z.ai model use** — Additional Terms 1.d: *"You must truthfully and accurately
  disclose the use of models from the Z.ai."* → **met** by section 8 (GLM-5.2 named with roles).
- **No misrepresenting AI as human** — III.5.a bars *"falsely claiming that AI generated
  content ('Outputs') is human-created."* → **met** by section 8.
- **Prominent AI-generated marking** — III.5.d: *"AI-generated Outputs shall be prominently
  marked at reasonable locations to indicate that it is generated by AI."* → **partially
  covered.** Section 8 discloses AI authorship at the paper level; to fully satisfy this,
  the released z.ai-derived artifacts (the .eval logs on Zenodo and `tmp/hetero_values.jsonl` /
  `tmp/p2final.jsonl` in the repo) should carry an explicit "GLM-5.2 / AI-generated" marker,
  e.g. one line in the Zenodo README and the repo data-file header. This is the one concrete
  add beyond what the other two providers require.
- **No endorsement / no partnership** — V.2 bars using z.ai marks to imply association without
  written consent; XII.3: *"These Terms do not create an agency, partnership, joint venture."*
  → **met** by section 8 (factual naming only).

**4. Conflict with arXiv perpetual license + CC BY 4.0.** arXiv's non-exclusive perpetual
license over the *paper* is within the user's rights (user owns the outputs, and only minimal
GLM text appears in the paper body). The genuine tension is **CC BY 4.0 on the Zenodo/GitHub
data**, addressed in FLAGS. No clause forbids the user from *publishing* the data; the tension
is between an unrestricted open license and Additional Terms 1.f.xii.

---

## Overall assessment (as of 2026-07-15)

As read on the access date, **all three providers leave ownership of model outputs with the
user** (Anthropic and OpenAI by affirmative assignment; z.ai by retaining the user's rights
and disclaiming its own), and **none prohibits publishing those outputs as research data.**
Each attaches conditions that are about *disclosure and non-misrepresentation*, not about
withholding publication rights, and the paper's section-8 AI-use statement satisfies the
disclosure/no-endorsement conditions of all three. The single item that is not a clean
"all-clear" is the **open (CC BY 4.0) licensing of the z.ai/GLM-5.2 outputs**, flagged below.
This does not block the release; it is a scope-of-license judgment for the human to make and,
if desired, to paper over with a short dataset notice.

---

## FLAGS

**FLAG 1 (z.ai — the material one). CC BY 4.0 grants a downstream right that z.ai's Additional
Terms withhold from the user.** CC BY 4.0 gives any recipient an irrevocable right to use the
data for *any* purpose, expressly including training AI models. z.ai Additional Terms 1.f.xii
prohibits using its "model-generated content" for "development, training, labeling ... related
to external models." So a no-field-restriction open license authorizes exactly the downstream
use z.ai bars the user from. Precise reading of the exposure:
  - CC BY conveys only the *author's own copyright* in the outputs; it does not, and cannot,
    purport to pass through z.ai-contract permissions the author never received, and a
    downstream party who is not a z.ai user is not bound by z.ai's terms. So open-licensing
    the *copyright* is not itself a breach.
  - The friction is that the author would be *inviting* (via CC BY) a use the author is
    contractually forbidden to perform, over content whose upstream terms restrict that use.
  - The same structural tension exists for Anthropic (D.4) and OpenAI ("Use Output to develop
    models that compete with OpenAI"), but both are limited to *competing* models; **z.ai's is
    broader (any external model) and is the only one that names "labeling."**
  - Options for the human (not chosen here): (a) proceed and rely on the copyright-only scope
    of CC BY, treating the provider use-restrictions as binding only actual z.ai customers;
    (b) add a short notice to the Zenodo/GitHub record that GLM-5.2-derived portions originate
    from z.ai and remain subject to z.ai's terms, which restrict using them to train or label
    external models (a "provider terms may apply to the model-generated portions" carve-out
    alongside the CC BY grant); or (c) ask z.ai for written confirmation. This is a decision to
    make before signing, not one this review makes.

**FLAG 2 (z.ai — minor, likely not triggered). "Labeling ... related to external models" vs.
the released codings.** The repo ships derived codings/extractions over GLM output
(`tmp/p2final.jsonl` marker codings; `tmp/hetero_values.jsonl` budget mentions). 1.f.xii bars
using z.ai content for "labeling ... *related to external models*." On the natural reading the
prohibited labeling is labeling *in service of building/optimizing an external model*, not
labeling *for research analysis of the outputs themselves*, which is what these files are. The
release therefore appears outside the bar, but the clause is broadly worded; noted so the human
can confirm the reading.

**FLAG 3 (z.ai — marking step). Prominent AI-generated marking (III.5.d).** Add an explicit
"GLM-5.2 / AI-generated" marker to the released z.ai-derived artifacts (Zenodo README line +
repo data-file header). Section 8 covers paper-level disclosure; this closes the file-level
marking condition. (Cheap; recommended regardless of FLAG 1's resolution.)

**FLAG 4 (all three — informational). Ownership wording is "as between the parties" and hedged
"if any."** None of the three warrants that outputs are free of third-party IP; each disclaims
that (Anthropic L.2/K.3(e-f); OpenAI similarity clause; z.ai VIII/IV.4 "if any"). This is the
normal AI-output posture and is consistent with the paper already taking full responsibility,
but it is exactly the residual the arXiv warranty ("right to include third-party materials")
sits on top of — the human, not this review, carries that representation.

**FLAG 5 (regime dependency). The favorable z.ai reading assumes API access.** If GLM-5.2 was
used through the consumer chat rather than z.ai/model-api, the individual-user regime applies:
Section IV.5 grants z.ai a broad, sublicensable, perpetual license over User Content and allows
training on it. That license is non-exclusive (so it still would not block the author's CC BY
grant), but it is materially less favorable. Confirm the outputs came via the API. Likewise, if
any GPT-5.6 output came via the OpenAI API, OpenAI Business Terms (not the consumer Terms of
Use read here) govern that portion — same ownership result.

---

## Proposed replacement for the section-9 TODO sentence

The current TODO (docs/PAPER-V3.md, end of section 9) reads: *"Provider terms for publishing
model outputs as research data (Anthropic and z.ai) were reviewed [TODO ...]."* Note it lists
only two providers; the replacement below covers all three now in scope. Worded as a
review-outcome, **not** a legal conclusion. **The human applies this edit himself.**

**Primary (recommended):**

> Provider terms for the model outputs released with this paper — Anthropic Commercial Terms of
> Service, OpenAI Terms of Use with its Sharing & Publication Policy, and the z.ai (JINGSHENG
> HENGXING) Terms of Use with Additional Terms for API Services — were reviewed as of
> 2026-07-15. As read on that date, each leaves ownership of model outputs with the user
> (Anthropic and OpenAI assign output rights to the customer; z.ai retains the user's rights and
> disclaims its own), none bars publishing those outputs as research data, and the disclosure
> and no-misrepresentation conditions the terms attach are satisfied by the AI-use statement in
> section 8. One caveat is recorded for openly licensing the GLM-5.2 (z.ai) portion: z.ai's
> Additional Terms restrict using its model-generated content to train or label external models,
> which a field-of-use-unrestricted CC BY 4.0 grant does not mirror; the released z.ai-derived
> files are additionally marked as AI-generated per z.ai's labeling requirement. This is a
> reading of the terms as of the access date, not legal advice, and the terms may change.

**Shorter alternative (if section 9 needs to stay tight):**

> Terms of the providers whose model outputs are released (Anthropic Commercial Terms, OpenAI
> Terms of Use, z.ai/Zhipu Terms of Use and Additional Terms for API Services) were reviewed as
> of 2026-07-15; each leaves output ownership with the user and permits research redistribution
> subject to AI-use disclosure, which section 8 provides. Exception noted: CC BY 4.0's
> unrestricted downstream grant is broader than z.ai's terms, which bar using its outputs to
> train or label external models; the released z.ai-derived files are marked AI-generated
> accordingly. Reviewed as read on the access date; not legal advice.

(If FLAG 1 option (b) is adopted, append to whichever version: *"; a provider-terms notice
accompanies the model-generated portions of the data record."* If the author prefers not to
assert the marking step until it is done, drop the clause about files being "marked as
AI-generated" and complete FLAG 3 first.)

---

## Sources (all accessed 2026-07-15)

- Anthropic, Commercial Terms of Service (effective 2025-06-17): https://www.anthropic.com/legal/commercial-terms
- OpenAI, Terms of Use (effective 2026-01-01): https://openai.com/policies/terms-of-use
- OpenAI, Sharing & Publication Policy (updated 2022-11-14): https://openai.com/policies/sharing-publication-policy/
- z.ai, Terms of Use + Additional Terms for API Services (last update 2026-04-14): https://docs.z.ai/legal-agreement/terms-of-use (mirror: https://chat.z.ai/legal-agreement/terms-of-service)

*Assistant knowledge cutoff January 2026; the four sources above were fetched live on
2026-07-15 and govern over training knowledge. Terms change; re-verify at submission if
materially later than the access date.*
