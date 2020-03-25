NAME_SEPARATOR = '/'


class PackageInfo:

    def __init__(self, package_name_prefix: str, is_obfuscated_name):
        self.name_prefix = package_name_prefix
        self.classes = []
        self.is_obfuscated_name = is_obfuscated_name

    def add_class(self, class_name: str):
        self.classes.append(class_name)

    def get_classes(self):
        return self.classes

    @staticmethod
    def get_parent_package_name_prefix(package_name_prefix):
        return package_name_prefix[:package_name_prefix.rfind(NAME_SEPARATOR)]

    @staticmethod
    def get_package_name(package_name_prefix):
        return package_name_prefix[package_name_prefix.rfind(NAME_SEPARATOR) + 1:]

    def __repr__(self):
        return "~Obfuscated" if self.is_obfuscated_name else ""
