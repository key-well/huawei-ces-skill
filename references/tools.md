# 已注册工具

工具使用 SDK 参数名，具体字段以 MCP 实际返回的 inputSchema 为准。以下 22 个接口均为显式选择的只读查询，不按名称前缀动态放行其他接口。

| 工具 | SDK 版本 | 用途 |
|---|---|---|
| `ListMetrics` | `v1` | 查询指标列表（只读查询） |
| `ShowMetricData` | `v1` | 查询监控数据（只读查询） |
| `BatchListMetricData` | `v1` | 批量查询监控数据（只读查询） |
| `ListAlarms` | `v1` | 查询告警规则列表（只读查询） |
| `ShowAlarm` | `v1` | 查询单条告警规则信息（只读查询） |
| `ListEvents` | `v1` | 查询事件监控列表（只读查询） |
| `ListEventDetail` | `v1` | 查询某一事件监控详情（只读查询） |
| `ShowEventData` | `v1` | 查询主机配置数据（只读查询） |
| `ListResourceGroup` | `v1` | 查询所有资源分组（只读查询） |
| `ListAlarmRules` | `v2` | 查询告警规则列表(推荐)（只读查询） |
| `ListAlarmHistories` | `v2` | 查询告警记录列表（只读查询） |
| `ListAlarmRulePolicies` | `v2` | 查询告警规则策略列表（只读查询） |
| `ListAlarmRuleResources` | `v2` | 查询告警规则资源列表（只读查询） |
| `ListAlarmTemplates` | `v2` | 查询告警模板列表（只读查询） |
| `ShowAlarmTemplate` | `v2` | 查询告警模板详情（只读查询） |
| `ListResourceGroups` | `v2` | 查询资源分组列表（只读查询） |
| `ShowResourceGroup` | `v2` | 查询指定资源分组详情（只读查询） |
| `ListDashboardInfos` | `v2` | 查询监控看板列表（只读查询） |
| `ListDashboardWidgets` | `v2` | 查询指定监控看板下的监控视图列表（只读查询） |
| `ShowWidget` | `v2` | 查询指定监控视图信息（只读查询） |
| `ListNotificationMasks` | `v2` | 查询告警通知屏蔽列表（只读查询） |
| `ListNotificationMaskResources` | `v2` | 查询告警通知屏蔽资源列表（只读查询） |

操作名称/简介来源及固定版本见根目录 NOTICE；详细字段由官方 SDK 生成。工具能被列出仅代表 MCP 启动正常，不能证明地域支持、云权限或实际业务结果。
