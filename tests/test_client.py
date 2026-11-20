from huawei_ces_mcp.client import build_client
from huawei_ces_mcp.config import CesConfig, CesScope
from huawei_ces_mcp.service import VERSIONS, client_class


def test_sdk_client_builds_for_each_supported_version_without_network():
    config = CesConfig(access_key="ak-placeholder", secret_key="sk-placeholder")
    scope = CesScope(region="cn-north-4", project_id="project-placeholder")
    for version in VERSIONS:
        assert isinstance(build_client(config, scope, version), client_class(version))
