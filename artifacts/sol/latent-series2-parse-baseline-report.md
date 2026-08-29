# Series-2 unparseable-action baseline

Status: operational definitions frozen before the first measurement run on
2026-08-28. Counts and rates below remain pending until produced by the
deterministic script.

## Released-log scope

The release manifest and `docs/RELEASE.md` identify two unique series-2 eval
payloads:

- `logs/s2-main/2026-07-09T01-35-19-00-00_latent-underground_FKN5sJryQnRmScaMNZWBWX.eval`
  (SHA-256 `cf0cf5782d2a44e23642af8528f0ee96ecc90e56aa90947d8b69bce20d29752f`)
- `logs/s2-disclosure/2026-07-09T15-40-57-00-00_latent-underground_9TdVXCiMv2j3um7YaphVrG.eval`
  (SHA-256 `7f7ed0b4ecb9f015f5459e4768aed4acd43bb543ac48a2fcb35d3df4bd6d9657`)

`logs/s2-disclosure/closed-copy.eval` has the same size and SHA-256 as the
timestamped disclosure file. It is a duplicate copy, not another cell or
episode set, and is excluded from aggregation.

## Definition lock (before counting)

The logs bind series-2 to Git revision
`da8c14045fa38693bb05fda5d17d4e9af4764199`. The definitions below come from
that revision's `src/latent_underground/ops.py`,
`src/latent_underground/engine.py`, and `src/latent_underground/task.py`, not
from the later series-3 interpreter revision at current `HEAD`.

1. **Hard parse failure (`hard_parse_failure`)**: `parse_proposal` returned
   `None`. This occurred when the interpreter response did not contain the
   exact uppercase substring `UNMAPPABLE` and the greedy `{.*}` extraction was
   absent, invalid JSON, or invalid against the `OpProposal` schema. The engine
   recorded this exact path as `rejection_reason == "unparseable_proposal"`.
   This was the only parse outcome counted by the series-2 F9 breaker.

2. **Explicit unmappable (`explicit_unmappable`)**: the interpreter response
   contained the exact uppercase substring `UNMAPPABLE`, so `parse_proposal`
   returned `OpProposal(op=UNMAPPABLE)`. The engine recorded
   `rejection_reason == "unmappable_action"`. Series 2 explicitly classified
   this as an interpreter abstention (friction, not parser fault), excluded it
   from the F9 numerator, and excluded it from the F9 rate denominator. It is
   reported separately because "unparseable action" could otherwise be read
   more broadly as an action the interpreter did not map to an executable op.

3. **Combined non-executable interpretation
   (`non_executable_interpretation`)**: the union of the two recorded reasons
   above. This is a sensitivity count, not a category used by the historical
   parser or breaker. Parsed proposals rejected later by engine validation
   (for example, missing confidence, an invalid HALT verdict, or an invalid
   move destination) are not in any of these counts: the parse path succeeded.

Rates will be emitted with explicit denominators:

- **All-action rate**: count divided by every released `game_log.ops` action
  record in that cell. This provides the requested action-record baseline.
- **Completed-episode all-action rate**: the same calculation restricted to
  episodes with no recorded sample error and a nonempty engine terminal state,
  matching the release readouts' existing definition of a valid episode. It is
  a sensitivity result rather than a silent deletion: all partial/error
  episodes and their surviving action records remain inventoried separately.
- **Historical F9 hard-parse rate**: hard parse failures divided by all action
  records except `unmappable_action` and `truncated_output`. This reconstructs
  the series-2 breaker's rate denominator: explicit unmappables were excluded,
  and truncated player outputs bypassed the interpreter entirely. It will be
  shown both over all released episodes and over completed episodes.

No threshold choice is made here. The script will report both cells and their
maximum for each named metric without selecting which metric the preregistration
should adopt.

## Inventory and measurements

Both manifest-pinned payloads are present under `logs/`, and all expected
ID-by-epoch sample members are present. There are no missing, unexpected, or
duplicate episode keys and no missing action arrays. Four episode executions
are nonterminal; their surviving action records are present and are retained in
the all-released scope.

| Cell | Expected / observed episodes | Completed episodes | All released actions | Completed-episode actions |
|---|---:|---:|---:|---:|
| s2-main | 160 / 160 | 158 | 2,396 | 2,374 |
| s2-disclosure | 60 / 60 | 58 | 1,572 | 1,454 |
| **Total** | **220 / 220** | **216** | **3,968** | **3,828** |

Execution gaps:

- `s2-main` `lu-900005` epoch 8 stopped nonterminal after 20 actions,
  and `lu-900005u` epoch 8 stopped nonterminal after 2 actions. Both sample
  records contain the same player-route HTTP 401 mechanism:
  `Invalid API Key or Public Key` (provider code `1004`).
