# Edict Rules

## Required Structure

Every formal edict uses this frame:

```markdown
奉天承运皇帝，诏曰：

【军事】
命某某……。
1. ...
2. ...

【内政】
命某某……。
1. ...

【外交】
命某某……。
1. ...

【其他】
命某某……。
1. ...

钦此。
```

Each section's first line is the concrete core command and must name the principal owner and action.

## Quarterly Workload Limit

A normal quarterly edict may contain:

- `1` decisive main effort;
- at most `2` hard supports;
- at most `3` maintenance lines.

A national emergency mobilization may exceed this only when the archive and user explicitly require it. Extra projects receive a lower execution-focus coefficient.

## Clause Checklist

Each major clause should specify:

- current actual baseline;
- task type from Scale v3;
- execution owner;
- backup, audit, or successor;
- department or region;
- concrete action;
- money, grain, troops, tools, or materials;
- deadline;
- stated bottom-line target;
- upper target;
- failure line;
- evidence requirement;
- reward for verified completion;
- punishment for fraud, delay, embezzlement, harassment, leaks, lost guns, or collaboration;
- fallback plan when war, disaster, or resource failure prevents the main plan.

The finished formal edict does not need to display internal formulas.

## Numeric Style

- Use Arabic digits: `5万两`, `2.5万人`, `80处`, `30日`, `70`, `35`.
- For 5+ digit quantities, prefer `万`.
- Institutions may keep established Chinese-number names such as `九品` and `四权互核`.
- Use percentage points for rate or score changes when appropriate; do not confuse them with percentage growth.

## Mandatory Target Rules

### 1. Baseline

- Use the latest measured actual result.
- Never use the previous target as the new baseline.
- If the actual value is uncertain, show a range or evidence level before calculating.
- If two current sources conflict, do not silently choose the larger value.

### 2. No universal target uplift

The former universal rule of bottom-line `+30%` and upper target `+50%` is prohibited.

Targets must use `references/target_scale_v3.md`.

### 3. Four target layers

Internally calculate:

- `actual_baseline`
- `imperial_real_target`
- `edict_bottom_line`
- `upper_target`
- `failure_line`

The edict normally presents the bottom line, upper target, failure line, evidence, and reward.

### 4. Stock and establishment

For troop establishment, fixed recurring rewards, standing institutions, and similar stock indicators:

- default quarterly change: `0%–3%`;
- ordinary cap: `5%`;
- emergency cap: `10%` with explicit resources and reasons.

Prefer improving readiness, qualified strength, morale process indicators, logistics, equipment availability, and training pass rate.

### 5. Quality and performance

Quality, production, logistics, retention, and verified results may grow according to task type.

Do not use percentage growth when:

- the baseline is near zero;
- the metric is a score or rate;
- the metric is a zero-tolerance threshold;
- the metric is a one-time milestone.

Use absolute points, fixed quantities, or milestones instead.

### 6. Upper target

Upper targets are limited stretches, not another uncontrolled `+50%`.

Typical upper stretch above stated bottom line:

- mature production: `8%–12%`, cap `15%`;
- military operation: `10%–15%`, cap `20%`;
- training/quality: `5%–10%`, cap `12%`;
- social governance: `10%–15%`, cap `20%`;
- engineering/logistics: `10%–15%`, cap `20%`;
- mature institution: `5%–10%`, cap `15%`;
- intelligence accuracy: `+1–2` percentage points, cap `+3`;
- trade and maritime: `10%–15%`, cap `20%`;
- stock/establishment: `0%–2%`, cap `3%`;
- new institution: one additional verified milestone, not a large output percentage.

### 7. System outcomes

Do not directly command:

- satisfaction `+5`;
- popular support `+5`;
- corruption `-5`;
- authority `+5`;

as if these were factory outputs.

Instead target controllable leading indicators:

- pay arrival;
- relief arrival;
- grain price;
- military harassment;
- audit discrepancy;
- wrongful cases;
- promotion delivery;
- casualty and pension handling.

The game may then calculate satisfaction, support, corruption, and authority.

### 8. Threshold conditions

For conditions such as:

- rebel supply=`0`;
- leaks=`0`;
- lost guns=`0`;
- core forts lost=`0`;

do not “raise” zero. Keep the threshold and increase resilience or verification:

- dual-source checks;
- continuous days maintained;
- backup route;
- recovery time;
- number of independent audits.

## Quarterly Coefficient Update

After game feedback, calculate a comparable realization ratio and classify causes.

Default update:

```text
new_coefficient =
    old_coefficient × 0.70
  + recent_comparable_median × 0.30
```

Limits:

- ordinary quarterly coefficient movement: `±0.05`;
- after two consecutive same-direction results: `±0.08`;
- annual recalibration or proven structural change: `±0.10`;
- extreme war, plague, flood, or contradictory data may be excluded from the rolling sample.

Do not punish an official for target distortion caused primarily by the edict itself.

## Target-Growth Update

Quarterly real-target growth is separate from execution-loss uplift.

Use the latest actual and completion band:

| Result against expected real outcome | Next-quarter rule |
|---|---|
| `≥110%` | use upper half of category growth range |
| `95%–109%` | use normal category growth |
| `80%–94%` | use lower half or maintain |
| `60%–79%` | pause growth; repair method/resources |
| `<60%` | do not inflate; use fallback, sandbox, or change owner/method |

A missed quarter does not automatically reduce the long-term strategic objective, but the next quarterly target must not be inflated merely to look ambitious.

## Disaster and War

When disaster, flood, plague, or war makes ordinary punishment unfair:

- classify external shock;
- preserve accountability for concealment, embezzlement, or reckless command;
- use the fallback plan;
- write `免罚但限期补效` only when the failure was genuinely outside the official's control.

## Forbidden Empty Phrases

Do not write:

- 妥善安抚灾民
- 加强边防
- 整顿吏治
- 恢复财政
- 稳定民心

Replace them with concrete commands, resources, deadlines, targets, evidence, and failure lines.

## Strategic Red Lines

Avoid unless the user explicitly overrides and archives support it:

- 加派民田正税
- 主动与后金决战
- 撤销或擅并东江
- 全面清丈江南
- 高阻力宗室大改
- 低威望时全国性激进改革
- 让情报军掌刑名、征税、调兵、抄家、刑讯
- 以扩大纸面兵额代替提升战力
- 用新券偿还旧券
- 以未核实数据大规模问罪

## Section Guidance

### 军事

Use for剿抚、边防、换防、清野、东江、新军、火器、犒军. Tie military action to logistics, readiness, morale credibility, and preservation of the main force.

### 内政

Use for relief, agriculture, seed, storage, water, epidemic control, revenue, official rewards, and pensions. Do not move protected relief funds into factories or frontier projects without explicit authority.

### 外交

Use for Mongol trade, Korea and Dongjiang, maritime trade, prohibited exports, Zheng maritime forces, and overseas technical acquisition. Prefer performance payment and diversification over uncontrolled spending.

### 其他

Use for execution Scale, audit, nine-grade assessment, intelligence boundaries, legal process, succession, data verification, policy sandbox, and archival feedback.
