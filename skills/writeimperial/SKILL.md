---
name: writeimperial
description: Draft, revise, validate, and optionally archive imperial edicts for the Chinese historical strategy workflow "历史模拟器：崇祯". Use when asked to read simulator archives, analyze a quarterly situation, prepare emperor-to-minister密谈话术, draft four-section edicts, calculate考成/奖惩 targets with quarterly execution correction, or update edict, strategy, intelligence, personnel, and history records.
---

# writeimperial

## Purpose

Use this skill to produce actionable 崇祯 simulator strategy and诏书 from the latest archive. The mandatory loop is:

`读最新档案 -> 提取实际基线 -> 判断季度主轴 -> 分类任务 -> 用 Scale v3.1 计算目标 -> 新制度年度考成/日落检查 -> 起草四段诏书 -> 校验拥塞与红线 -> 等待游戏反馈 -> 更新执行系数`

Never use a universal `+30%` bottom-line and `+50%` upper-target rule. Different task types have different growth rates, execution loss, uplift caps, and quarterly correction limits.

For projects whose result depends on a long quantitative chain—such as imperial estates, agriculture, mining, military industry, trade, banks, waterworks, logistics, relief, or large construction—also use sibling `$writeimperial-causal-ledger`. Calculate a Scale v3.1 target here first, then require that skill to prove the full resource, input, output, cost, distribution, and panel-update chain. A causal-ledger projection remains a policy target until later game feedback confirms it.

## Core Workflow

### 1. Ground in the latest archive

Before drafting, read the newest:

- `朝政纪要`
- previous-quarter edict
- `国家态势` / `game_state`
- `制度规则/关键制度源头/01_长期国策有效清单.md`
- `制度规则/关键制度源头/02_季度试行与非永久政策清单.md`
- `战略方针/README.md` 与相关专项 `战略方略`
- `朝臣档案`
- `密谈记录`
- relevant `data/*.json`
- any user screenshots or pasted game feedback

Use the newest measured actual result as the baseline. Do not use the previous edict target as the new baseline.

If sources conflict:

1. prefer the latest executed `朝政纪要`;
2. retain conflicting values as separate口径;
3. mark evidence quality;
4. do not silently choose the most optimistic value.

### 2. Extract the crisis map

Always consider:

- 军事
- 内政
- 财政
- 外交
- 民变
- 朝堂/派系
- 疫病/灾荒
- 边防
- 军工
- 情报
- 执行能力

Identify:

- 1 decisive quarterly main effort;
- up to 2 hard supports;
- up to 3 maintenance lines.

Do not make all national policies grow sharply in the same quarter.

### 3. Classify every numeric target

Before calculating a target, assign one Scale v3.1 task type:

- `A` mature production
- `B` single military operation
- `C` training, quality, or force reorganization
- `D` pacification, resettlement, and social governance
- `E` engineering, logistics, and storage
- `F` new institution in its first quarter, requiring setup, direct output, and visible system effect
- `G` mature institution
- `H` intelligence and early warning
- `I` diplomacy, trade, and maritime activity
- `J` stock, establishment, fixed headcount, or fixed recurring appropriation
- `K` dual-layer system outcomes: controllable leading signals plus actual satisfaction, support, corruption, authority, prestige, or risk movement
- `L` threshold or zero-tolerance conditions such as supply=`0`, leaks=`0`, lost guns=`0`

Read `references/target_scale_v3.md`, `references/institution_lifecycle_v3_1.md`, and `config/execution_scale_v3.json` whenever a request includes targets, upper assessments, expansion, quarterly correction, new institutions, temporary offices, or comparison with prior results.

### 4. Register new institutions before drafting

Before writing any new-institution edict, first set the annual total target and four quarterly cumulative targets. A new system is never a one-quarter slogan.

Required fields for every new system:

- institution name and version;
- formal supervising office and formal responsible post;
- concurrent temporary role, if any;
- launch quarter and current quarter number;
- annual imperial real target;
- quarter 1, quarter 2 cumulative, quarter 3 cumulative, quarter 4 annual targets;
- annual upper assessment and annual failure line;
- direct-output target and at least one K-class actual-outcome target;
- quarterly actual records and system-outcome records;
- annual assessment quarter and decision;
- 12-quarter sunset date for temporary offices or roles;
- abolish, merge, reduce, or renew disposition plan.

Default annual path: quarter 1 `20%–35%` of annual target, quarter 2 cumulative `45%–60%`, quarter 3 cumulative `70%–85%`, quarter 4 `100%`; annual upper assessment is normally `110%–120%`.

For an F-class first quarter, use the 100-point three-layer assessment:

- setup and execution chain: `35` points;
- direct business output: `40` points;
- system outcome and actual impact: `25` points.