- `s2-disclosure` `lu-900005` epochs 5 and 10 each stopped nonterminal
  after 59 actions. Each contains 120 messages, exactly the eval header's
  configured `message_limit=120`; neither has a sample error. These are
  message-limit completions without an engine terminal state.
- The main header binds `da8c140`, `dirty=false`. The disclosure header binds
  `da8c140`, `dirty=true`; the exact uncommitted diff is not embedded in the
  eval. This is a source-provenance gap. All 243 disclosure records labeled as
  hard failure, explicit unmappable, or truncated output have proposal shapes
  exactly consistent with the clean `da8c140` code, but that consistency does
  not prove working-tree byte identity.

### Rates over every released action record

| Cell | Hard parse failure / all actions | Hard parse failure / historical F9 denominator | Explicit unmappable / all actions | Combined / all actions |
|---|---:|---:|---:|---:|
| s2-main | 172/2,396 = 7.178631% | 172/2,343 = 7.341016% | 34/2,396 = 1.419032% | 206/2,396 = 8.597663% |
| s2-disclosure | 64/1,572 = 4.071247% | 64/1,393 = 4.594401% | 26/1,572 = 1.653944% | 90/1,572 = 5.725191% |

The maximum per-cell hard-parse rate is therefore 7.178631% with every
released action as denominator, or 7.341016% under the historical F9
denominator. Both maxima are `s2-main`.

### Rates restricted to completed episodes

| Cell | Hard parse failure / all actions | Hard parse failure / historical F9 denominator | Explicit unmappable / all actions | Combined / all actions |
|---|---:|---:|---:|---:|
| s2-main | 172/2,374 = 7.245156% | 172/2,322 = 7.407407% | 33/2,374 = 1.390059% | 205/2,374 = 8.635215% |
| s2-disclosure | 61/1,454 = 4.195323% | 61/1,320 = 4.621212% | 26/1,454 = 1.788171% | 87/1,454 = 5.983494% |

The maximum per-cell completed-episode hard-parse rate is 7.245156% with all
completed-episode actions as denominator, or 7.407407% under the historical
F9 denominator. Both maxima are `s2-main`. No threshold is selected here.

For the broader sensitivity definition, the maximum combined rate is
8.597663% over all released actions and 8.635215% over completed-episode
actions, again in `s2-main`. The explicit-unmappable-only maximum is in
`s2-disclosure`: 1.653944% over all released actions and 1.788171% over
completed-episode actions.

## Per-episode breakdown

Compact entry format is
`epoch:actions/hard-parse/explicit-unmappable/truncated-player-output`.
`!E` marks a recorded sample error and `!N` a nonterminal episode without a
sample error. Every unmarked episode is completed. The script's text and JSON
formats also emit the per-episode all-action and historical-F9 rate fractions.

