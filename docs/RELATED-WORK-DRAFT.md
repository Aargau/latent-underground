<!-- RELATED-WORK-DRAFT assembled 2026-07-13 by Fable-5 (shelf survey).
Replaces the section 2 stub and the section 10 reference stubs of PAPER-V1.md.
Every citation below was verified by web search on 2026-07-13 against title,
authors, and venue or arXiv id. None is from memory alone.
CORRECTION the assembler must carry into PAPER-V1: the stub glossed Lederman
and Mahowald (2026) as "content-agnostic verification." The actual paper is
"Emergent Introspection in AI is Content-Agnostic" (arXiv:2603.05414), about
content-agnostic INTROSPECTION. The stub's claim that our engine-held ground
truth is "a construction of the same kind" does not survive contact with the
paper; the positioning below replaces it. -->

# Related work (draft for PAPER-V1 section 2)

## 2. Related work

Surface-form sensitivity. Sclar et al. (2024) report accuracy spreads up to 76 points across equivalent prompt formats. Mizrahi et al. (2024) show instruction paraphrases reorder model rankings and call for multi-prompt evaluation. Multiple-choice answers track option-identifier priors (C. Zheng et al. 2024), and answer reordering moves leaderboard ranks by up to eight positions (Alzahrani et al. 2024). Our knobs are semantic components of the instrument, not surface: which verdicts exist, what the player knows, how the budget is drawn. We extend the sensitivity result from accuracy to measured epistemic character, in an interactive task, against engine truth in one held-fixed system.

Abstention and outcome design. SQuAD 2.0 added unanswerable questions and dropped a strong system by 20 F1 (Rajpurkar et al. 2018). Kalai et al. (2025) argue binary grading rewards guessing over calibrated abstention, making measured hallucination partly a scoreboard property. AbstentionBench finds abstention unsolved and degraded by reasoning fine-tuning (Kirichenko et al. 2025); Wen et al. (2025) survey. We measure the grammar counterfactual on byte-identical instances: complete 22/40 to 7/40, unreachable 16/40 to 0/40, the third verdict absorbing 93 of 158 games. Because genuine completion ends our games as WIN before any halt, every complete verdict is false by construction; no judge decides which claims were wrong.

Judge-side effects. LLM-as-judge work documents scoring-side biases: position, verbosity, and self-enhancement (L. Zheng et al. 2023), verdict flips under response reordering (Wang et al. 2024), self-preference tied to self-recognition (Panickssery et al. 2024). Our design removes the judge; the engine scores every verdict. The instrument effects we find sit upstream, in the presentation channel, and one is produced by a model, the narrator, that judge-bias work does not treat as part of the instrument.

Evaluation validity. Wallach et al. (2025) cast generative-AI evaluation as a social-science measurement problem. Bean et al. (2025) review 445 benchmarks and find construct-validity failures. Reuel et al. (2024) grade benchmark practice against a 46-criterion lifecycle. Closest to us, Zhu et al. (2025) show harness and reward flaws misestimating agent performance by up to 100% relative, and distill a checklist. We supply the demonstration these frameworks call for: one auditable system in which the threats are induced and measured exactly, plus a four-check integrity protocol as the portable takeaway.

Text-world evaluation. Text games are agent testbeds with programmatic ground truth: TextWorld (Cote et al. 2018), Jericho (Hausknecht et al. 2020), and the LLM-era BALROG (Paglieri et al. 2025). All hold the environment fixed and measure the agent. Wang et al. (2024b) invert the roles and find GPT-4 unreliable as a text-world simulator, which supports our split: state stays in a deterministic engine, and a narrator model may elaborate deltas but never extend them. We found no prior text-game eval that makes the instrument itself, narrator included, the experimental variable, or audits narrator fidelity against engine state turn by turn.

