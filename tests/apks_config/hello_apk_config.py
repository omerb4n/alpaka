import pytest
from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from tests.apks_config.apk_config import ApkConfig
from tests.conftest import TOAST_APKS_PATH

APK_NAME = 'hello'
TOAST_HELLO_APK_CONFIG = ApkConfig(TOAST_APKS_PATH, APK_NAME)

MAIN_APPLICATION_PACKAGE = 'Lcom/example/myapplication'
MAIN_ACTIVIY = 'Lcom/example/myapplication/MainActivity;'


@pytest.fixture(scope='session')
def hello_analyzed_apk_fixture() -> AnalyzedApk:
    return AnalyzedApk(TOAST_HELLO_APK_CONFIG.apk_path, session_path=TOAST_HELLO_APK_CONFIG.session_path)


@pytest.fixture(scope='session')
def hello_apk_classes_fixture(hello_analyzed_apk_fixture):
    return hello_analyzed_apk_fixture.analysis.classes


@pytest.fixture(scope='function')
def main_activity_class_fixture(hello_apk_classes_fixture) -> ClassAnalysis:
    return hello_apk_classes_fixture["Lcom/example/myapplication/MainActivity;"]
