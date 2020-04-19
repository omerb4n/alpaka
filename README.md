# alpaka

>APK diff tool

Alpaka is an APK diff tool written in Python 3.

It mainly uses [androguard](https://github.com/androguard) to analyze two apks (usually different versions of the same app), then it indicates any modification that was done between them.

The tool is still in development

#### Obfuscated Apks
Alpaka was built to work even if the APK is obfuscated.
It's up for the user to configure how the obfuscation detectors will work or use the default ones.

## Setup
Alpaka is not yet a Python package but it should be!

Right now in order to use the tool all you need to clone and install the requirements:

`pip3 install -r requirements.txt`

##### Known Errors
- The `simhash-py` package might be problematic if you have a package named `simhash` installed.
If you do have it you should `pip3 uninstall simhash` first.
## Technical overview

Analyzing an APK is easily done by androguard. Alpaka's part is detecting the modifications that were done between the apks.
##### Challenges

- The names and offsets of packages, classes, functions and variables inside the apk can be changed (either by obfuscation or manually by the developer).
    - Thus, in order to detect the modifications that were done on a given class, we first have to find the matching class in the other apk.
    - Furthermore, matching between classes must be done by detecting structural similarities; this method can yield false answers.
- Modern Apks can be pretty big, as a result the diff process must be efficient in memory and computation time.


To overcome the challenges above, alpaka's diff process is constructed from 3 stages:

#### Stage 1: Filtering Classes (Optional)
Finding a class match in a `100,000` classes list can consume a lot of resources, and will probably yield a false answer.
Hence, filtering irrelevant classes from the known classes is very useful and efficient.

- It is always recommended to filter native Java and Android classes.
- The user chooses which classes to filter

#### Stage 2: Matching Classes Pools (Optional)
Looking for a class match is a heavy O(number_of_classes^2) computation, even if the number of classes was reduced by a filter.

It is better to divide the classes in both apks to groups (called pools) that we can easily match.

After dividing the classes into pools, the class matching stage can search for a match in a smaller and targeted group, which will be more efficient and accurate.

##### Dividing To Pools By Packages
Right now the only way to divide to pools is by packages.

Packing the apk will group classes from the same Java package into a package object.
Then package objects can be used as pools and easily matched by name.

Notes:
- In case the package name was indicated as obfuscated by an ObfuscationDetector, it will not be matched. 
- Alpaka lets the user decide whether he wants to pack the APK or not.

### Stage 3: Matching Classes
Matching is done in two steps:
1. Matching by class name (if it's not obfuscated)
2. If the above step did not yield results - matching by class signature.

A class signature is made from structural properties, such as:
- number of methods
- methods return types
- methods parameters types
- number of fields
- class instructions
- ... etc ...

The similarity between classes is determined by the distance between their signatures.

##### How Does a Class Signature Work:
While properties like number of methods can be easily represented and differentiated, other properties, like methods return types and class instructions, are more complex.

Most of the complex properties are represented by a Simhash.
Unlike other hashes, Simhash is one where similar items are hashed to similar hash values.

## Code Examples
```python
def test_facebook_apk():
    old_apk = AnalyzedApk(FACEBOOK_262_0_0_34_117_APK_CONFIG.apk_path, # This will analyze the apk using Androguard
                          session_path=FACEBOOK_262_0_0_34_117_APK_CONFIG.session_path) # androguard session file
    new_apk = AnalyzedApk(FACEBOOK_264_0_0_44_111_APK_CONFIG.apk_path,
                          session_path=FACEBOOK_264_0_0_44_111_APK_CONFIG.session_path)
    
    # Initialize ApkDiffer with custom Obfuscation Detectors (OD)
    apk_differ = ApkDiffer(old_apk, new_apk, FacebookPackageNameOD(), FacebookClassNameOD())
    apk_differ.filter_classes(android_class_filter) # Filter android and java classes (Optional)
    apk_differ.pack() # Dividing To Pools By Packages (Optional)
    apk_differ.find_classes_matches() # Matching Classes
    print(apk_differ.get_classes_matches_json(indent=4)) 
```

The above code will output:
```python
{
    # Matches by name
  "Lcom/facebook/quicksilver/QuicksilverShortcutExternalActivity;": { # Old apk class name
        "Lcom/facebook/quicksilver/QuicksilverShortcutExternalActivity;": 1.0 # the matching class in the new apk
    },
    "Lcom/facebook/redex/ConstantPropagationAssertHandler;": {
        "Lcom/facebook/redex/ConstantPropagationAssertHandler;": 1.0
    },
    # ...
    # Matches by signature
    "LX/009;": { # Old apk class name
        "LX/009;": 5.300000000000001, # Signatures distance
        "LX/0Sn;": 6.5,
        "LX/0JJ;": 6.500000000000001
    },
    "LX/00B;": {
        "LX/00I;": 4.0,
        "LX/0Ql;": 6.300000000000001,
        "LX/0Zh;": 9.000000000000002
    }
    # ...
}
```

## Tests
Some of the tests require large APKs (Facebook, WhatsApp, etc.). These APKs are not included in the default branch.

if you want to test them you should copy them from the '**tests/add_large_apks**' branch.