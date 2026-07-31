---
name: writeimperial
description: Draft, revise, validate, and optionally archive imperial edicts for the Chinese historical strategy workflow "历史模拟器：崇祯". Use when asked to read simulator archives, analyze a quarterly situation, prepare emperor-to-minister密谈话术, draft four-section edicts, calculate考成/奖惩 targets with quarterly execution correction, or update edict, strategy, intelligence, personnel, and history records.
---

# writeimperial

## Purpose

Use this skill to produce actionable 崇祯 simulator strategy and诏书 from the latest archive. The mandatory loop is:

`读最新档案 -> 提取实际基线 -> 判断季度主轴 -> 分类任务 -> 用 Scale v3 计算目标 -> 起草四段诏书 -> 校验拥塞与红线 -> 等待游戏反馈 -> 更新执行系数`

Never use a universal `+30%` bottom-line and `+50%` upper-target rule. Different task types have different growth rates, execution loss, uplift caps, and quarterly correction limits.

## Core Workflow

### 1. Ground in the latest archive

Before drafting, read the newest:

- `朝政纪要`
- previous-quarter edict
- `国家态势` / `game_state`
- `国策路线`
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

Before calculating a target, assign one Scale v3 task type:

- `A` mature production
- `B` single military operation
- `C` training, quality, or force reorganization
- `D` pacification, resettlement, and social governance
- `E` engineering, logistics, and storage
- `F` new institution in its first quarter
- `G` mature institution
- `H` intelligence and early warning
- `I` diplomacy, trade, and maritime activity
- `J` stock, establishment, fixed headcount, or fixed recurring appropriation
- `K` system outcomes such as satisfaction, morale, popular support, corruption, or authority
- `L` threshold or zero-tolerance conditions such as supply=`0`, leaks=`0`, lost guns=`0`

Read `references/target_scale_v3.md` and `config/execution_scale_v3.json` whenever a request includes targets, upper assessments, expansion, quarterly correction, or comparison with prior results.

### 4. Separate stock from performance

Do not expand everything merely because a new quarter begins.

Default stock rules:

- total troop establishment, fixed rewards, and standing institutions: `0%–3%` quarterly change;
- ordinary hard cap: `5%`;
- emergency cap: `10%` only with explicit resources and strategic need.

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

### 5. Calculate the four target layers

For every major measurable clause, calculate internally:

1. `actual_baseline`: latest measured actual;
2. `imperial_real_target`: the result the state truly needs;
3. `edict_bottom_line`: the stated target after execution-loss uplift;
4. `upper_target`: a limited stretch above the stated bottom line;
5. `failure_line`: the point requiring method, resource, or personnel correction.

The calculation must obey task-specific:

- real growth range;
- forecast execution coefficient;
- uplift cap;
- upper-target cap;
- quarterly coefficient-change cap.

Do not expose the formula in the finished edict unless the user asks. The edict should present clean bottom-line, upper-target, deadline, evidence, reward, failure line, and red lines.

### 6. Use quarterly feedback

After receiving a new `朝政纪要`:

1. compute realized completion by task type;
2. separate external shock, resource failure, coordination failure, target distortion, and personal negligence;
3. update the execution coefficient using recent comparable tasks;
4. limit ordinary coefficient movement to `±0.05` per quarter;
5. allow `±0.08` only after two consecutive results in the same direction;
6. reserve `±0.10` for annual recalibration or a proven structural change.

Never let a single disaster quarter permanently reduce capacity, and never let one exceptional overachievement inflate all future targets.

### 7. Lock the quarterly axis

Use:

- 1 decisive main effort;
- 2 hard supports;
- 3 maintenance lines.

Each section-leading sentence must contain a concrete command and owner, because the game AI prioritizes section-leading instructions.

Keep effective prior policies unless the latest feedback shows failure.

### 8. Draft in four fixed sections

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

### 9. Reward first, but distinguish recurring and performance rewards

Preserve recurring reward credibility when affordable.

Do not automatically increase recurring appropriations every quarter. Default recurring appropriation change is `0%`; ordinary adjustment cap is `±5%`.

Increase performance rewards only when linked to:

- verified military readiness;
- actual arrival of grain or silver;
- qualified production;
- retained settlement;
- effective warning;
- reduced losses;
- clean evidence.

### 10. Validate before finalizing

Check:

- four-section structure;
- `钦此。`;
- Arabic digits;
- 5+ digit quantities expressed naturally with `万`;
- no universal `+30%/+50%` target inflation;
- no more than 1 main effort, 2 hard supports, 3 maintenance lines;
- no stock target inflated like a production target;
- no satisfaction/corruption target written as if it were direct production;
- no impossible intelligence accuracy jump;
- no threshold condition numerically “raised” above zero;
- no conflict with fiscal, military, or institutional red lines.

If writing JSON, parse every touched JSON file.

### 11. Archive only with explicit authorization

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
- Read `config/execution_scale_v3.json` for machine-readable defaults and caps.
- Read `references/archive_map.md` when deciding which project files to inspect or update.
- Read `references/style_examples.md` for compact clause style.

## Output Defaults

- Finished edicts use the established four-section form.
- Target calculations use the latest actual baseline, not the previous target.
- Force size and recurring appropriations remain broadly stable unless explicitly justified.
- Quality, readiness, production, logistics, retention, and verified outcomes may expand within Scale v3 limits.
- For archive writes, summarize changed files, coefficient updates, and validation results.
