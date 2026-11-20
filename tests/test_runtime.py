from dataclasses import replace
import pytest
from huawei_ces_mcp.catalog import TOOL_BY_NAME
from huawei_ces_mcp.config import CesConfig
from huawei_ces_mcp.runtime import invoke_tool


def config():
    return CesConfig(access_key="ak-placeholder", secret_key="sk-placeholder",
        region="cn-north-4", project_id="project-placeholder")


@pytest.mark.asyncio
async def test_scope_override_and_sdk_routing_use_fake_client():
    spec = TOOL_BY_NAME['ListMetrics']
    seen = {}
    class Client:
        def __getattr__(self, name):
            assert name == spec.sdk_method
            def query(request):
                assert request.__class__.__name__ == spec.request_class
                return {"items": []}
            return query
    def factory(conf, scope, version):
        seen["scope"] = scope
        assert version == spec.api_version
        return Client()
    result = await invoke_tool(spec, {"region": "cn-east-3", "project_id": "project-override"},
        config=config(), client_factory=factory)
    assert seen["scope"].project_id == "project-override"
    assert seen["scope"].region == "cn-east-3"
    assert result == {"items": []}


@pytest.mark.asyncio
@pytest.mark.parametrize("arguments", [{"not_a_parameter": "private-value"}, {"region": ""}])
async def test_invalid_arguments_fail_before_network_without_echoing_value(arguments):
    def fail(*args):
        raise AssertionError("unexpected network factory")
    with pytest.raises(ValueError) as raised:
        await invoke_tool(TOOL_BY_NAME['ListMetrics'], arguments, config=config(), client_factory=fail)
    assert "private-value" not in str(raised.value)


@pytest.mark.asyncio
async def test_unregistered_or_modified_tools_cannot_run():
    spec = replace(TOOL_BY_NAME['ListMetrics'], sdk_method="delete_instance")
    with pytest.raises(ValueError, match="read-only catalog"):
        await invoke_tool(spec, {}, config=config())


@pytest.mark.asyncio
async def test_missing_resource_or_time_parameters_fail_before_network():
    def fail(*args):
        raise AssertionError("unexpected network factory")
    with pytest.raises(ValueError, match="schema rule required"):
        await invoke_tool(TOOL_BY_NAME["ShowMetricData"], {}, config=config(), client_factory=fail)
