# data 读取说明

当前机器入口依次为：

1. `archive_manifest.json`
2. `latest_state.json`
3. `current_snapshot.json`
4. `personnel_current.json`
5. `current_directives.json`
6. `state_snapshots/CZ11-WINTER-EXEC-1.json`
7. `state_snapshots/CZ12-SPRING-IN-PROGRESS-1.json`
8. `evidence_model.json`

旧 `game_state.json`、`history_records.json`、`personnel.json`、`strategy.json`、`intelligence.json`、`edicts.json` 为早期兼容数据，部分记录止于崇祯9年春。它们可以查历史，但不得决定当前回合。

当前事实时间为崇祯12年春执行中；最近完整反馈为崇祯11年冬。12年春密谈、诏书和任务尚待玩家补充。

所有新增结构化记录须使用 `evidence_model.json` 的五层分类。L1计划、L2诏书和L5事后修订不得直接更新当前事实；L4当前快照必须能追溯到L3游戏结果。
