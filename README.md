# 崇祯模拟器辅助管理系统

这是供个人使用的《历史模拟器：崇祯》长期档案管理系统，用于结构化保存、检索、归档和辅助分析季度纪要、诏书、人员、财政、军力与长期目标。系统不连接游戏，也不自动执行决策。

## 远程多设备入口

公开仓库：

```text
https://github.com/archibald80000-ai/moni-ceshi-guanli-xitong
```

新设备或新的 AI 线程不必先克隆仓库即可阅读公开页面；需要修改、运行或同步时再使用 Git。

### 当前档案快照

- 档案版本：`CZ10-SUMMER-EXEC-1`
- 版本名称：崇祯十年夏季执行反馈
- 当前游戏时间：崇祯10年夏季
- 快速入口：`CURRENT_ARCHIVE.md`
- 机器读取入口：`data/archive_manifest.json`
- 当前结构化快照：`data/current_snapshot.json`
- 当前人事覆盖层：`data/personnel_current.json`
- 当前执行与下一季要求：`data/current_directives.json`
- 诏书长期记忆：`大明档案/制度规则/崇祯模拟器诏书撰写长期记忆.md`
- 最新事实源：`大明档案/朝政纪要/崇祯十年/崇祯十年夏季朝政纪要——辽阳焚粮振军威，京西投产百工兴.md`
- 当前国家态势：`大明档案/国家态势/崇祯10年夏季国家态势总览.md`
- 当前军械库存：`大明档案/国家态势/崇祯10年夏季军械库存.md`
- 当前人事复核：`大明档案/朝臣档案/崇祯10年夏季朝臣任职复核.md`

历史数组中的旧年份属于历史记录，不代表当前回合。判断当前时间必须先读 `data/archive_manifest.json`、`data/current_snapshot.json` 和 `CURRENT_ARCHIVE.md`；旧 `data/game_state.json` 等固定数组仅作为历史底座。

当前长期财政红线：全国练兵补给100万、防损防疫20万、人才专项国库30万、长期常赏26万，合计176万两的自动拨款、年度滚存和触发权继续冻结。未经御前当季明发新旨不得恢复、拆名或变相支出；正俸和基本军饷不受影响。

## 当前核心事实

- 辽阳夜袭毁粮约25500石，达到底线；归队人数口径存在90.5%与95%冲突。
- 京西军械总厂工程83%、六区投产；厂报产量与全局库存增量必须分账。
- 三层军制主要底线完成；京营转役人数纪律达标，但军屯实播无实际数。
- 陕西、山西、河南靖乱完成；乌思藏压缩25%，未达30%。
- 全国大明地区民心最低不低于43；河南净增2未达净增4。
- 海贸税20万达到上考；重修大明律、核心技术零外泄完成。
- 人才累计3950未达4000；技术下沉和归屯留存缺实际数。
- 东江辅兵18085、补给70、忠诚48；登莱新军仅余300辅兵。
- 国库期末2531445.82两、内帑2304250两；92万大赏与国库88万支出分账仍待核。

## 新设备同步

```powershell
git clone "https://github.com/archibald80000-ai/moni-ceshi-guanli-xitong.git"
cd ".\moni-ceshi-guanli-xitong"
```

已有设备更新：

```powershell
git pull
```

本地修改后同步：

```powershell
git status -sb
git add -A
git commit -m "backup: 更新崇祯档案"
git push
```

不要提交 `.env`、`.env.*`、`__pycache__/`、`*.pyc` 等本地缓存或密钥。

## AI 读档导航

推荐读取顺序：

1. `CURRENT_ARCHIVE.md`
2. `data/archive_manifest.json`
3. `data/current_snapshot.json`
4. `data/personnel_current.json`
5. `data/current_directives.json`
6. `大明档案/制度规则/崇祯模拟器诏书撰写长期记忆.md`
7. 最新朝政纪要、上一季正式诏书和当前 Scale
8. 需要历史背景时再读取旧固定 JSON

必须遵守：

- 最新朝政纪要和同回合面板是最高事实依据。
- 当前快照是结构化覆盖层，旧 JSON 不得覆盖它。
- 全局库存不得冒充单厂产量。
- 本季硬目标季末必须报告实际数、完成率、判定和证据；无实际数按未完成。
- 冲突必须写入 `data/archive_manifest.json`，不得静默选择最乐观口径。
- 未完成和长期目标必须同步进诏书长期记忆。

## 核心资料位置

- `data/current_snapshot.json`：当前季度结构化事实。
- `data/personnel_current.json`：当前六阁六部、人事和临时差遣。
- `data/current_directives.json`：当前考成和下一季要求。
- `data/archive_manifest.json`：当前版本、权威来源和冲突。
- `data/history/`：每季度独立结构化记录。
- `data/edicts/`：季度诏书结构化目标与反馈。
- `data/strategy/`：季度方案和执行考成。
- `data/personnel.json`、`data/history_records.json`、`data/game_state.json`、`data/edicts.json`、`data/strategy.json`、`data/intelligence.json`：历史底座。
- `大明档案/朝政纪要/`：原始季度纪要。
- `大明档案/国家态势/`：季度总览和军械库存。
- `大明档案/朝臣档案/`：当前人事复核。
- `大明档案/财政报告/`、`战争记录/`、`诏书全集/`：专题档案。
- `大明档案/制度规则/`：长期记忆与制度红线。
- `uploads/index.json`、`大明档案/资料索引/上传资料目录.md`：上传资料索引。

## 边界

- 不包含自动 Agent。
- 不模拟或操作游戏。
- 不替玩家自动决策。
- 未经用户授权不得修改仓库或发布诏书。
- 证据不足时必须明确标记未知或未完成。

## 本地运行

要求 Python 3.9 或更高版本，无第三方依赖。

```powershell
cd "E:\AIS\AI任务执行清单\0730\崇祯模拟器辅助管理系统"
py main.py
py main.py --check
```

网页版：

```powershell
py -3 web_app.py --open
```

本地访问：

```text
http://127.0.0.1:8765
```

数据使用 UTF-8 JSON 保存，Markdown 为便于阅读的知识库副本。建议定期备份整个 `data` 和 `大明档案` 目录。