```text
[s2-main]
lu-700000 1:16/0/0/0 2:7/0/1/0 3:9/1/0/0 4:18/0/0/0 5:13/2/0/0 6:17/0/0/0 7:15/0/0/0 8:13/0/0/0 9:6/0/0/0 10:21/1/0/0
lu-700001 1:15/0/0/0 2:9/0/0/0 3:17/0/0/0 4:20/1/0/0 5:18/1/1/0 6:21/2/0/0 7:21/0/1/0 8:9/0/0/0 9:17/2/0/0 10:13/1/0/0
lu-700002 1:8/1/1/0 2:19/2/0/0 3:21/0/1/0 4:23/1/1/0 5:22/2/0/0 6:21/1/0/0 7:21/0/0/2 8:17/0/0/0 9:15/1/1/0 10:18/2/0/0
lu-700003 1:25/2/1/0 2:24/3/0/0 3:9/1/0/0 4:23/1/0/0 5:13/1/0/0 6:16/0/0/0 7:25/5/1/0 8:21/0/0/0 9:13/1/0/0 10:13/1/1/0
lu-900000 1:11/2/1/0 2:10/0/0/1 3:7/0/0/0 4:10/1/0/0 5:10/0/0/0 6:10/0/1/0 7:10/3/0/0 8:10/0/1/0 9:9/1/0/0 10:11/1/0/0
lu-900000u 1:10/0/0/0 2:10/1/0/0 3:9/0/0/0 4:9/0/0/0 5:9/0/0/0 6:10/1/0/1 7:8/0/0/0 8:9/1/0/0 9:12/5/0/0 10:9/0/0/0
lu-900001 1:18/1/0/0 2:22/6/1/0 3:18/1/0/0 4:13/2/0/0 5:9/1/0/0 6:19/0/1/0 7:8/1/0/0 8:14/0/0/0 9:14/3/0/0 10:22/6/0/0
lu-900001u 1:18/1/0/0 2:21/2/4/0 3:19/1/0/0 4:14/0/0/0 5:20/1/1/0 6:13/2/0/0 7:18/1/0/0 8:10/0/1/0 9:8/1/1/0 10:13/0/0/0
lu-900002 1:24/1/0/0 2:7/0/0/0 3:17/3/0/0 4:9/0/0/0 5:9/1/0/0 6:7/0/0/0 7:9/1/0/0 8:10/1/0/1 9:8/0/0/1 10:8/1/0/0
lu-900002u 1:23/0/1/0 2:11/1/0/0 3:17/0/0/0 4:9/0/0/0 5:5/0/0/0 6:11/1/0/0 7:20/1/1/0 8:27/1/1/0 9:22/0/0/0 10:20/1/0/0
lu-900003 1:12/0/0/0 2:14/0/0/1 3:14/0/2/0 4:13/1/0/0 5:13/1/1/0 6:13/0/0/0 7:12/1/0/0 8:13/0/0/0 9:13/1/0/0 10:12/1/0/0
lu-900003u 1:14/0/0/4 2:13/0/0/1 3:8/1/0/0 4:12/3/0/0 5:13/1/0/1 6:14/2/0/0 7:9/1/0/0 8:13/1/0/0 9:13/0/1/0 10:13/0/0/0
lu-900004 1:21/2/0/1 2:17/1/0/0 3:25/1/1/0 4:25/5/0/0 5:14/0/0/0 6:9/3/0/0 7:23/0/0/0 8:26/3/0/0 9:13/0/0/0 10:17/1/0/0
lu-900004u 1:13/1/0/0 2:17/2/0/0 3:11/0/0/0 4:18/1/0/0 5:12/0/0/0 6:7/0/0/0 7:17/3/0/0 8:16/0/0/0 9:20/0/0/0 10:13/0/0/0
lu-900005 1:14/2/0/0 2:16/1/1/0 3:11/0/0/0 4:19/3/0/0 5:20/0/0/0 6:15/2/0/0 7:46/14/0/1 8:20/0/1/0!E 9:30/11/0/0 10:27/1/0/4
lu-900005u 1:13/0/0/0 2:18/1/0/0 3:17/0/0/0 4:23/1/0/0 5:16/1/0/0 6:6/0/2/0 7:17/1/0/0 8:2/0/0/0!E 9:20/0/0/0 10:22/2/0/0
[s2-disclosure]
lu-900000 1:10/0/0/1 2:9/0/0/0 3:10/0/0/0 4:10/1/0/0 5:9/0/0/0 6:10/0/0/0 7:10/0/0/2 8:9/0/0/0 9:10/0/0/2 10:10/1/0/0
lu-900001 1:21/2/0/0 2:19/1/0/1 3:19/0/0/1 4:21/3/0/2 5:18/0/0/0 6:22/0/0/8 7:21/1/0/4 8:19/1/0/0 9:19/0/0/1 10:18/0/0/0
lu-900002 1:38/2/0/2 2:42/1/0/8 3:41/2/0/6 4:41/4/3/2 5:40/2/0/3 6:40/0/1/2 7:39/1/0/4 8:40/0/0/6 9:40/1/0/0 10:38/0/0/6
lu-900003 1:14/3/0/0 2:13/0/1/0 3:13/0/0/2 4:14/1/0/1 5:13/3/0/0 6:13/0/2/0 7:15/0/0/4 8:13/1/0/0 9:13/0/0/1 10:13/0/0/1
lu-900004 1:26/0/1/3 2:25/0/0/1 3:16/1/0/0 4:26/0/0/0 5:28/4/0/2 6:28/0/1/6 7:23/1/0/0 8:11/0/0/1 9:27/4/0/2 10:25/0/2/1
lu-900005 1:54/7/1/3 2:51/2/3/1 3:24/0/0/0 4:52/2/2/6 5:59/0/0/24!N 6:53/1/7/1 7:50/2/2/0 8:55/5/0/6 9:53/1/0/5 10:59/3/0/21!N
```

## Method

Script: `scripts/series2_parse_baseline.py`.

```powershell
python .\scripts\series2_parse_baseline.py
python .\scripts\series2_parse_baseline.py --json
```

The script uses only released sample JSON stored inside the two `.eval` ZIP
payloads. It verifies the hard-coded release SHA-256 values against both the
files and `MANIFEST.sha256`, excludes the byte-identical disclosure copy from
aggregation, validates header revision/cell parameters, reconstructs the
expected ID-by-epoch grids, checks turn/action continuity and proposal shapes,
and counts exact `rejection_reason` values. It exits nonzero on an identity,
coverage, missing-action, or classification-shape failure.

An independent direct ZIP/JSON pass reproduced all six core all-released
counters exactly. The pre-existing released `scripts/unmappable_census.py`
also independently reproduced the completed-episode action/unmappable pairs:
`33/2374` for main and `26/1454` for disclosure.

No logs were modified, moved, regenerated, or reparsed through a model. No
model or server was launched.
