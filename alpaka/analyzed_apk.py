import os

from androguard.core.analysis.analysis import Analysis
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.misc import AnalyzeAPK, get_default_session
from androguard import session


class AnalyzedApk:
    def __init__(self, apk_path: str, session_path: str = None):
        self._path = os.path.abspath(apk_path)
        self._filename = os.path.basename(self._path)
        self._session_path = session_path

        results = self._analyze_apk()
        self.apk: APK = results[0]
        self.dalvik_vm_format: DalvikVMFormat = results[1]
        self.analysis: Analysis = results[2]

    def _analyze_apk(self):
        sess = None
        if self._session_path:
            sess = get_default_session()
            if os.path.isfile(self._session_path):
                # Session exists
                sess = session.Load(self._session_path)
                return sess.get_objects_apk(filename=self._path)

        analayzed_apk = AnalyzeAPK(self._path, session=sess)
        if sess:
            session.Save(sess, self._session_path)
        return analayzed_apk
