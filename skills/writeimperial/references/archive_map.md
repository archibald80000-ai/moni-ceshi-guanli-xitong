# Archive Map

Use paths relative to the project root `崇祯模拟器辅助管理系统`.

## Read First

1. Latest `大明档案/朝政纪要/<年>/<季>季朝政纪要.md`
2. Previous season edict in `大明档案/诏书全集/`
3. Latest `大明档案/国家态势/`
4. `大明档案/国策路线/国策路线.md`
5. Relevant `大明档案/密谈记录/`
6. `大明档案/朝臣档案/朝臣总档.md`
7. `大明档案/参谋笔记/个人战略笔记.md`
8. `data/game_state.json`, `data/personnel.json`, `data/strategy.json`, `data/intelligence.json`, `data/edicts.json`, `data/history_records.json`

## Common Write Targets

Write only after explicit authorization.

- New edict: `大明档案/诏书全集/<时间>《<标题>》.md`
- Edict index: `大明档案/诏书全集/诏书全集.md`
- State recap: `大明档案/国家态势/<时间>国家态势复盘.md` or `<时间>拟诏国家态势.md`
- Strategy: `data/strategy.json` and `大明档案/国策路线/国策路线.md`
- Intelligence: `data/intelligence.json`
- Personnel: `data/personnel.json` and `大明档案/朝臣档案/朝臣总档.md`
- History: `data/history_records.json`
- Edicts: `data/edicts.json`
- Upload/index: `uploads/index.json` and `大明档案/资料索引/上传资料目录.md`
- War notes: `大明档案/战争记录/战争记录.md`
- Emperor log: `大明档案/皇帝日志/季度记录.md`

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
