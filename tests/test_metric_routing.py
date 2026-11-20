import pytest
from huaweicloudsdkces.v1 import MetricInfo
from huawei_ces_mcp.catalog import TOOL_BY_NAME
from huawei_ces_mcp.config import CesConfig
from huawei_ces_mcp.runtime import invoke_tool
from huawei_ces_mcp.schema import model_schema
from huaweicloudsdkces.v1 import BatchPeriod, Filter


@pytest.mark.asyncio
async def test_batch_metrics_builds_nested_v1_models():
    class Client:
        def batch_list_metric_data(self, request):
            assert request.body._from == 1700000000000
            assert isinstance(request.body.metrics[0], MetricInfo)
            assert request.body.metrics[0].dimensions[0].name == "instance_id"
            assert request.body.period == "60"
            return {"metrics": []}
    def factory(config, scope, version):
        assert version == "v1"
        return Client()
    result = await invoke_tool(TOOL_BY_NAME["BatchListMetricData"], {"body": {
        "metrics": [{"namespace": "SYS.DCS", "metric_name": "metric-placeholder",
            "dimensions": [{"name": "instance_id", "value": "instance-placeholder"}]}],
        "_from": 1700000000000, "to": 1700000060000, "period": "60", "filter": "average"
    }}, config=CesConfig(access_key="ak-placeholder", secret_key="sk-placeholder",
        region="cn-north-4", project_id="project-placeholder"), client_factory=factory)
    assert result == {"metrics": []}


@pytest.mark.asyncio
async def test_alarm_queries_route_to_v2():
    class Client:
        def list_alarm_rules(self, request):
            assert request.limit == 5
            return {"alarms": []}
    def factory(config, scope, version):
        assert version == "v2"
        return Client()
    assert await invoke_tool(TOOL_BY_NAME["ListAlarmRules"], {"limit": 5},
        config=CesConfig(access_key="ak-placeholder", secret_key="sk-placeholder",
            region="cn-north-4", project_id="project-placeholder"),
        client_factory=factory) == {"alarms": []}


def test_sdk_enum_models_are_scalar_schemas():
    assert model_schema(Filter, "v1")["type"] == "string"
    assert "average" in model_schema(Filter, "v1")["enum"]
    assert "60" in model_schema(BatchPeriod, "v1")["enum"]


@pytest.mark.asyncio
async def test_batch_metrics_requires_a_body_before_calling_sdk():
    with pytest.raises(ValueError, match="schema rule required"):
        await invoke_tool(TOOL_BY_NAME["BatchListMetricData"], {},
            config=CesConfig(access_key="ak-placeholder", secret_key="sk-placeholder",
                region="cn-north-4", project_id="project-placeholder"))
