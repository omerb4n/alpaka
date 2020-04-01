from androguard.core.analysis.analysis import ClassAnalysis

# Packages found at https://developer.android.com/reference/packages.html
ANDROID_PACKAGES = ["Landroid/", "Lcom/android/internal/util", "Ldalvik/", "Ljava/", "Ljavax/", "Lorg/apache/",
                    "Lorg/json/", "Lorg/w3c/dom/", "Lorg/xml/sax", "Lorg/xmlpull/v1/", "Ljunit/"]
CUSTOM_ANDROID_PACKAGES = ANDROID_PACKAGES + ["Landroidx/", "[Landroidx/"]


def android_class_filter(class_name_prefix: str, _class_analysis: ClassAnalysis):
    for candidate in CUSTOM_ANDROID_PACKAGES:
        if class_name_prefix.startswith(candidate):
            return False
    return True


def myapplication_filter(k: str, v):
    if k.startswith('Lcom/example/myapplication'):
        return True
    return False
