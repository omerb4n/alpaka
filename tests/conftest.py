import os
from typing import Type, Any, Callable
from unittest.mock import Mock

from _pytest.monkeypatch import MonkeyPatch

TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), "test_files")
APKS_PATH = os.path.join(TEST_FILES_PATH, "apks")
AG_SESSIONS_PATH = os.path.join(TEST_FILES_PATH, "ag_sessions")

TOAST_APKS_PATH = os.path.join(APKS_PATH, 'toastAPK')


def mock_function(monkeypatch: MonkeyPatch, target: Type[Any], function: Callable, side_effect: Callable = None):
    mock = Mock(side_effect=side_effect)
    monkeypatch.setattr(target, function.__name__, mock)
