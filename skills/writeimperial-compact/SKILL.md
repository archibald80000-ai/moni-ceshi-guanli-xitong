---
name: writeimperial-compact
description: Write compact, result-forward imperial directives for the 崇祯 historical simulator. Use when the user asks for short edict clauses, 300–500 character policy paragraphs, one directive per paragraph, immediate simulation results, quantified gains and losses, or a world-state → causal process → constrained execution → visible result → final target structure.
---

# writeimperial-compact

## Purpose

This skill produces short, high-density imperial directives for the 崇祯 simulator. Each directive is written as one compact paragraph that first establishes the world state, then explains the causal execution chain, then states the simulated result and final target.

Mandatory rhythm:

`世界状态 → 问题因果 → 皇帝指令与执行链 → 风险边界 → 即时推演结果 → 最终目标`

The reader must understand, within one paragraph:

1. why the order is necessary;
2. who carries it out;
3. what resources and method are used;
4. what can go wrong and where the red line lies;
5. what concrete game-panel change the order is expected to produce;
6. what state must exist at the end of the quarter.

## Source boundary

Before drafting, read the latest executed chronicle, current state, previous edict, personnel roster, military data, infrastructure data, and relevant strategy files.

Use the latest executed actual as the baseline. Never use a previous target as if it already happened.

A drafted directive may state a **推演结果**, but it must not be archived as an executed fact until a later朝政纪要 confirms it.

Use these labels internally:

- `已知事实`: confirmed by the latest executed chronicle;
- `推演值`: logically derived expected result;
- `最终目标`: end-of-quarter state required by the emperor;
- `实际结果`: only filled after game feedback.

Do not present a推演值 as an actual result in state/history files.

## Paragraph size and cadence

Each directive must be one paragraph of normally `280–450` Chinese characters.

Hard maximum: `500` Chinese characters per directive unless the user explicitly asks for more.

For a quarter containing 3–5 policies:

- write 3–5 independent paragraphs;
- each paragraph handles one policy only;
- do not split one policy into many headings;
- do not bury results in a later summary;
- place the quantified simulated result in the same paragraph as the order.

A military section still must remain under `2000` characters when the project’s four-section edict rule applies.

## Six-sentence compression model

Use up to six logical sentences, not necessarily six visible sentences:

### 1. World state

Open with the current reality, not a slogan.

Include 1–3 decisive facts only:

- enemy strength or weakness;
- current troop readiness;
- treasury and supply condition;
- unrest, plague, trade, harvest, or production condition;
- prior-quarter result and remaining gap.

Good pattern:

`今辽东清军因马场连遭破袭，战马补充不足，盛京仍须分兵护仓；我人和军补给已升至78，合锋军团具备短促突袭条件。`

### 2. Causal judgment

Explain why this action should work.

Use one explicit mechanism:

- cut the enemy’s horses → reduce mobility;
- pay soldiers directly → raise pay arrival and morale;
- build waterworks → expand irrigated acreage and reduce grain-price pressure;
- open ports → increase cargo throughput and tax receipts;
- train officers → improve unit command and lower disorder;
- issue equipment to named units → convert inventory into readiness.

Avoid vague claims such as `必将大振`, `自然成功`, or `国势日隆` without a causal chain.

### 3. Imperial order and execution chain

State in one flow:

- principal owner;
- supporting or audit owner;
- exact action;
- resources;
- deadline.

Compact pattern:

`着黄得功总领、吴三桂率合锋军团出击，祖大寿供乙级情报，沈应时导路、黄蜚海接，限4时辰内完成夺马焚仓并撤回。`

### 4. Risk boundary

Every directive must contain at least one failure line or red line.

Examples:

- casualties exceed 8% → withdraw;
- pay arrival below 95% → suspend reward and investigate;
- sales below 80% of target → freeze expansion;
- intelligence below B grade → cancel attack;
- grain prices rise above 5% → stop government procurement;
- panel not updated → task fails.

Risk language must alter execution, not merely warn.

### 5. Immediate simulated result

Directly state the expected panel result in the same paragraph.

Use 3–6 linked outputs, chosen from:

- troops killed, captured, dispersed, or surrendered;
- horses, weapons, grain, silver, taxes, sales, profit, acreage, jobs;
- experience, morale, loyalty, supply, readiness, equipment availability;
- popular support, satisfaction, authority, prestige, corruption, unrest, epidemic risk;
- enemy cost, enemy diverted troops, enemy mobility, enemy supply;
- construction completion, throughput, repair cost, transport loss;
- personnel graduation, appointment, promotion, pay arrival.

Preferred form:

`推演可得战马800–900匹、军械4000件，清军另增护仓兵1000余；合锋经验+2至3、士气+1，清军机动补充成本再升5%，大明威望+1。`

Do not force every policy to change every panel. Choose only changes supported by the mechanism.

### 6. Final target

End with the desired completed state, not another command.

Good pattern:

`季末以合锋归队率93%以上、辽西清军骑兵补充继续受限、三军马匹实配率99%为最终验收。`

## Result calculation rules

All numerical results must be reasoned from the latest baseline and task type.

Use Scale v3.1 from the main `writeimperial` skill:

