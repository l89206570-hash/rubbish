# state.json 格式定义

此文件定义 `.claude/phased-build/state.json` 的完整结构，由 分阶段-规划 创建，分阶段-实施 维护，分阶段-集成 消费。

## 完整 Schema

```json
{
  "phase": "planning_done | building | integration_done",
  "project_name": "项目名称",
  "total_modules": 5,
  "completed_modules": ["模块1", "模块2"],
  "current_module": "模块3",
  "created_at": "2026-05-15T10:30:00+08:00",
  "last_updated": "2026-05-15T11:45:00+08:00",
  "architecture": {
    "tech_stack": "Python 3.11 + Flask + SQLite",
    "directory_structure": "src/, tests/, config/",
    "entry_point": "src/main.py"
  },
  "modules": [
    {
      "index": 1,
      "name": "模块名称",
      "goal": "一句话目标",
      "files": ["文件路径列表"],
      "dependencies": ["依赖的模块名称或null"],
      "acceptance_criteria": ["验收标准列表"],
      "summary": "完成后填充的摘要"
    }
  ],
  "key_decisions": [
    "使用Flask而非FastAPI因为...",
    "数据库选择SQLite因为..."
  ],
  "compressed_context": {
    "architecture_snapshot": "当前架构的简要描述",
    "key_apis": [
      {
        "name": "函数名",
        "signature": "def func(arg: Type) -> ReturnType",
        "module": "所属模块",
        "description": "功能描述"
      }
    ],
    "data_structures": [
      {
        "name": "结构名",
        "fields": {"field1": "type1", "field2": "type2"},
        "module": "所属模块"
      }
    ],
    "file_tree": ["文件路径列表"],
    "open_issues": ["未解决问题列表"]
  },
  "git_checkpoints": {
    "planning_done": "abc1234 (commit hash)",
    "module_1_done": "def5678",
    "module_2_done": "ghi9012",
    "integration_done": "jkl3456"
  }
}
```

## 阶段说明

### planning_done
- 由 分阶段-规划 写入
- `completed_modules` 为空
- `current_module` 指向第一个模块
- `compressed_context` 为空

### building
- 由 分阶段-实施 在每个模块完成后更新
- `completed_modules` 逐步增长
- `current_module` 指向下一个待执行模块，或 null（全部完成）
- `compressed_context` 在每个模块后更新

### integration_done
- 由 分阶段-集成 写入
- 所有模块已完成
- 包含验证结果摘要

## 恢复逻辑

### 从 state.json 恢复逻辑状态

当 分阶段-实施 启动时：
1. 读取 state.json
2. 如果 `phase` = "planning_done" → 从 `current_module`（第一个模块）开始
3. 如果 `phase` = "building" → 从 `current_module` 继续
4. 如果 `current_module` = null → 提示进入集成阶段

### 从 Git 恢复文件状态

| 场景 | 命令 |
|------|------|
| 恢复到最近 checkpoint | `git reset --hard $(cat state.json \| jq -r '.git_checkpoints.module_N_done')` |
| 查看可用的恢复点 | `git tag -l` |
| 回到某个模块完成时 | `git reset --hard module-N-done` |
| 恢复被误删的单个文件 | `git checkout module-N-done -- path/to/file` |
| 查看两次提交的差异 | `git diff module-1-done module-2-done` |

### 双重保障

- `state.json` 记录逻辑进度（哪个模块已完成、当前模块、架构快照）
- `git tags + commits` 记录文件级快照（可精确回滚到任意模块完成时刻）
- 如果 state.json 丢失，可以通过 `git tag` 列表推断进度
- 如果 `.git` 损坏，state.json 仍有 `git_checkpoints` 中的 commit hash 供参考
