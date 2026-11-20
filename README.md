# Huawei CES Skill + MCP

独立的华为云 CES 只读排障工具，提供 Agent Skill、轻量 Python stdio MCP 服务，以及 Cursor、Claude Code、OpenCode、Codex 的安装/卸载脚本。

这是 key-well 维护的社区项目，非华为云官方发布。复用 LTS 项目的安装和适配实现，工具绑定使用华为云官方 Python SDK，无需克隆整套上游 MCP 工程。来源与许可证见 [NOTICE](NOTICE)。

## 能力

华为云监控指标、告警规则和告警历史的只读关联排查，共 **22 个只读查询工具**。完整清单见 [references/tools.md](references/tools.md)。

不新增、修改、删除告警，不发送监控数据，不执行 Agent 任务，也不更改通知屏蔽策略。

## 安装

要求 macOS/Linux、Git、Python 3.10+、[uv](https://docs.astral.sh/uv/) 和至少一个受支持客户端。

```bash
git clone https://github.com/key-well/huawei-ces-skill.git
cd huawei-ces-skill
./install.sh --platforms codex
# 可选：cursor / claude / opencode，逗号分隔；不指定则安装所有客户端
# ./install.sh --platforms cursor,claude
# 自定义运行目录必须为绝对路径或 ~/ 开头
# ./install.sh --platforms codex --install-dir ~/tools/huawei-ces-skill
```

默认运行目录：`~/.local/share/huawei-ces-skill`。安装在独立 `.venv` 中运行，合并本服务的 MCP 项并备份已有客户端配置；不同服务分别安装，不覆盖其他 MCP 项。不会调用 sudo，也不会自动安装 uv。

| 客户端 | Skill 目录 | MCP 配置 |
|---|---|---|
| Codex | `~/.agents/skills/huawei-ces` | `~/.codex/config.toml` |
| Claude Code | `~/.claude/skills/huawei-ces` | `~/.claude.json` |
| Cursor | `~/.cursor/skills/huawei-ces` | `~/.cursor/mcp.json` |
| OpenCode | `~/.config/opencode/skills/huawei-ces` | `~/.config/opencode/opencode.json` |

安装后，在本地配置里将下列占位符替换为自己的值，再重启客户端。不要把真实 AK/SK 发到聊天或提交到仓库。

```text
HUAWEI_ACCESS_KEY=REPLACE_WITH_YOUR_AK
HUAWEI_SECRET_KEY=REPLACE_WITH_YOUR_SK
HUAWEI_REGION=REPLACE_WITH_YOUR_REGION
HUAWEI_PROJECT_ID=REPLACE_WITH_YOUR_PROJECT_ID
```

地域/项目也可由工具调用 `region` / `project_id` 覆盖，优先级高于环境默认值。运行时要求二者完整，不自动跨项目查询。此版本不支持 STS 临时凭证。

建议使用专用、最小只读 IAM 权限；工具白名单限制不替代云端权限管理。安装脚本重复执行会重写本服务的 MCP 项为占位配置，请妥善保留自己的本地配置并重新填入，不要将配置备份提交 Git。

## 使用

- 查资源 RESOURCE_ID 在北京时间 14:00 到 14:30 的可用指标，确认命名空间后再查数据。
- 对照实例 RESOURCE_ID 最近一小时的指标和告警历史，说明聚合粒度与数据缺口。
- 查告警规则 ALARM_ID 的策略和关联资源，不修改规则。

Skill 中包含服务专属的排查路线和数据边界。CES 监控或 LTS 日志跨服务关联需要分别安装相应 MCP，不会自动连接。

## 卸载

```bash
./uninstall.sh --platforms codex
# 自定义运行目录时传入与安装时一致的 --install-dir
```

仅卸载本安装拥有的配置和 Skill，恢复安装前记录的条目；仍有客户端使用时保留运行目录。先前配置备份可能含有本地凭证，请自行安全保管。

## 开发与验证

```bash
uv sync --frozen --extra dev
uv run pytest
uv run python scripts/generate_tools.py --check
bash -n install.sh uninstall.sh
```

`references/operations.json` 是显式工具白名单；生成脚本验证 SDK 请求类、方法和 HTTP 方式，并生成已提交的完整 inputSchema。升级依赖后运行 `--write` 更新目录，并审查差异。拒绝未登记操作、未知字段、缺失必填字段和类型不匹配的请求。

测试使用假客户端和临时 HOME，不需要云凭证，不会更改真实客户端配置。包含安装/卸载、参数转换、版本路由及 stdio 协议检查。**离线测试通过不等于云端验收通过**；首次使用仍需以自己的只读账号验证地域、权限与实际返回字段。

## 许可证

主体代码 MIT；保留 LTS 上游版权声明。官方操作清单衍生部分遵守 Apache-2.0，详见 [NOTICE](NOTICE)、[LTS-LICENSE](LTS-LICENSE) 和 `licenses/iaas-mcp-server-LICENSE`。
