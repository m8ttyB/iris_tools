#!/usr/bin/python
# A quick script that outputs the necessary pypi package information for
# releng bugs. The outputs can be redirected to a text file and then given
# to releng for upload to Mozilla's internal pypi mirror


import sys

import hashin
from pprint import pprint


PYTHON37 = ['py3', 'py2.py3', 'cp37']

# TODO have method use get_pkg_name_and_version() to populate a dictionary
def get_requirements_from_file(file):
    requirements_file = open(file)
    packages = []
    for requirement in requirements_file:
        # TODO skip commented out requirements
        # TODO handle unpinned requirements?
        if '#' not in requirement[0]:
            # in a small number of isntances remove the new-line char
            requirement = requirement.strip("\n")
            pkg = requirement.split('==')[0]


def get_pkg_names_and_versions(pkgs):
    pkg_name_version_dict = {}
    for pkg in pkgs:
        pkg_name = pkg.split('==')[0]
        version = pkg.split('==')[1]
        pkg_name_version_dict[pkg] = {'name': pkg_name, 'version': version}
    return pkg_name_version_dict


# TODO update method name to something more useful.
def get_pkg_hashes(requirements_file):
    requirements = open(requirements_file)
    pkg_data = {}
    for requirement in requirements:
        # skip commented out requirements
        # TODO handle unpinned requirements?
        if '#' not in requirement[0]:
            requirement = requirement.strip("\n")
            pkg = requirement.split('==')[0]
            pkg_data[requirement]= hashin.get_package_data(pkg, "https://pypi.org/simple")
    return pkg_data


def get_whl_and_hash(pkg_name, releases, python_version=PYTHON37):
    for release in releases:
        version =  release['python_version']
        if 'bdist_wheel' == release['packagetype'] and  version in python_version:
            pprint(pkg_name)
            print(version)
            print(release['url'])
            print('SHA256: %s' % release['digests']['sha256'])
            print()
        else:
            # TODO capture if a bdist isn't available
            pass


if __name__ == "__main__":
    print('.... collecting URIs and hashes')
    requirements_file = sys.argv[1]
    pkg_hash_dict = get_pkg_hashes(requirements_file)
    pkgs = pkg_hash_dict.keys()
    pkgs_and_versions = get_pkg_names_and_versions(pkgs)

    count = 0
    for pkg_key in pkgs_and_versions.keys():
        pkg = pkg_hash_dict[pkg_key]
        release = pkg['releases'][pkgs_and_versions[pkg_key]['version']]
        get_whl_and_hash(pkg_key, release)
        count+=1
    print('pkg count gathered from requirements file[%s]: %s' % (sys.argv[1], len(pkgs)))
    print('Final hash match count: %s' % count)
