---
name: writeimperial-compact
description: Write compact, result-forward imperial edicts and policy directives for the 崇祯 historical simulator. Use when the user asks for a four-section quarterly edict whose sections contain several short directives, or asks for 300–500 character policy paragraphs with world state, causal reasoning, execution, risk boundaries, simulated gains, and final targets.
---

# writeimperial-compact

## Purpose

This skill distinguishes two different writing units:

- **诏书**：一个季度的完整御令文件，固定由 `【军事】【内政】【外交】【其他】` 四大部分组成。
- **政令**：诏书某一部分内部的执行单元，一条政令只处理一件事，通常为一个编号段落。

An edict is not a pile of independent mini-edicts. The full document uses `奉天承运皇帝，诏曰：` once at the beginning and `钦此。` once at the end. Individual directives inside the four sections do not repeat either formula.

## Mandatory hierarchy

```text
完整诏书
├─ 总序：最新世界状态、上季结果、当季主轴
├─ 【军事】
│  ├─ 政令1
│  ├─ 政令2
│  └─ 政令3
├─ 【内政】
│  ├─ 政令1
│  ├─ 政令2
│  └─ 政令3
├─ 【外交】
│  ├─ 政令1
│  └─ 政令2
├─ 【其他】
│  ├─ 政令1
│  └─ 政令2
└─ 钦此。
```

The four sections are containers. Each container may hold several directives. A directive is compact; the entire section still obeys the project limit of fewer than 2000 Chinese characters.

## Edict-level structure

### 1. Opening world description

The preamble describes the world once for the whole edict:

- latest executed quarter;
- 3–6 decisive actual facts;
- what succeeded last quarter;
- what remains unfinished;
- the current national advantages or crises;
- the one decisive main effort, two hard supports, and up to three maintenance lines.

Do not repeat the full world background in every directive. Each directive only recalls the one fact directly relevant to its policy.

### 2. Four fixed sections

Required order:

1. `【军事】`
2. `【内政】`
3. `【外交】`
4. `【其他】`

Each section begins with one short owner-and-axis sentence, then contains numbered directives.

Example:

`【军事】命孙承宗总裁军政、卢象升总领实编，今季只办三军实装、军官考成与辽东短袭三事。`

### 3. Final total verification

The final directive in `【其他】` normally sets:

- unified evidence;
- panel refresh requirements;
- no double counting;
- reward and punishment;
- what happens below 80% or 60%;
- the rule that planned or simulated results are not executed facts.

## Directive-level rhythm

Every directive uses this causal chain:

`相关世界状态 → 症结与因果 → 皇帝命令与执行链 → 风险边界 → 即时推演收益 → 季末最终目标`

This chain belongs inside one directive paragraph, not across the whole edict.

## Directive size

- Normal length: `280–450` Chinese characters.
- Hard maximum: `500` Chinese characters unless the user explicitly permits more.
- One directive handles one policy only.
- A section may contain 2–5 directives, provided the section total remains below 2000 characters.
- A quarterly edict may therefore contain roughly 8–14 compact directives across four sections.

## Six-part directive model

### 1. Relevant world state

Open with only the local facts needed for this directive, usually 1–2 clauses.

Example:

`今三军火铳、轻炮库存充足，然各军团到营签收未全，库存尚未转化为战力。`

Do not repeat the entire national situation already stated in the edict preamble.

### 2. Causal judgment

Explain one clear mechanism:

- equipment reaches named units → readiness rises;
- waterworks reach fields → yield and household surplus rise;
- ports reduce clearance time → cargo and tax receipts rise;
- officer training fills commands → disorder and mobilization delay fall;
- horse raids reduce Qing mobility → defensive troop diversion rises.

### 3. Imperial command and execution chain

The same paragraph must name:

- principal owner;
- supporting or audit owner;
- exact action;
- resources;
- deadline.

### 4. Risk boundary

The boundary must alter execution:

- intelligence below B grade → cancel attack;
- casualties reach 8% → withdraw;
- sales below 80% → freeze expansion;
- grain prices rise above 5% → halt government procurement;
- equipment panel not refreshed → task fails.

### 5. Immediate simulated result

The directive must directly state the logically expected result, normally 3–6 linked outputs:

- direct gains or destruction;
- system capacity change;
- panel value change;
- strategic option created for next quarter.

Use `推演可得`、`据现有基线可使` or another explicit planning phrase when the result is not yet executed.

### 6. Final target

End the paragraph with the required end-of-quarter state and evidence.

Example:

`季末以九团军械可用率99%、五日可调增加4000人及总库存、军团签收两表同日更新为验收，缺一项即判失败。`

## Difference between directive, section, and edict

| Unit | Function | Typical size | Opening/ending |
|---|---|---:|---|
| 政令 | Execute one policy and predict its result | 280–450 characters | No `奉天承运`; no `钦此` |
| 部分 | Group several related directives | Under 2000 characters | Uses section title and one owner sentence |
| 诏书 | Quarterly national command | Four fixed sections | One `奉天承运皇帝，诏曰` and one `钦此。` |

## Source template adaptation rule

When a reference source presents many separate texts each beginning with `奉天承运皇帝，诏曰`, treat them as examples of **standalone edicts**. Extract their internal strengths:

- state the crisis first;
- name money, grain, troops, people, and deadlines;
- explain the operating process;
- directly state the resulting suppression, revenue, production, satisfaction, experience, or risk change;
- end with reporting and supervision.