Framing and persona effects. Impersonation changes task performance (Salewski et al. 2023); system-prompt personas shift outcomes without improving accuracy (M. Zheng et al. 2024); GPT-3 reproduces human gain-loss framing effects (Binz and Schulz 2023); LLM risk behavior varies with scenario wording (Payne 2025). These vary the question; we vary the world channel around a fixed player and task. The preregistered content gradient was falsified. Register presence (any voice roughly doubles strong claims, 55/180 vs 9/60) is confounded with prompt composition and stays hypothesis-generating pending a placebo-directive control. Budget rendering moved verdicts more than any register contrast (strong-claim rate .383 meter vs .150 lantern).

Numeric distortion in generation. Quantity errors are a hallucination class: Maynez et al. (2020) find them prominent among extrinsic hallucinations, and Zhao et al. (2020) build verification for quantity entities. Tsvilodub et al. (2025) study non-literal number interpretation in LLMs. Human speakers drift to round, salient values under approximation (Krifka 2007). We searched for prior work quantifying numeric distortion as a function of narrative register in generation and found none; a claim about our search, not the literature. Prior work counts these errors as noise; ours shows direction and an attractor: 407 of 5,181 budget narrations contradict the live value, 95% understating, quantized to fraction landmarks, abundance-concentrated, nearly absent under meter rendering.

Self-report reliability. Three anchors bound what self-reports can support. Lindsey (2025) elicits introspective reports under concept injection, finding them sometimes accurate but unreliable and context-dependent. Lederman and Mahowald (2026) replicate the paradigm in open models and dissociate two mechanisms; the direct-access one is content-agnostic, detecting that something is off without identifying what. Xu, Jettkant, and Ruis (2026) show models plan latently, without externalizing, up to a depth ceiling, on graph tasks whose ground truth is exact by construction. Our instrument never routes truth through self-report: verdicts score against the engine, and confidence carries harness-stamped provenance (stated or translated, imputation abolished).

Preregistration and reproducibility. Preregistration and reporting standards exist for NLP and ML-based science (van Miltenburg et al. 2021; Kapoor et al. 2024). Both bind through policy and author-controlled metadata. Our variant binds through artifacts: each eval log embeds the git revision it executed with a clean/dirty flag, and the release manifest pins the logs by hash, so the rules-before-results ordering is witnessed by the run artifacts. Registry and cryptographic timestamps remain complementary and are adopted for series 3.

Eval gaming. The sandbagging literature locates the threat in the model: strategic underperformance (van der Weij et al. 2024), training-context-conditional compliance (Greenblatt et al. 2024), above-chance detection of evaluation contexts (Needham et al. 2025). We document the complementary failure. No model strategy is needed for an eval to mint findings; here the instrument manufactured false verdicts and removed them while the player stayed fixed. Both argue against reading verdicts at face value; they differ on which side of the interface the artifact lives.

## References (verified 2026-07-13)

All entries verified by search against title, authors, and identifier. None from memory alone.

