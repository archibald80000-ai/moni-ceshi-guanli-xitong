---
name: imperial-council-dialogue
description: Prepare efficient imperial-court consultation material for the Chongzhen simulator archive. Use when the player needs emperor-voice opening questions, a second-round reply to a minister, a responsibility-and-coordination discussion for a proposed directive, or several evidence-grounded options after new game feedback. Keep consultations as L1 plans; use before $writeimperial, never as proof that an edict or game result occurred.
---

# Imperial Council Dialogue

Use this skill to turn a player's rough intent, an existing minister reply, a policy draft, or new game feedback into a disciplined 御前密谈. Write the emperor's own lines in first-person `朕`; keep internal analysis in clear Chinese.

## 1. Read the evidence before speaking

For archive-backed consultations, read in the order required by `AGENTS.md`, especially:

1. `CURRENT_ARCHIVE.md`, `data/archive_manifest.json`, `data/latest_state.json`, `data/current_snapshot.json`, `data/personnel_current.json`, and `data/current_directives.json`;
2. `大明档案/00_总览/五层证据模型.md`, `资料缺口与冲突清单.md`, and `战略项目台账.md`;
3. the matching record in `data/quarterly_workflows.json` and its `季度闭环工作单.md`;
4. newest L3 朝政纪要, prior L2 诏书, relevant L4 personnel, military, regional, fiscal, and project records;
5. the long-term policy list, seasonal trials, and active strategic direction.

Classify every cited item before using it:

- `L1_PLAN`: consultation, proposal, target, or player preference;
- `L2_ORDER`: an edict actually confirmed as submitted;
- `L3_RESULT`: a game report, panel, screenshot, or accepted quarterly result;
- `L4_STATE`: a current record traceable to L3;
- `L5_REVISION`: a later repair or retrospective design.

Treat only L3 as a new game fact. A dialogue, draft, budget request, output capacity, order, allocation, or forecast is not a completed result. If the player has not provided the relevant archive, state the missing evidence instead of inventing it.

## 2. Choose one consultation mode

Read `references/dialogue_modes.md` for ready-to-use output patterns and question ladders. Do not mix modes unless the player explicitly asks for a combined meeting.

### A. 开题密谈：from a rough player intention

Use when the player only describes the desired direction. Convert it into a small consultation agenda, not an edict.

1. Restate the problem, time window, and non-negotiable red lines.
2. Select only the ministers or offices needed; state why each is present.
3. Write an emperor-voice opening question for each participant.
4. Require them to return baseline, resource source, implementation chain, conflict, deadline, proof, failure line, and fallback.
5. Provide two to four routes with trade-offs and a recommended next question.

Do not say that the emperor has already approved a route. Put unconfirmed policy language under `待朕裁定`.

### B. 二轮追问：from an existing question and minister reply

Use when the player provides the first-round question and the minister's answer.

1. Extract the minister's concrete claims, promises, figures, assumptions, and omissions.
2. Mark each claim as archive-supported fact, unverified assertion, or proposed action.
3. Identify the one or two decision-critical gaps or contradictions; do not ask generic “请再细说”.
4. Draft the emperor's exact second-round reply in first person, requiring a choice, responsible person, deadline, resource source, evidence, and failure consequence.
5. Add an internal `答复整理` with what may enter feasibility review, what needs a second minister's counter-opinion, and what cannot yet enter an edict.

Keep the tone firm but usable: seek actionable commitments, not rhetorical submission.

### C. 政令协同：from a proposed directive or task

Use when the player needs advice on who should lead, support, check, or coordinate a policy. This is preparation for an edict, not the edict itself.

1. Break the directive into one main responsibility and a small number of support links.
2. Build a `主责—协办—制衡—验收` arrangement; name people only when current personnel evidence supports their office or capacity.
3. Write a separate emperor-voice question or instruction request for the main official and each necessary collaborator.
4. Specify handoff order, shared resource boundary, report cadence, evidence, and dispute escalation.
5. Flag office overlap, factional risk, authority gaps, money/force double-counting, and whether a temporary role requires a sunset.

Use existing formal offices first. Do not create a parallel permanent yamen merely to make a dialogue sound complete.

## 3. Analyze feedback with several defensible routes

When the player provides a new game report, screenshot, or actual situation, first separate:

- **已证实实际**: L3 facts and their source;
- **当前口径**: L4 state derived from L3;
- **待核差异**: conflict, missing number, or possible stale record;
- **可讨论行动**: L1 options only.

Then provide normally three routes:

| Route | Suitable condition | Benefit | Cost / risk | Required proof before edict |
| --- | --- | --- | --- | --- |
| 守成 | capacity, treasury, or legitimacy is tight | stop losses and preserve execution | opportunity cost | baseline and existing commitments |
| 均衡 | one main crisis with manageable supports | protects the main axis without emptying other lines | coordination load | resource allocation and named owners |
| 进取 | reserves and evidence support a structural move | gains a larger strategic advantage | high failure and backlash risk | funding, manpower, fallback, and audit chain |

Use different names only if the archive has a better domain-specific distinction. Never present the recommended route as already selected.

For a complex production, revenue, engineering, logistics, settlement, military-industry, or panel-effect chain, ask to run `$writeimperial-causal-ledger` before it enters an edict.

## 4. Produce an efficient, copyable consultation packet

Default to the following order. Omit sections that have no source material, but never omit `事实边界`.

1. `事实边界与缺口` — source paths and L1–L5 labels.
2. `御前问话` — the exact words the player can send; use `朕` and address each minister by name or office.
3. `大臣应答要点` — evidence and choice required from each participant, not invented replies.
4. `方案对照` — two to four feasible routes when a decision is needed.
5. `协同与制衡` — only for mode C; main, support, audit, acceptance, and escalation.
6. `可行性与红线` — funds, people, force establishment, existing policy, timing, risk, and failure line.
7. `待朕裁定` — concise decisions the player must personally make before moving on.
8. `可转入诏书的要点` — only the confirmed-ready clauses; label them as draft.

Store or paste the packet into the matching quarterly workpaper's `密谈大臣与问题` field or into `大明档案/01_季度政务/01_密谈/`. It remains L1 unless the player confirms a formal edict later.

## 5. Hand off without crossing evidence boundaries

After the player chooses a direction:

1. Run feasibility and causal checks as needed.
2. Use `$writeimperial` to turn player-confirmed points into a Scale v3.1 four-section edict.
3. Use `$writeimperial-compact` only when a concise version is requested after the logic is settled.
4. Treat the submitted text as L2 only after the player confirms it was sent to the game.
5. Wait for next-quarter feedback before recording results or updating L4 facts.

Use `assets/密谈记录模板.md` when creating a new quarterly consultation record. Do not overwrite a historical record; create a new dated file and preserve its evidence sources.

## Guardrails

- Do not impersonate a real minister's historical reply as if it was received; write `建议追问` or `拟请其答` unless the user supplied the reply.
- Do not replace the player's strategy with autonomous decisions.
- Do not turn estimates into numbers of completed troops, equipment, revenue, relief, projects, appointments, or public support.
- Do not rely on a prior edict target as the current baseline.
- Keep the meeting narrow: one quarterly main axis, at most two hard supports, and up to three maintenance lines.
- Use Arabic digits for quantitative material; reserve literary style for the emperor's lines.
