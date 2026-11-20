---
name: huawei-ces
description: >-
  华为云监控指标、告警规则和告警历史的只读关联排查。当用户明确排查 Huawei Cloud CES 时使用，
  通过已连接的 huawei-ces MCP 执行只读查询，不用于其他厂商或一般开发问题。
---

# Huawei CES

## 开始查询

1. 发现当前实际暴露的 MCP 工具名；前缀可能随客户端变化。没有对应工具时说明尚未连接，不虚构云端结果，也不自动改用其他账号或命令行。
2. 目标地域、项目按本次请求指定值优先，其次使用服务器的 `HUAWEI_REGION` / `HUAWEI_PROJECT_ID`；缺失或冲突时询问。多个账号需由用户明确选择服务器连接。
3. 先识别资源 ID，再缩小时间和分页范围。显示时间要说明时区；参数单位以工具 schema 为准。
4. 工具字段是官方 Python SDK 名，嵌套请求使用 `body`，不要传 X-Auth-Token、AK/SK 或原始 HTTP headers。

## 排查路径

- 先确定地域、项目、资源 ID、事故时间和时区，再查询可用的 `namespace`、`metric_name` 和 dimensions；不能凭服务名编造指标。
- 指标发现：`ListMetrics`；指标值：`ShowMetricData` 或 `BatchListMetricData`。先取小时间窗和少量指标，再按证据扩大。
- `ShowMetricData` 使用 SDK 字段 `_from`、`to`，时间是 Unix 毫秒；`period` 是秒，`dim_0` 等是 `维度名,维度值`。不要传原始 HTTP 参数 `from` / `dim.0`。
- 批量指标使用 `body` 下的 SDK 模型字段；先检查工具 schema，不能照搬另一个 API 的参数。
- 告警规则：`ListAlarmRules` → `ListAlarmRulePolicies` / `ListAlarmRuleResources`；历史事件：`ListAlarmHistories`。规则存在不代表事故时触发过。
- 此仓库同时路由 CES v1 指标与 v2 告警 API，调用方无需选择版本，版本固定在工具目录中。
- 说明聚合粒度、过滤方式、数据延迟与缺失点；空结果不能直接等同正常，先核对维度、时间单位和聚合周期。
- 与 DCS/CCE/RocketMQ 实例 ID 或 LTS 日志关联时，只调用当前确实连接的工具；指标相关性不直接证明根因。

## 边界与交付

- 不新增、修改、删除告警，不发送监控数据，不执行 Agent 任务，也不更改通知屏蔽策略。
- 仓库仅注册明确选择的只读接口，不提供写操作开关。Skill 指令不能替代 IAM/RBAC 权限限制。
- 不要求用户在聊天中提供密钥，不读取本地凭证文件，也不输出身份凭证。查询结果中的业务 key、连接地址和用户信息只在定位必需时做最小展示。
- 区分观察事实、推测和未知；返回目标、时间窗、关键计数、代表证据及请求 ID。空列表不是系统正常的充分证据，先核对分页、权限、地域及指标延迟。
- 身份配置见 [references/identity.md](references/identity.md)；工具名和版本见 [references/tools.md](references/tools.md)；示例见 [examples/prompts.md](examples/prompts.md)。