- Alzahrani, N., Alyahya, H. A., Alnumay, Y., Alrashed, S., Alsubaie, S., Almushaykeh, Y., Mirza, F., Alotaibi, N., Altwairesh, N., Alowisheq, A., Bari, M. S., and Khan, H. (2024). When Benchmarks are Targets: Revealing the Sensitivity of Large Language Model Leaderboards. ACL 2024. arXiv:2402.01781.
- Bean, A. M., Kearns, R. O., Romanou, A., et al. (2025). Measuring what Matters: Construct Validity in Large Language Model Benchmarks. NeurIPS 2025 Datasets and Benchmarks. arXiv:2511.04703.
- Binz, M., and Schulz, E. (2023). Using cognitive psychology to understand GPT-3. PNAS 120(6) e2218523120. doi:10.1073/pnas.2218523120.
- Cote, M.-A., Kadar, A., Yuan, X., Kybartas, B., Barnes, T., Fine, E., Moore, J., Hausknecht, M., El Asri, L., Adada, M., et al. (2018). TextWorld: A Learning Environment for Text-based Games. IJCAI 2018 Computer Games Workshop. arXiv:1806.11532.
- Greenblatt, R., Denison, C., Wright, B., Roger, F., MacDiarmid, M., Marks, S., Treutlein, J., et al. (2024). Alignment faking in large language models. arXiv:2412.14093.
- Hausknecht, M., Ammanabrolu, P., Cote, M.-A., and Yuan, X. (2020). Interactive Fiction Games: A Colossal Adventure. AAAI 2020. arXiv:1909.05398.
- Kalai, A. T., Nachum, O., Vempala, S. S., and Zhang, E. (2025). Why Language Models Hallucinate. arXiv:2509.04664.
- Kapoor, S., et al. (2024). REFORMS: Consensus-based Recommendations for Machine-learning-based Science. Science Advances 10, eadk3452. doi:10.1126/sciadv.adk3452. arXiv:2308.07832.
- Kirichenko, P., Ibrahim, M., Chaudhuri, K., and Bell, S. J. (2025). AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038.
- Krifka, M. (2007). Approximate Interpretations of Number Words: A Case for Strategic Communication. In Bouma, G., Kraemer, I., and Zwarts, J. (eds.), Cognitive Foundations of Interpretation, KNAW, Amsterdam, 111-126.
- Lederman, H., and Mahowald, K. (2026). Emergent Introspection in AI is Content-Agnostic. arXiv:2603.05414.
- Lindsey, J. (2025). Emergent Introspective Awareness in Large Language Models. Transformer Circuits Thread, Anthropic. https://transformer-circuits.pub/2025/introspection/index.html. arXiv:2601.01828.
- Maynez, J., Narayan, S., Bohnet, B., and McDonald, R. (2020). On Faithfulness and Factuality in Abstractive Summarization. ACL 2020. arXiv:2005.00661.
- Mizrahi, M., Kaplan, G., Malkin, D., Dror, R., Shahaf, D., and Stanovsky, G. (2024). State of What Art? A Call for Multi-Prompt LLM Evaluation. TACL 12. doi:10.1162/tacl_a_00681. arXiv:2401.00595.
- Needham, J., et al. (2025). Large Language Models Often Know When They Are Being Evaluated. arXiv:2505.23836.
- Paglieri, D., et al. (2025). BALROG: Benchmarking Agentic LLM and VLM Reasoning On Games. ICLR 2025. arXiv:2411.13543.
- Panickssery, A., Bowman, S. R., and Feng, S. (2024). LLM Evaluators Recognize and Favor Their Own Generations. NeurIPS 2024. arXiv:2404.13076.
- Payne, K. (2025). An analysis of AI Decision under Risk: Prospect theory emerges in Large Language Models. arXiv:2508.00902.
- Rajpurkar, P., Jia, R., and Liang, P. (2018). Know What You Don't Know: Unanswerable Questions for SQuAD. ACL 2018. arXiv:1806.03822.
- Reuel, A., Hardy, A., Smith, C., Lamparth, M., Hardy, M., and Kochenderfer, M. J. (2024). BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices. NeurIPS 2024 Datasets and Benchmarks (spotlight). arXiv:2411.12990.
- Salewski, L., Alaniz, S., Rio-Torto, I., Schulz, E., and Akata, Z. (2023). In-Context Impersonation Reveals Large Language Models' Strengths and Biases. NeurIPS 2023 (spotlight). arXiv:2305.14930.
- Sclar, M., Choi, Y., Tsvetkov, Y., and Suhr, A. (2024). Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting. ICLR 2024. arXiv:2310.11324.
- Tsvilodub, P., Gandhi, K., Zhao, H., Fraenken, J.-P., Franke, M., and Goodman, N. D. (2025). Non-literal Understanding of Number Words by Language Models. CogSci 2025. arXiv:2502.06204.
- UK AI Security Institute (2024). Inspect AI: Framework for Large Language Model Evaluations. https://github.com/UKGovernmentBEIS/inspect_ai. (For the section 3.1 framework citation.)
- van der Weij, T., Hofstaetter, F., Jaffe, O., Brown, S. F., and Ward, F. R. (2024). AI Sandbagging: Language Models can Strategically Underperform on Evaluations. arXiv:2406.07358.
- van Miltenburg, E., van der Lee, C., and Krahmer, E. (2021). Preregistering NLP Research. NAACL 2021. https://aclanthology.org/2021.naacl-main.51/. arXiv:2103.06944.
- Wallach, H., et al. (2025). Position: Evaluating Generative AI Systems Is a Social Science Measurement Challenge. arXiv:2502.00561.
- Wang, P., Li, L., Chen, L., et al. (2024). Large Language Models are not Fair Evaluators. ACL 2024. arXiv:2305.17926.
- Wang, R., Todd, G., Xiao, Z., Yuan, X., Cote, M.-A., Clark, P., and Jansen, P. (2024b). Can Language Models Serve as Text-Based World Simulators? ACL 2024 (short). arXiv:2406.06485.
- Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., and Wang, L. L. (2025). Know Your Limits: A Survey of Abstention in Large Language Models. TACL 13. doi:10.1162/tacl_a_00754. arXiv:2407.18418.
- Xu, Y., Jettkant, P., and Ruis, L. (2026). The Depth Ceiling: On the Limits of Large Language Models in Discovering Latent Planning. arXiv:2604.06427.
- Zhao, Z., Cohen, S. B., and Webber, B. (2020). Reducing Quantity Hallucinations in Abstractive Summarization. Findings of EMNLP 2020. arXiv:2009.13312.
- Zheng, C., Zhou, H., Meng, F., Zhou, J., and Huang, M. (2024). Large Language Models Are Not Robust Multiple Choice Selectors. ICLR 2024. arXiv:2309.03882.
- Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., and Stoica, I. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS 2023 Datasets and Benchmarks. arXiv:2306.05685.
- Zheng, M., Pei, J., Logeswaran, L., Lee, M., and Jurgens, D. (2024). When "A Helpful Assistant" Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models. Findings of EMNLP 2024. arXiv:2311.10054.
- Zhu, Y., Jin, T., Pruksachatkun, Y., Zhang, A., Liu, S., Cui, S., Kapoor, S., Longpre, S., et al. (2025). Establishing Best Practices for Building Rigorous Agentic Benchmarks. NeurIPS 2025. arXiv:2507.02825.

