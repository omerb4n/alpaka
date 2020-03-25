from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo


class ApkDiffer:
    def __init__(self, old_apk: AnalyzedApk, new_apk: AnalyzedApk):
        self._old_apk_info = ApkInfo(old_apk)
        self._new_apk_info = ApkInfo(new_apk)

    def filter_classes(self, class_filter):
        self._old_apk_info.filter_classes(class_filter)
        self._new_apk_info.filter_classes(class_filter)

    def pack(self):
        self._old_apk_info.pack()
        self._new_apk_info.pack()
