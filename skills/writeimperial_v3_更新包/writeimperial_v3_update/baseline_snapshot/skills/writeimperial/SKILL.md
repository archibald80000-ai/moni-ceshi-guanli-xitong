---
name: writeimperial
description: Draft, revise, and archive imperial edicts for the Chinese historical strategy workflow "历史模拟器：崇祯". Use when asked to read local Chongzhen simulator archives, analyze a quarterly situation, prepare emperor-to-minister密谈话术, draft four-section edicts, set考成/奖惩 targets, or update the project archives for edicts, strategy, intelligence, personnel, and history records.
---

# writeimperial

## Purpose

Use this skill to produce actionable 崇祯 simulator strategy and诏书 from the local archive. The core loop is: read档案 -> judge局势 -> lock季度主轴 -> draft four-section分条诏书 -> validate -> optionally write档案 when explicitly authorized.

## Core Workflow

1. Ground in the latest archive before writing.
   - Read the newest `朝政纪要`, previous季诏书, `国家态势`, `国策路线`, `朝臣档案`, `密谈记录`, and relevant `data/*.json`.
   - If the user supplies screenshots or pasted minister advice, treat them as current player material and reconcile them with archive facts.
   - If archive facts and user material conflict, prefer the latest季度纪要 and mark user additions as strategic intent or推演.

2. Extract the current crisis map.
   - Always cover: 军事, 内政, 财政, 外交, 民变风险, 朝堂/派系, 疫病/灾荒, 边防, 军工.
   - Identify the single most lethal near-term risk and the 2-4 supporting priorities.
   - Do not spread one edict across unrelated high-resistance reforms unless the user explicitly asks for a national mobilization诏.

3. Lock the quarterly axis.
   - Use at most 3-5 main lines, e.g. “救大同、截陕晋、续撤辽、节财用”.
   - Make the first line of each edict section a concrete core command because the game AI prioritizes section-leading instructions.
   - Keep previous effective policies unless the latest纪要 proves they failed.

4. Draft in four fixed sections.
   - Required order: `【军事】`, `【内政】`, `【外交】`, `【其他】`.
   - Each section first line must be an imperative core command.
   - Then use numbered clauses `1. 2. 3.` with execution owner, department/region, money/grain, deadline, bottom-line target, upper target, supervision, reward, and punishment.

5. Set targets and rewards.
   - If last season has measured results, never repeat the same target.
   - Default: bottom-line target should exceed last actual result; user preference is often +`30%`.
   - If user asks for上考 or “目标提高”, set上考 around +`50%` above actual or bottom-line.
   - Put rewards early, especially for军队, 官僚, 农民, 士绅, and useful technical officials.

6. Validate before finalizing or writing.
   - Check four-section structure and `钦此。`.
   - Check numeric style: money, grain, troops, deadlines, satisfaction, stock, production use Arabic digits; 5+ digit quantities use `万` where natural.
   - Scan forbidden vague phrases and forbidden strategies.
   - If writing JSON archives, parse every touched JSON after writing.

7. Archive only with explicit authorization.
   - You may suggest archive updates anytime.
   - Do not edit files unless the user says “写入档案”, “更新档案”, “落档”, or otherwise clearly authorizes writing.
   - Never claim game actions were executed; only state that local档案 were updated.

## References

- Read `references/edict_rules.md` when drafting or revising an诏书.
- Read `references/archive_map.md` when deciding which project files to inspect or update.
- Read `references/style_examples.md` when you need a compact example of the preferred条款 style.

## Output Defaults

- For direct诏书 requests: output the finished edict first unless the user asks for analysis.
- For参谋 requests: use concise sections: 档案依据, 局势判断, 优先级, 风险推演, 推荐方案, 诏书草案, 白话解释, 档案更新建议.
- For write requests: summarize changed files and validation results after updating.