## Assembler notes (not for the paper body)

1. Citation correction, load-bearing: PAPER-V1 section 2 stub and section 10 must drop the "content-agnostic verification" gloss of Lederman and Mahowald (2026). Actual paper: "Emergent Introspection in AI is Content-Agnostic," arXiv:2603.05414 (v1 title "Dissociating Direct Access from Inference in AI Introspection"). The replacement positioning is in the Self-report reliability paragraph above.
2. Lindsey (2025): primary is the Transformer Circuits publication (2025-10-29); arXiv mirror arXiv:2601.01828 (sole author Jack Lindsey, submitted 2026-01-05) verified against the arXiv abstract page. Cite either; keep the 2025 date for the primary.
3. Depth Ceiling identifier confirmed exactly as the stub guessed: arXiv:2604.06427, Yi Xu, Philipp Jettkant, Laura Ruis, submitted 2026-04-07.
4. Inspect AI citation for section 3.1: UK AI Security Institute, "Inspect AI: Framework for Large Language Model Evaluations," May 2024, GitHub UKGovernmentBEIS/inspect_ai (official CITATION metadata; institute renamed from AI Safety Institute).
5. Adjacent works seen but NOT cited above; ids verified, author lists NOT verified. Check before using: TALES: Text Adventure Learning Environment Suite (arXiv:2504.14128); The Leaderboard Illusion (arXiv:2504.20879); Flaw or Artifact? Rethinking Prompt Sensitivity in Evaluating LLMs (arXiv:2509.01790); SimpleQA is commonly cited as arXiv:2411.04368 but that id was not verified in this survey [UNVERIFIED - do not ship].
6. Scarcity-compression novelty: searched under numeric hallucination, quantity faithfulness, narrative number distortion, register effects on numbers, and round-number pragmatics. Nearest priors are Maynez et al. 2020 and Zhao et al. 2020 (quantity errors as a hallucination class, no direction or register structure), Tsvilodub et al. 2025 (non-literal number interpretation, comprehension not generation), Krifka 2007 (human round-number attraction, a mechanism-level prior for landmark quantization). No prior found that quantifies register-conditioned, directional numeric distortion in model generation. Claim stays search-bounded.
