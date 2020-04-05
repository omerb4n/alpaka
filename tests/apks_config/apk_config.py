import os

from tests.conftest import AG_SESSIONS_PATH


class ApkConfig:
    def __init__(self, apk_dir: str, apk_name: str):
        self.apk_path = os.path.join(apk_dir, f'{apk_name}.apk')
        self.session_path = os.path.join(AG_SESSIONS_PATH, f'{apk_name}.ag')
