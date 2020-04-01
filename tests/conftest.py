import os
from typing import Type, Any, Callable
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from alpaka.apk.analyzed_apk import AnalyzedApk

TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), "test_files")
APKS_PATH = os.path.join(TEST_FILES_PATH, "apks")
AG_SESSIONS_PATH = os.path.join(TEST_FILES_PATH, "ag_sessions")

TOAST_APKS_PATH = os.path.join(APKS_PATH, 'toastAPK')
TOAST_HELLO_APK_PATH = os.path.join(TOAST_APKS_PATH, 'hello.apk')
TOAST_HELLO_SESSION_PATH = os.path.join(AG_SESSIONS_PATH, 'hello.ag')
TOAST_BYE_APK_PATH = os.path.join(TOAST_APKS_PATH, 'bye.apk')
TOAST_BYE_SESSION_PATH = os.path.join(AG_SESSIONS_PATH, 'bye.ag')


def mock_function(monkeypatch: MonkeyPatch, target: Type[Any], function: Callable, side_effect: Callable = None):
    mock = Mock(side_effect=side_effect)
    monkeypatch.setattr(target, function.__name__, mock)


@pytest.fixture(scope='session')
def hello_analyzed_apk_fixture() -> AnalyzedApk:
    return AnalyzedApk(TOAST_HELLO_APK_PATH, session_path=TOAST_HELLO_SESSION_PATH)


@pytest.fixture(scope='session')
def hello_apk_classes_fixture(hello_analyzed_apk_fixture):
    return hello_analyzed_apk_fixture.analysis.classes
