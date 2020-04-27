from alpaka.apk.class_pool import PackagesDict
from alpaka.apk.package_info import PackageInfo
from alpaka.matching.base import Match, Matcher, MatchingResult


class NameBasedPackageMatcher(Matcher[PackageInfo]):

    """
    Matches packages with the same name from 2 package pools
    """

    @classmethod
    def match(cls, pool1: PackagesDict, pool2: PackagesDict) -> MatchingResult[PackageInfo]:
        pool1 = dict(pool1)
        pool2 = dict(pool2)
        matches = dict()
        for package_key, package_info in dict(pool1).items():
            if package_info.is_obfuscated_name:
                continue
            matching_package = pool2.get(package_key)
            if matching_package is not None:
                if matching_package.is_obfuscated_name:
                    continue
                matches[package_key] = [Match(package_info, matching_package, 0.0)]
                del pool1[package_key]
                del pool2[package_key]
        return MatchingResult(matches, (pool1, pool2))