The first quarter must set all three:

- setup goals such as owner, concurrent personnel, authority boundary, books, pilot scope, resources, data return, sunset date, success case, and failure case;
- direct output such as verified numbers checked, red-light districts handled, officials rated, soldiers registered, students arriving, double-source intelligence, or actual maritime receipts;
- at least one actual K-class outcome, such as satisfaction, popular support, authority, prestige, corruption, unrest risk, policy response time, account discrepancy, grain price, pay arrival, intelligence accuracy, or military harassment.

Do not write only `建账`, `设人`, `试行`, `待观察`, `完成建制`, or `开始运行`. If the game has no direct point return, use an equivalent visible result metric; do not fall back to pure setup milestones.

### 5. Keep K-class outcomes visible

K-class clauses must include both:

- `K1` controllable leading signals: pay arrival, relief arrival, grain price, account discrepancy, pensions, wrongful cases, harassment, rework, warning lead time, promotion delivery, or retention;
- `K2` actual system results: soldier, official, peasant, or gentry satisfaction; popular support; imperial authority; national prestige; corruption; unrest risk; epidemic risk; or local stability.

When a new system claims to improve a K-class result, set a first-quarter target and annual target for that result. Ordinary first-quarter expectations are `+1` point for satisfaction/support/authority/prestige, `-1` point for corruption/unrest/risk, or an equivalent visible improvement. Do not use `+5` points as an ordinary quarterly default.

If direct output is completed but K-class outcome does not improve, record: `建制和业务已完成，但制度影响尚未穿透，限下一季度调整传导机制。`

If two consecutive quarters show no K-class improvement, trigger reverse review: reassess mechanism, narrow pilot, change method or owner, and stop the trial if necessary. Do not merely raise the numbers.

### 6. Control temporary institutions with three-year sunset

Long-term state capacity must rest on formal offices: the Grand Secretariat, Six Ministries, Censorate, Court of Judicial Review, Office of Transmission, provincial governors, provincial administrations, surveillance commissions, prefectures and counties, regular military commands, and formal education or military posts.

New systems should normally be led concurrently by existing formal officials, for example `户部尚书兼御前总数局总核`. Do not create a permanent parallel fiscal, military, intelligence, judicial, or personnel office by default.

Every temporary yamen, special committee, bureau, envoy, imperial commissioner, special army, inspection team, school-management body, special treasury office, temporary assessment post, pilot port office, intelligence organization, or new non-regular title defaults to:

- `3` years;
- `12` quarters;
- annual review every `4` quarters;
- final disposition in quarter `12`: abolish, merge into regular office, reduce to a regular suboffice, or renew for three years.

No automatic renewal is allowed. Renewal requires the original mission still existing, last-year bottom line achieved, B-grade or better evidence, no serious overreach/corruption/harassment, no regular office able to take over directly, next-stage targets, and a new 3-year sunset date.

### 7. Separate stock from performance

Do not expand everything merely because a new quarter begins.

Default stock rules:

- troop establishment changes by `0%–2%` per quarter by default and never exceeds the `5%` hard cap;
- fixed recurring rewards remain unchanged by default; ordinary adjustment stays within `±3%` and never exceeds the `±5%` hard cap;
- standing-institution count and long-term baseline appropriations remain stable unless an archive-supported structural need justifies a small change, never above `5%` in one quarter.

Prefer expanding:

- qualified troops;
- training pass rate;
- readiness;
- ammunition availability;
- logistics speed;
- production quality;
- settlement retention;
- intelligence accuracy;
- tax arrival rate.

Do not rely on expanding paper headcount.

### 8. Calculate the six target fields

For every major measurable clause, calculate separately:

1. `actual_baseline`: latest measured actual;
2. `imperial_real_target`: the result the state truly needs;
3. `forecast_execution_coefficient`: expected execution coefficient;
4. `edict_bottom_line`: the stated target after execution-loss uplift;
5. `upper_target`: a limited stretch above the stated bottom line;
6. `failure_line`: the point requiring method, resource, or personnel correction.

The calculation must obey task-specific:

- real growth range;
- forecast execution coefficient;
- uplift cap;
- upper-target cap;
- quarterly coefficient-change cap.

Do not expose the formula in the finished edict unless the user asks. The edict should present clean bottom-line, upper-target, deadline, evidence, reward, failure line, and red lines.

### 9. Use quarterly feedback

After receiving a new `朝政纪要`:

1. compute realized completion by task type;
2. separate external shock, resource failure, coordination failure, target distortion, and personal negligence;
3. update the execution coefficient using recent comparable tasks;
4. limit ordinary coefficient movement to `±0.05` per quarter;
5. allow `±0.08` only after two consecutive results in the same direction;
6. reserve `±0.10` for annual recalibration or a proven structural change;
7. exclude a single extreme event or limit its effect to `±0.03`.

