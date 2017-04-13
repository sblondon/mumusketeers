import os
import shutil

import pytest
import yzodb

import web.application
import web.settings
import webtest


@pytest.fixture(scope="module", autouse=True)
def yzodb_fixture():
    yzodb.make_connection_pool()


@pytest.fixture(scope="session", autouse=True)
def persistent_dir_fixture():
    os.makedirs(web.settings.LOGS_DIR)
    os.makedirs(web.settings.BLOBS_DIR)
    os.makedirs(web.settings.FILES_ROOT_DIR)
    yield
    shutil.rmtree(web.settings.PERSISTENT_DIR)


@pytest.fixture(scope="session")
def testapp():
    return webtest.TestApp(web.application.make())

