import re
from alpaka.apk.class_info import ClassInfo

# Packages found at https://developer.android.com/reference/packages.html

ANDROID_PACKAGES = ["Landroid/", "Lcom/android/internal/util", "Ldalvik/", "Ljava/", "Ljavax/", "Lorg/apache/",
                    "Lorg/json/", "Lorg/w3c/dom/", "Lorg/xml/sax", "Lorg/xmlpull/v1/", "Ljunit/"]
CUSTOM_ANDROID_PACKAGES = ANDROID_PACKAGES + ["Landroidx/", "[Landroidx/"]

PRIMITIVE_CLASS_REGEX = re.compile(r'^\[*[Z|B|C|D|F|I|J|S]$')


def primitive_class_filter(class_name_prefix: str, _class_info: ClassInfo):
    """
    This will filter classes like '[I', 'I', 'B' etc.
    See https://docs.oracle.com/javase/7/docs/api/java/lang/Class.html#getName() for more information
    :param class_name_prefix:
    :param _class_info:
    :return:
    """
    return PRIMITIVE_CLASS_REGEX.match(class_name_prefix) is None


def android_class_filter(class_name_prefix: str, class_info: ClassInfo):
    if class_info.analysis.is_external():
        return False
    for candidate in CUSTOM_ANDROID_PACKAGES:
        if class_name_prefix.startswith(candidate):
            return False
    return primitive_class_filter(class_name_prefix, class_info)


def myapplication_filter(k: str, v):
    if k.startswith('Lcom/example/myapplication'):
        return True
    return False
