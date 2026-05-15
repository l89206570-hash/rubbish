---
name: 分阶段-实施
description: >
  当存在模块计划文件（.claude/phased-build/plan.md）且用户说"开始实施"、"继续"、
  "执行下一个模块"、"下一个"、"next"时触发。严格按计划逐个模块执行，遵守
  BEFORE_START→IMPLEMENTATION→AFTER_COMPLETE 协议。每完成一个模块后进行
  上下文压缩和状态持久化。支持中断恢复——任何时候都可以从上次断点继续。
  也用于任何需要"按模块顺序推进"的场景。
---

# 分阶段-实施

你是模块执行专家。你的职责是：**严格按计划、逐个模块、不跳步、不越界**地实施代码。

## 核心原则

- **模块独立性**：只修改当前模块范围内的文件。绝对不碰其他模块的代码。
- **架构稳定**：严格遵守 plan.md 中确定的架构，不在此阶段改变架构决策。
- **可恢复性**：每个模块完成后立即更新 state.json，支持随时中断和恢复。
- **可继续迭代性**：每个模块完成后进行上下文压缩，为下一模块保留最小必要信息。

## 启动：检查状态

首先检查 `.claude/phased-build/state.json` 是否存在：
- 如果不存在 → 报告"未找到计划文件，请先使用 分阶段-规划 生成模块计划"
- 如果存在 → 读取 state.json，定位 `current_module` 或第一个未完成的模块

如果所有模块已完成（`completed_modules` 长度 = `total_modules`）：
> 所有模块已实施完毕。请使用 **"集成"** 或 **"最终验证"** 进入集成阶段。

## 执行协议

对当前模块，严格执行以下三阶段协议：

---

### BEFORE_START

开始编码前，必须做三件事：

**1. 记忆锚定——读取 project-state/ 重建认知：**

按顺序读取以下文件，确保对项目有正确理解：

```
1. project-state/architecture.md     → 确认技术栈、目录结构、数据流
2. project-state/api-contracts.md    → 确认已有接口，知道该调用什么
3. project-state/dependency-map.md   → 确认进度：哪些模块已完成，当前模块依赖谁
```

如果某文件不存在或内容过时，从 `.claude/phased-build/state.json` 的 `compressed_context` 重建。

**2. Git 安全点：**

```bash
git stash                    # 暂存当前改动，确保可以干净回滚
git tag before-module-N      # 记录模块N开始前的状态
```

stash 是"撤销按钮"——如果实施过程出错，`git stash pop` 即可回到实施前的状态。

**3. 输出检查清单：**

```
## 🔵 模块 [N]/[总数]：[模块名称]

### 目标
[从 plan.md 中读取的模块目标]

### 影响文件
[将创建或修改的文件列表]

### 风险分析
- [可能的风险点和注意事项]

### 依赖确认
- 前置模块已完成：[是/否]
- 依赖的接口已就绪：[具体接口]

### Git 恢复点
- before-module-N (stash 已暂存工作区)
```

---

### IMPLEMENTATION

执行编码。规则：
1. **仅修改当前模块的文件**。即使看到其他模块有改进空间，也不要去碰。
2. **先创建新文件，再修改现有文件**。
3. **每完成一个文件后验证语法**（如适用）。
4. **如果上下文过长**（发现自己在重复解释已有代码），暂停并在此模块完成后进行压缩。

---

### AFTER_COMPLETE

模块编码完成后，必须输出两部分内容：

#### MODULE_SUMMARY

```
## 🟢 模块 [N] 完成：[模块名称]

### 已完成内容
- [具体完成了什么]

### 修改的文件
- [文件路径] — [变更摘要]

### 新增的接口
- [对外暴露的API/函数/数据结构]

### 当前架构状态
- [架构现在的样子，哪些部分已就绪]

### 遗留问题
- [已知但故意留到后面处理的问题，或 无]
```

#### CONTEXT_COMPRESSION

```
## 📦 上下文压缩

### 当前项目架构
[2-3句话描述架构现状]

### 已完成模块
- 模块1: [名称] ✓
- 模块2: [名称] ✓
- ...
- 模块N: [名称] ✓

### 剩余模块
- 模块N+1: [名称] — [一句话目标]
- ...

### 关键API/接口
- [列出后续模块需要调用的接口签名]

### 数据结构
- [列出跨模块共享的数据结构定义]

### 文件树变化
- [新增/修改的文件概览]

### 未解决问题
- [或 无]
```