For this project, embed that rhythm inside individual directives under the four-section quarterly edict. Do not repeat a full imperial formula for every directive.

## Edict drafting template

```markdown
# 崇祯X年X《诏书标题》

奉天承运皇帝，诏曰：

[总序：最新世界状态、上一季结果、剩余问题、当季主轴。]

【军事】
[本部分主责与主轴。]

1. [军事政令：状态—因果—执行—边界—推演收益—最终目标。]

2. [军事政令。]

3. [军事政令。]

【内政】
[本部分主责与主轴。]

1. [内政政令。]

2. [内政政令。]

【外交】
[本部分主责与主轴。]

1. [外交政令。]

2. [外交政令。]

【其他】
[本部分主责与总考。]

1. [人事、制度或考成政令。]

2. [面板、证据、奖惩与失败规则。]

钦此。
```

## Compact directive fillable template

`今[该事项最新实际状态]，症结在[因果机制]。着[主责]会[协同/核验]，以[资源]于[期限]内完成[动作]；若[红线]，即[撤回/冻结/换法/追责]。依[实际基线]推演，可取得[直接成果]，使[能力或面板]变化[数字或窄范围]，代价为[银、伤亡、时间或机会成本]。季末以[最终状态]及[证据/面板]为验收，未更新或无凭证按失败。`

## Result ledger inside each directive

When applicable, include four layers without double counting:

1. **直接结果**：得马、得械、税银、销量、亩数、毕业人数、完工数；
2. **制度结果**：调度速度、到账率、损耗率、训练率、预警提前量；
3. **面板结果**：经验、士气、补给、收入、民心、威望、风险；
4. **战略结果**：下一季度能够扩大的行动或制度能力。

Inventory transfer is not new production. Internal allocation is not market sales. Capacity is not actual output. Funds authorized are not funds spent.

## Numerical discipline

Use the latest executed actual baseline and Scale v3.1 from the main `writeimperial` skill.

- mature production normally improves `5%–12%` per quarter;
- a single military action normally improves comparable results `5%–15%` and must have casualty/withdrawal limits;
- training and readiness normally improve `+3–6` points or `+3–5` percentage points;
- ordinary satisfaction, authority, prestige, corruption, and risk movement is usually `±1–2` points unless a major funded event supports more;
- exact values require a baseline, mechanism, resource, and execution coefficient;
- unsupported outcomes use narrow ranges and are labeled as推演.

## Example of one complete section

```markdown
【军事】命孙承宗总裁军政、卢象升总领实编，本部分只办军械到团、武备军官与辽东短袭三事。

1. 今火铳、轻炮库存充足而九团签收未全，症结在库存未转为可用战力。着徐霞客会武库司按团逐号拨付，30日完成火铳28800支、轻炮540门、燧发枪9000支到营；军械可用低于99%的军团暂停上等考成。依秋末兵力推演，火器覆盖率可升8至12个百分点，五日可调增加3000至5000人，训练通过率提高2点，维修积压下降20%，仅新增运输、弹药与修械成本。季末以总库存与九团签收面板同日刷新为验收，缺一团即全项失败。

2. 今武备学堂已有1170人到学，基层军官仍有实职空缺。着兵部完成笔试、实操与带队考核，90日毕业1040人、试任936人；带队不合格者降为2级，不得凭文凭占职。推演可补百总与把总900余缺，使一人兼两缺降至0，军团号令传达时间下降10%，训练事故减少5%至8%，季度军阶赏银仍封顶15万两。季末以毕业、到岗、实辖、军阶和军团面板同步为验收。

3. 今清军因连续失马增兵护仓，人和军已具短袭经验。着黄得功总领、吴三桂主攻，祖大寿供乙级情报，沈应时导路、黄蜚海接，限4时辰；内应失联或伤亡达8%即撤。依上季战果推演，可夺马500至650、得械2500至3000、焚粮2000石，使合锋经验加2、士气加1，清军另分兵800至1200、骑兵补充成本升3%至5%。季末以归队93%、双源战果与马械面板更新为验收。
```

## Prohibited structures

Do not:

- write `奉天承运皇帝，诏曰` before every directive;
- write `钦此` after every directive;
- treat four sections as four separate edicts;
- place one giant 1500-character directive inside a section;
- split one policy into many tiny fragments with no causal closure;
- give commands without predicted results;
- give results without mechanism, owner, resource, deadline, and risk;
- repeat the full world description in every directive;
- put all predicted benefits only in a final summary;
- archive simulated results as executed facts.

## Validation checklist

### Whole edict

- one title;
- one imperial opening;
- one world-state preamble;
- four sections in fixed order;
- each section under 2000 characters;
- one final `钦此。`;
- 1 decisive main effort, 2 hard supports, up to 3 maintenance lines.

### Each directive

- one policy only;
- 280–450 characters normally, never above 500 without permission;
- relevant actual baseline appears;
- causal mechanism is explicit;
- owner, resource, deadline appear;
- risk or failure line appears;
- 3–6 quantified outputs appear;
- material cost or tradeoff appears;
- end-state target appears;
- evidence or panel update is named;
- predicted result remains separate from actual history.

## Output defaults

When asked for a formal quarterly edict, output the entire four-section edict, not isolated directives.

When asked for one policy order, output one compact directive only and identify which of the four sections it belongs to.

When archiving, store:

- edict-level metadata;
- section list;
- directive list;
- predicted result fields;
- actual result fields left empty until the next executed chronicle.