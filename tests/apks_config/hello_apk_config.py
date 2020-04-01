import os

import pytest
from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from tests.conftest import TOAST_APKS_PATH, AG_SESSIONS_PATH

TOAST_HELLO_APK_PATH = os.path.join(TOAST_APKS_PATH, 'hello.apk')
TOAST_HELLO_SESSION_PATH = os.path.join(AG_SESSIONS_PATH, 'hello.ag')

MAIN_APPLICATION_PACKAGE = 'Lcom/example/myapplication'
MAIN_ACTIVIY = 'Lcom/example/myapplication/MainActivity;'


@pytest.fixture(scope='session')
def hello_analyzed_apk_fixture() -> AnalyzedApk:
    return AnalyzedApk(TOAST_HELLO_APK_PATH, session_path=TOAST_HELLO_SESSION_PATH)


@pytest.fixture(scope='session')
def hello_apk_classes_fixture(hello_analyzed_apk_fixture):
    return hello_analyzed_apk_fixture.analysis.classes


@pytest.fixture(scope='function')
def main_activity_class_fixture(hello_apk_classes_fixture) -> ClassAnalysis:
    return hello_apk_classes_fixture["Lcom/example/myapplication/MainActivity;"]