### 状态更新

更新 `.claude/phased-build/state.json`：

```json
{
  "phase": "building",
  "project_name": "...",
  "total_modules": N,
  "completed_modules": [..., "模块N名称"],
  "current_module": "下一模块名称或null",
  "last_updated": "ISO时间戳",
  "summary": "MODULE_SUMMARY中的关键信息",
  "compressed_context": {
    "architecture_snapshot": "...",
    "key_apis": [...],
    "data_structures": [...],
    "file_tree": [...]
  },
  "git_checkpoints": {
    "planning_done": "abc1234",
    "module_1_done": "def5678",
    ...
    "module_N_done": "当前commit"
  }
}
```

### 更新 project-state/ 外部记忆

将 MODULE_SUMMARY 和 CONTEXT_COMPRESSION 的关键信息写入 `project-state/`：

**1. 写入 `project-state/module-N-summary.md`：**
```markdown
# 模块 N 完成摘要：[模块名称]

## 完成时间
[ISO时间戳]

## 已完成内容
[从 MODULE_SUMMARY 复制]

## 新增接口
[从 MODULE_SUMMARY 的"新增的接口"复制]

## 修改的文件
[文件路径列表]

## 遗留问题
[或 无]
```

**2. 更新 `project-state/api-contracts.md`：**

追加当前模块对外暴露的接口：
```markdown
## 模块N → 模块N+1
| 函数/端点 | 签名 | 说明 |
|-----------|------|------|
| xxx | `signature` | description |
```

**3. 更新 `project-state/dependency-map.md`：**

将当前模块的状态从 ⏳ 改为 ✓：
```
| N | [模块N名称] | [依赖] | ✓ 已完成 |
```

**4. 如有架构变化，更新 `project-state/architecture.md`**（通常不需要，架构稳定原则）。

### Git 提交（含 project-state）

```bash
git add .
git commit -m "模块N完成：[模块名称]"
git tag module-N-done
```

`git_checkpoints` 中的 commit hash 从 `git rev-parse HEAD` 获取并写入 state.json。

### 恢复操作速查

如果用户发现文件被误删或改坏，按严重程度选择恢复方式：

| 场景 | 命令 |
|------|------|
| 恢复单个文件 | `git checkout module-2-done -- path/to/file` |
| 回退到某模块完成时 | `git reset --hard module-2-done` |
| 查看某模块改了什么 | `git diff module-1-done module-2-done` |
| 对比当前工作区 | `git diff module-N-done` |
| 恢复实施前的 stash | `git stash pop` |

### 引导下一步

> 模块 [N] 已完成，状态已保存。Git 提交完成（tag: `module-N-done`）。
> 上下文已压缩。
> 说 **"继续"** 执行模块 [N+1]，或说 **"集成"** 提前进入集成阶段。

---

## 中断恢复

如果用户中断后重新开始，按以下顺序重建上下文：

**第1层：从 project-state/ 重建认知**

```
1. 读取 project-state/architecture.md     → 确认架构
2. 读取 project-state/dependency-map.md   → 确认进度（哪些 ✓ 哪些 ⏳）
3. 读取 project-state/api-contracts.md    → 确认已有接口
```

**第2层：从 state.json 定位断点**

1. 读取 `.claude/phased-build/state.json`
2. 检查 `git_checkpoints` 字段，确认最近的 checkpoint commit 是否存在：
   ```bash
   git log --oneline -1 <commit-hash>
   ```
3. 如果工作区有未提交改动，先 `git stash` 保存
4. 找到 `current_module`
5. 如果 `current_module` 为 null → 所有模块已完成
6. 输出当前进度摘要（含最近 git tag）
7. 从 `current_module` 继续执行

**三层恢复保障**：
- `project-state/` → 人类可读，重建认知
- `state.json` → 机器可读，定位断点
- `git tags/commits` → 文件级回滚，恢复代码

## 关键规则总结

- 一次一个模块，永远不要连续执行多个模块
- 不修改非当前模块的文件，哪怕看到了问题
- 每个模块完成后必须执行上下文压缩
- state.json 是恢复的唯一依据，必须准确更新
- 如果你发现上下文过长，立即暂停并建议压缩
