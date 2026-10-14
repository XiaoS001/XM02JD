# 技术收藏存档：REA (Reverse Engineer Anything)

> 存档日期：2026-10-26
> 来源：用户提供截图 + GitHub/npm 官方源核实
> 状态：**仅存档，未安装、未执行**。需要时再按官方源安装。

---

## 一、项目身份（务必认准官方源）

| 项 | 值 |
|---|---|
| 项目名 | REA — Reverse Engineer Anything |
| 官方仓库 | https://github.com/morluto/rea （21.3 万 star，2026-10 时点） |
| 官方站点 | https://rea.tools/ |
| npm 包 | `rea-agents`（当前 latest 6.4.0） |
| 许可证 | MIT |
| Discord | https://discord.gg/GkcryMnJDM |

> ⚠️ **README 明确警告**：仓库名相似、或复制了 README 的仓库，**不代表是官方下载**。安装必须从上面三个官方源之一进行。

---

## 二、它是干什么的

一个 **MCP server + CLI**，让 agent 在**无源码**的情况下逆向分析：

- 应用行为（某个功能是怎么实现的）
- 原生二进制（native binaries）
- JavaScript / Electron 应用目录与 ASAR 包
- 运行时行为

典型用法（README 原文示例）：

```text
Understand how search works in the Notes app, show me the evidence,
and build a similar feature for my project.
```

CLI 用法示例：

```bash
npx -y rea-agents@latest analyze-javascript-application /absolute/path/to/app --json
```

---

## 三、安装方式（用时再执行，现在不跑）

### 3.1 给 agent 装（会写 MCP 配置 + workflow 指令）

```bash
npx rea-agents setup
```

- 支持 Claude Code、Codex、Cursor、Gemini CLI、Grok Build 等
- 会**修改 agent 配置**，但带备份；装完需重启 agent
- ⚠️ 执行前先看清它要对哪些配置文件做什么

### 3.2 手动 MCP 注册 / provider 配置

见官方文档 `docs/installation.md`。

### 3.3 系统要求

- Node.js + npm
- Linux 下静态分析（Ghidra/JADX/固件等）需 procps 的 `ps` 在 PATH 上
- Windows/macOS 详见官方文档

---

## 四、为什么当时只存档不安装（决策记录）

1. 用户诉求是"以后可能会用到"，非当前刚需。
2. `npx rea-agents setup` 会改动 agent 配置，非必要不贸然执行。
3. 当前主线是「按 JD 练手 Java 后端项目」，与此工具是两条线。
4. 用户当时未开网络代理，GitHub 直连不通，安装依赖需走镜像。

---

## 五、国内网络镜像（当时实测可用性）

| 镜像 | 状态（2026-10-26） |
|---|---|
| gh-proxy.com | ✅ 可通（api/raw 均可用） |
| gitclone.com | ✅ 可通（根路径 404 属正常） |
| ghfast.top | 403（能通但被拦） |
| gitee.com | ✅ 200 完全可达 |
| ghproxy.com / mirror.ghproxy.com / hub.fastgit.xyz | ❌ 超时 |

> 以后安装或 clone 时，优先走 `https://gh-proxy.com/https://github.com/...`。

---

## 六、用的时候找谁

以后需要用到 REA 时，告诉我一声，我会：
1. 从官方源（GitHub 主仓 / npm / rea.tools）重新核对最新版本；
2. 按官方 `docs/installation.md` 评估对当前环境的适配；
3. 走国内镜像完成安装，并在执行 `setup` 前先展示它要改哪些配置。
