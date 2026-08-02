# Archive Map

Use paths relative to the project root `崇祯模拟器辅助管理系统`.

## Read First

1. Latest `大明档案/01_季度政务/03_朝政纪要/<年>/<季>季朝政纪要.md`
2. Previous season edict in `大明档案/01_季度政务/02_诏书/`
3. Latest `大明档案/02_国家档案/03_国家态势/`
4. `大明档案/03_国策与战略/01_制度规则/关键制度源头/01_长期国策有效清单.md`
5. `大明档案/03_国策与战略/01_制度规则/关键制度源头/02_季度试行与非永久政策清单.md`
6. `大明档案/03_国策与战略/02_战略方针/README.md`, relevant `大明档案/03_国策与战略/04_国策设计/`, and historical `大明档案/03_国策与战略/03_已执行方案/`
7. Relevant `大明档案/01_季度政务/01_密谈/`
8. `大明档案/02_国家档案/01_朝臣/朝臣总档.md`
9. `大明档案/03_国策与战略/05_玩家笔记/个人战略笔记.md`
10. `data/game_state.json`, `data/personnel.json`, `data/strategy.json`, `data/intelligence.json`, `data/edicts.json`, `data/history_records.json`

## Common Write Targets

Write only after explicit authorization.

- New edict: `大明档案/01_季度政务/02_诏书/<时间>《<标题>》.md`
- Edict index: `大明档案/01_季度政务/02_诏书/诏书全集.md`
- State recap: `大明档案/02_国家档案/03_国家态势/<时间>国家态势复盘.md` or `<时间>拟诏国家态势.md`
- Current long-term policy: `大明档案/03_国策与战略/01_制度规则/关键制度源头/01_长期国策有效清单.md`
- Strategic direction: `大明档案/03_国策与战略/02_战略方针/`
- New policy proposal: `大明档案/03_国策与战略/04_国策设计/`
- Historical executed proposal: `大明档案/03_国策与战略/03_已执行方案/`
- Historical strategy mirror: `data/strategy.json` and `大明档案/03_国策与战略/90_历史策略镜像/国策路线.md`
- Intelligence: `data/intelligence.json`
- Personnel: `data/personnel.json` and `大明档案/02_国家档案/01_朝臣/朝臣总档.md`
- History: `data/history_records.json`
- Edicts: `data/edicts.json`
- Upload/index: `uploads/index.json` and `大明档案/04_辅助资料/上传资料索引.md`
- War notes: `大明档案/02_国家档案/05_战争/战争记录.md`
- Emperor log: `大明档案/01_季度政务/季度记录汇总（系统生成）.md`

## Conflict Policy

- Latest季度纪要 is the highest factual source.
- User screenshots and minister pasted text are current strategic material, but not executed facts until the next纪要 confirms.
- If `data/*.json` lags behind Markdown纪要, use the Markdown纪要 and note the mismatch.
- Historical materials, videos, and user strategy are “取法/推演” unless the game archive confirms execution.

## Validation After Writing

- Parse all touched JSON files.
- Confirm the new edict file exists and includes the required structure.
- Scan for forbidden strategies and vague phrases.
- Report that local archives were updated, not that in-game actions occurred.