Never let a single disaster quarter permanently reduce capacity, and never let one exceptional overachievement inflate all future targets.

### 10. Lock the quarterly axis

Use:

- 1 decisive main effort;
- 2 hard supports;
- 3 maintenance lines.

Each section-leading sentence must contain a concrete command and owner, because the game AI prioritizes section-leading instructions.

Keep effective prior policies unless the latest feedback shows failure.

### 11. Draft in four fixed sections

Required order:

- `【军事】`
- `【内政】`
- `【外交】`
- `【其他】`

Each major clause should contain:

- owner;
- backup or audit owner;
- region or department;
- concrete action;
- resources;
- deadline;
- bottom-line target;
- upper target;
- evidence requirement;
- reward;
- failure line;
- punishment for red-line conduct;
- fallback when war or disaster makes the main plan impossible.

### 12. Reward first, but distinguish recurring and performance rewards

Preserve recurring reward credibility when affordable.

Do not automatically increase recurring appropriations every quarter. Keep fixed recurring rewards unchanged by default; ordinary adjustments stay within `±3%` and the hard adjustment cap is `±5%`.

Increase performance rewards only when linked to:

- verified military readiness;
- actual arrival of grain or silver;
- qualified production;
- retained settlement;
- effective warning;
- reduced losses;
- clean evidence.

### 13. Validate before finalizing

Check:

- four-section structure;
- `钦此。`;
- Arabic digits;
- 5+ digit quantities expressed naturally with `万`;
- no universal `+30%/+50%` target inflation;
- all six target fields are separately determined for each major metric;
- no more than 1 main effort, 2 hard supports, 3 maintenance lines;
- no troop-establishment target above the `0%–2%` default band without explicit justification; neither the bottom line nor upper target may exceed the `5%` hard cap after combining all adjustments;
- no fixed recurring reward bottom line or upper target beyond the combined `±5%` hard cap;
- no stock target inflated like a production target;
- no satisfaction/corruption target written as if it were direct production;
- every new institution has an annual target, four-quarter cumulative path, current-quarter number, direct output, K-class outcome target, annual assessment quarter, and quarterly records;
- a first-quarter new institution has visible effect and normally reaches `20%–35%` of the annual target, never only setup milestones;
- K-class goals include bottom line, upper assessment, and annual target for actual system outcomes when the policy claims such outcomes;
- a new institution with two consecutive quarters and no K-class improvement triggers reverse review;
- every temporary post names the formal office it depends on and a formal official holding it concurrently;
- every temporary institution or temporary post has a 12-quarter sunset date and annual review every 4 quarters;
- quarter 12 disposition is abolish, merge, reduce, or renew, and never automatic survival;
- later edicts citing an existing system continue annual progress records instead of treating it as a one-off policy;
- no impossible intelligence accuracy jump;
- no threshold condition numerically “raised” above zero;
- no conflict with fiscal, military, or institutional red lines.

If writing JSON, parse every touched JSON file.

### 14. Archive only with explicit authorization

You may suggest updates, but do not edit the archive unless the user explicitly authorizes writing.

Never claim game actions were executed. State only that files were drafted or local archives were updated.

## Target Output Rules

For direct edict requests:

1. output the finished edict first unless analysis was requested;
2. keep internal Scale calculations out of the formal text;
3. after the edict, optionally provide a compact target-calculation note.

For analysis or参谋 requests, use:

- 档案依据
- 局势判断
- 季度主轴
- Scale分类
- 目标计算
- 风险与败案
- 推荐方案
- 诏书草案
- 档案更新建议

## References

- Read `references/edict_rules.md` for formal structure and clause validation.
- Read `references/target_scale_v3.md` for all target calculations and quarterly updates.
- Read `references/institution_lifecycle_v3_1.md` for new-institution first-quarter effect, annual assessment, K-class outcomes, and temporary-office sunset rules.
- Read `config/execution_scale_v3.json` for machine-readable defaults and caps.
- Use `templates/quarterly_scale_feedback.json` when recording quarterly Scale feedback.
- Read `tests/scale_examples.md` when checking whether a target proposal obeys Scale v3.1.
- Read `references/archive_map.md` when deciding which project files to inspect or update.
- Read `references/style_examples.md` for compact clause style.

## Output Defaults

- Finished edicts use the established four-section form.
- Target calculations use the latest actual baseline, not the previous target.
- Force size, fixed rewards, and standing institutions remain broadly stable unless explicitly justified.
- Quality, readiness, production, logistics, retention, and verified outcomes may expand within Scale v3.1 limits.
- For archive writes, summarize changed files, coefficient updates, and validation results.
