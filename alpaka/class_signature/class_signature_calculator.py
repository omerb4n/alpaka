from androguard.core.analysis.analysis import ClassAnalysis


class ClassSignatureCalculator:
    def __init__(self, class_analysis):
        self._class_analysis: ClassAnalysis = class_analysis

    def calculate(self):
        """

        :return: ClassSignature
        """
        pass

    def get_member_count(self):
        raise NotImplementedError()

    def get_method_count(self):
        raise NotImplementedError()

    def get_instructions_count(self):
        raise NotImplementedError()

    def get_members_simhash(self):
        raise NotImplementedError()

    def get_methods_params_simhash(self):
        raise NotImplementedError()

    def get_methods_returns_simhash(self):
        raise NotImplementedError()

    def get_instructions_simhash(self):
        raise NotImplementedError()
