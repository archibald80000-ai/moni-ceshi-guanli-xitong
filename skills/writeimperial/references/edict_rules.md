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

Each major clause should specify or internally determine:

- latest actual baseline;
- task type from Scale v3.1;
- imperial real target;
- forecast execution coefficient;
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

For every new institution, new temporary role, or new temporary office, the clause must also determine:

- annual target;
- current quarter number;
- current cumulative target;
- first-quarter direct business output;
- first-quarter K-class system outcome;
- formal supervising office and formal responsible post;
- temporary concurrent role;
- annual assessment time;
- 3-year sunset time;
- abolish, merge, reduce, or renew disposition plan.

Formal edicts may use one common lifecycle clause and then reference it in individual projects. The text must still make clear:

```markdown
本制以1年为初考之期，每季具实效册。
首季除建账设人外，必须取得明确成果。
满1年总考，满3年撤并总验。
临时差遣附属于朝廷正职，不另成永久衙门。
```

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

### 3. Six-field target model

Determine separately:

- `actual_baseline`
- `imperial_real_target`
- `forecast_execution_coefficient`
- `edict_bottom_line`
- `upper_target`
- `failure_line`

Do not merge the real need, forecast coefficient, and stated target into one number. The edict normally presents the bottom line, upper target, failure line, evidence, and reward.

### 4. Stock and establishment

For troop establishment:

- default quarterly change: `0%–2%`;
- hard cap: `5%`;
- no emergency exception may exceed the hard cap.
- both the stated bottom line and upper target must remain within the combined `5%` hard cap from the actual baseline.

For fixed recurring rewards:

- default quarterly change: `0%`;
- ordinary adjustment: within `±3%`;
- hard cap: `±5%`.
- bottom-line and upper-target adjustments combined must remain within `±5%` of the actual baseline.

For standing institutions and long-term baseline appropriations:

- remain stable by default;
- change only for an archive-supported structural need;
- never change by more than `5%` in one quarter.

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
- new institution: three-layer first-quarter assessment: setup `35`, direct output `40`, system outcome `25`; upper assessment is a limited stretch on direct output and K-class effect, not one more empty milestone.

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

## New Institution and Lifecycle Rules

### 1. First-quarter visible effect

F-class new institutions must both stand up and work in the first quarter. Do not write only personnel, ledgers, process, and pilot milestones. The first quarter must include:

- setup and execution chain, including owner, concurrent personnel, authority boundary, ledger, pilot scope, resources, data return, sunset date, success case, and failure case;
- direct business output, such as verified discrepancies, red-light relief cases, official ratings, soldier registrations, school arrivals, double-source intelligence, or actual trade receipts;
- at least one actual K-class system result or equivalent visible outcome.

If the game does not return direct point changes, use equivalent indicators such as response time, account discrepancy, grain price, pay arrival, intelligence accuracy, harassment cases, or relief arrival. Pure setup milestones are not enough.

### 2. Annual assessment path

Every new institution establishes a 1-year assessment cycle at launch:

| Quarter | Annual cumulative target |
|---|---:|
| 1 | 20%–35%, default 25% |
| 2 | 45%–60%, default 50% |
| 3 | 70%–85%, default 75% |
| 4 | 100% |

Annual upper assessment is normally `110%–120%`. Quarter 4 must conclude one of:

- 上考
- 达标
- 基本达标但须整改
- 未达标需更换方法或主官
- 停止试行

The annual review checks actual output, K-class results, cost, harassment, false reporting, duplicate offices, whether the system remains worth keeping, and whether it can be merged into a regular yamen.

### 3. K-class dual layer

K-class rules always include:

- `K1` controllable leading signals: pay, relief, grain price, account discrepancy, pensions, wrongful cases, harassment, rework, warning lead time, promotions, or retention;
- `K2` actual system results: soldier, official, peasant, or gentry satisfaction; popular support; imperial authority; national prestige; corruption; unrest risk; epidemic risk; or local stability.

When a new institution claims to improve a K-class result, the edict must set both first-quarter and annual targets for the actual result. Ordinary first-quarter targets are `+1` to `+2` points for satisfaction/support/authority/prestige, `-1` to `-2` points for corruption/unrest/risk, or an equivalent visible result. `+5` points is exceptional only for major victory, obvious disaster relief, mature structural effects, or explicit court-record support.

If direct output succeeds but K2 does not move, the conclusion is: `建制和业务已完成，但制度影响尚未穿透，限下一季度调整传导机制。` Two consecutive quarters without K2 improvement trigger reverse review instead of automatic target inflation.

### 4. Formal office priority and 3-year sunset

Long-term state capacity must rely on formal posts: 内阁、六部、都察院、大理寺、通政司、地方督抚、布政司、按察司、府县、正式军镇、正式学政和军政官职。

Temporary yamen, special bureaus, envoys, commissioners, inspection teams, school-management bodies, special treasuries, temporary assessment posts, pilot port offices, intelligence organizations, and other non-regular titles default to 3 years and 12 quarters. They should be led concurrently by formal officials, for example:

```yaml
正式官职: "户部尚书"
临时兼领: "御前总数局总核"
```

At setup, record launch quarter, first-year assessment quarter, second-year assessment quarter, 3-year sunset quarter, supervising regular office, concurrent formal post, disposition plan, and archive handoff target. Year 1 and Year 2 reviews check results, K-class targets, overlap, budget growth, disturbance, and whether the regular office can take over. Quarter 12 must decide one of:

- 撤销
- 并入正式衙门
- 缩编为正式衙门下属常设科司
- 续期3年

There is no automatic renewal. Renewal requires a continuing mission, last-year bottom-line completion, B-grade or better evidence, no serious overreach/corruption/harassment, no regular office able to take over directly, next-stage targets, and a new 3-year sunset date.

When a temporary institution ends, formal officials return to their posts, temporary assignments end, temporary staffing cannot become permanent redundancy by default, capable people may enter regular vacancies through Personnel Ministry review, and accounts, funds, archives, and pending matters move to the supervising regular office without destroying responsibility records.

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
- a single extreme war, plague, flood, or contradictory record is excluded by default or limited to `±0.03`.

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

Use for剿抚、边防、换防、清野、东江、新军、火器、犒军. Tie military action to logistics, readiness, morale credibility, and preservation of the main force. Distinguish主帅、中层将官、普通士卒 in奖惩.

### 内政

Use for赈灾、春耕、种子、仓储、水利、疫病、税源、养廉、官僚奖赏、抚恤. Do not挪陕西赈银 into border or factory costs unless explicitly ordered.

### 外交

Use for蒙古互市、朝鲜东江、海贸、禁炮、郑氏水师、西洋工匠. Prefer绩效给付 and diversification over uncontrolled spending.

### 其他

Use for四权互核、三硬七辅、九品考成、执行 Scale、密探、查账、刑部、吏部、归档、派系平衡、数据核验、政策试点. Keep权责 separated: 王承恩掌账不掌刑, 刑部掌刑不掌账, 内阁复核, 司礼监封册.
