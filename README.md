# 崇祯模拟器辅助管理系统

这是《历史模拟器：崇祯》的长期档案管理仓库，用于保存季度纪要、诏书、财政、军队、人事、地方政策、国策和执行考成。仓库不连接游戏，也不自动替玩家执行决策。

## 当前档案

- 档案版本：`CZ11-SUMMER-EXEC-1`
- 当前游戏时间：崇祯11年夏季
- 快速入口：`CURRENT_ARCHIVE.md`
- 权威清单：`data/archive_manifest.json`
- 当前快照：`data/current_snapshot.json`
- 当前人事：`data/personnel_current.json`
- 当前军队：`data/military/CZ11-SUMMER-MILITARY-1.json`
- 当前人事详表：`data/appointments/CZ11-SUMMER-PERSONNEL-1.json`
- 当前地方政策：`data/policies/CZ11-SUMMER-LOCAL-POLICIES-1.json`
- 当前四总社：`data/companies/CZ11-SUMMER-FOUR-CORPORATIONS-1.json`
- 当前省级面板：`data/province_panels/CZ11-SUMMER-PROVINCES-1.json`
- 当前政令与秋季任务：`data/current_directives.json`
- 最新纪要：`大明档案/朝政纪要/崇祯十一年/崇祯十一年夏季朝政纪要——首辅薨逝财政虚，三路奇袭辽东惊.md`

## 当前核心事实

### 财政政治

- 毕自严病逝，首辅、中极殿大学士、户部尚书正式空缺；王三善、蔡懋德署理。
- 六部36名堂官称具名；季末正式实职53/54，署理维持54席运转。
- 国库期末5558890两；内帑正文期末2801250两。
- 三军50万、武备10万存在国库内帑双记；安抚总额30万与分项35万冲突。

### 军队

- 战兵实补8000、辅兵7000、侦骑800，但总实点未报且战兵未达84000。
- 五日可调、训练、军械、五册和关口无实际数；靖边军团未授旗。
- 新军经验42、士气93、忠诚85、补给71。
- 武备学堂到学1170；1040人毕业到岗待秋季。
- 九级军阶实名评分赏罚无实际数。

### 辽东

- 夺马750、军械3800、焚粮3200、归队率89%，主要目标未达。
- 阵亡420、伤180，按万人约6%，守住伤亡线。
- 大明威望97，大清89。

### 地方经济

- 百万亩屯田没有清册、验实和实耕实际数。
- 鼠疫造成山西、陕西、河南死亡68000，边军辅兵减员1100。
- 四社销售25万至28万、净收益6万至7万，连续两季未达。
- 六口报关4日，货值和海贸实税增长10%，绝对数缺失。
- 燧发枪库存4000、年产能力6000；新造改造12000未核。
- 艺学局实际500/目标10000。

## 强制读档顺序

1. `CURRENT_ARCHIVE.md`
2. `data/archive_manifest.json`
3. `data/current_snapshot.json`
4. `data/personnel_current.json`
5. 当前军队、人事、地方政策、四社和省级面板
6. `data/current_directives.json`
7. 长期记忆、最新纪要、当前诏书和执行考成
8. 需要历史背景时再读旧固定JSON

## 强制规则

- 无实际数按未完成。
- 补入兵员不得冒充期末总实点。
- 署理不得冒充正式任命。
- 产能不得冒充产量，增长率不得冒充绝对收入。
- 股本、洋银、货值、销售、净收益和实税不得重复。
- 一职一主、独立事项不超过5项继续有效。
- 四项旧自动授权176万继续冻结。
- 死囚献首必须作为制度冲突复核，不得默认为新常例。

## 边界与运行

本仓库不包含自动Agent，不操作游戏，不替玩家自动决策。数据使用UTF-8 JSON，Markdown为阅读副本。旧`game_state.json`、`personnel.json`等是历史底座，不能覆盖当前快照。

```powershell
git clone "https://github.com/archibald80000-ai/moni-ceshi-guanli-xitong.git"
cd ".\moni-ceshi-guanli-xitong"
git pull
```