- mature production: ordinary quarterly improvement `5%–12%`;
- single military action: result improvement commonly `5%–15%`, with casualty and withdrawal limits;
- training and reorganization: quality normally `+3–6` points or `+3–5` percentage points;
- trade and maritime activity: use actual cargo, tax, loss, and arrival data;
- satisfaction, authority, prestige, corruption, and unrest: ordinary movement is usually `±1–2` points unless a major funded event justifies more;
- zero-tolerance conditions remain zero and are not “increased.”

When an exact number is unsupported, give a narrow logical range and label it as推演, for example:

- `推演增收8万至10万两`;
- `预计减少运输损耗2至3个百分点`;
- `可使敌军分兵800至1200人`.

Never invent precise numbers without a baseline, mechanism, resource, and execution coefficient.

## Benefit ledger

Each directive should, when applicable, cover four layers of benefit:

1. **direct result**: what is immediately gained, destroyed, built, sold, trained, or paid;
2. **system result**: what operational capacity improves;
3. **panel result**: which game values change and by how much;
4. **strategic result**: what next-quarter option becomes possible.

Compact example:

`直接得马850匹；三军侦骑实配提高；军械面板战马缺口缩小850；下一季可扩大辽东侦察与短袭半径。`

Do not count the same benefit twice. Inventory transfer is not new production; internal military allocation is not market sales; authorized funds are not actual spending; production capacity is not output.

## Compact directive template

Use this fillable pattern:

`【政策名】今[世界状态与最新基线]，其症结在[因果判断]。着[主责]会[协同/核验]，以[资源]于[期限]内完成[具体动作]；若[失败线/红线]，即[撤回、冻结、换法或追责]。依现有[兵力/产能/财力/人心/情报]推演，可实际取得[直接成果]，并使[经验、士气、补给、收入、税银、民心、风险等]变化[明确数字或窄范围]，代价为[银两、伤亡、时间或机会成本]。季末以[最终目标1]、[最终目标2]及[面板同步字段]为验收，未更新或无凭证按失败。`

## Three model paragraphs

### Military

`【辽东短袭】今清军马场连遭损失，辽西骑兵补充迟滞，而人和军补给已达78、合锋军团具有万人混编经验。着黄得功总领，吴三桂主攻，祖大寿供乙级以上马场与粮仓情报，沈应时导路、黄蜚海接，行动限4时辰；内应失联、退路受阻或伤亡达8%即撤。依上季夺马850匹、归队91%的实际推演，本次可夺马500–650匹、得械2500–3000件、焚粮2000石，使合锋经验+2、士气+1，清军再分兵800–1200护仓，骑兵补充成本升3%–5%。季末以归队93%、战果双源核验和军械马匹面板同步更新为验收。`

### Internal affairs

`【水利复耕】今百万亩屯田已验实80万亩，但亩产、入仓和农户余粮尚未闭环，若只扩清册不能形成税源。着户部左侍郎会通济水机总社，以既有水车、渠道和屯田军修复主粮区灌溉，90日内新增稳定灌溉10万亩；粮价上涨超过5%即暂停官府征购。按既有实耕基础推演，可增商品粮6%–8%、减少旱损3个百分点，屯户粮银收入+2至3，农民满意度维持90以上，新增可持续税户3000–5000户。季末以亩产、实入仓、余粮、粮价和省级农业面板同时刷新为验收。`

### Industry and trade

`【军工实发】今火铳、轻炮库存充足而军团到营数据不足，库存不能直接转化为战力。着工部、兵部武库司按九团逐件拨付，军团主官逐号签收，30日完成火铳28800支、轻炮540门和燧发枪9000支到营，军械可用率低于99%的军团暂停上等考成。推演完成后，三军火器覆盖率可提高8–12个百分点，五日可调兵力增加3000–5000，训练通过率+2，维修积压下降20%；国库仅承担运输、修械与弹药成本，不重复计购置。季末总库存与九团实发面板必须同日更新，否则全项失败。`

## Prohibited writing

Do not write:

- only commands with no predicted result;
- only predicted result with no mechanism;
- a long background occupying more than one third of the paragraph;
- more than one major policy in one paragraph;
- universal `+30%/+50%` gains;
- every policy raising authority, prestige, morale, revenue, and satisfaction at once;
- exact gains unsupported by a baseline;
- `完成、顺利、全面提升` without numbers;
- `预计、将会、推动` as substitutes for an end state;
- panel changes without specifying which panel must be updated;
- archive writes that convert推演值 into actual fact.

## Validation checklist

Before finalizing each paragraph, verify:

- one policy only;
- 280–450 characters normally, never above 500 without permission;
- latest actual baseline appears;
- causal mechanism is explicit;
- owner, resource, and deadline appear;
- at least one risk boundary appears;
- 3–6 quantified result fields appear;
- cost or tradeoff appears when material;
- final target appears at the end;
- required panel update is named;
-推演 result is not archived as executed fact.

## Output defaults

When the user asks for several directives, output the finished compact paragraphs first. Do not precede them with a long analysis.

For formal edicts, retain the main project order `【军事】【内政】【外交】【其他】`, but each numbered clause should follow this compact result-forward pattern.

When archiving, store planned result fields separately from actual result fields and wait for the next executed chronicle before filling actual values.
