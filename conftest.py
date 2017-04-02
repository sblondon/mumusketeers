import pytest
import yzodb


@pytest.fixture(scope="module", autouse=True)
def yzodb_fixture():
    yzodb.make_connection_pool()

