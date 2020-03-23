import os
from typing import List

from androguard.core.analysis.analysis import Analysis
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.misc import AnalyzeAPK, get_default_session
from androguard import session


class AnalyzedApkNotFoundError(Exception):
    def __init__(self, analyzed_files: List, file_not_found: str):
        super(AnalyzedApkNotFoundError, self).__init__(
            f"file {file_not_found} was not found in the session's analyzed files: {analyzed_files}"
            f"Pay attention that session files store the absolute path of the apk.")


class SessionNotFoundError(Exception):
    def __init__(self, session_path: str):
        super(SessionNotFoundError, self).__init__(f"session file {session_path} was not found")


class AnalyzedApk:
    def __init__(self, apk_path: str, session_path: str = None):
        self._path = os.path.abspath(apk_path)
        self._filename = os.path.basename(self._path)
        self._session_path = session_path

        results = self._analyze_apk()
        self.apk: APK = results[0]
        self.dalvik_vm_format: DalvikVMFormat = results[1]
        self.analysis: Analysis = results[2]

    def _get_analysis_from_session(self):
        if os.path.isfile(self._session_path):
            # Session exists
            sess = session.Load(self._session_path)
            apk_analysis = sess.get_objects_apk(filename=self._path)
            if apk_analysis[0] is None:
                raise AnalyzedApkNotFoundError(list(sess.analyzed_files.keys()), self._path)
            return apk_analysis
        else:
            raise SessionNotFoundError(self._session_path)

    def _analyze_apk(self):
        sess = None
        if self._session_path:
            sess = get_default_session()
            try:
                self._get_analysis_from_session()
            except SessionNotFoundError:
                # Analyze the apk and save the session
                pass

        analayzed_apk = AnalyzeAPK(self._path, session=sess)
        if sess:
            session.Save(sess, self._session_path)
        return analayzed_apk
