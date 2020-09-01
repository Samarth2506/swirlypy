#!/usr/bin/env python3

import subprocess, os
from setuptools import setup

print("Obtaining version... ", end="")
try:
    version = subprocess.check_output(["git", "describe", "--dirty=+"],
            universal_newlines=True)
except subprocess.CalledProcessError as e:
    version = "0.0.1"
print(version)

setup(name='swirlypy',
        version=version,
        description='Python courseware',
        author='Alexander Bauer/Samarth',
        author_email='samarthmc@gmail.com',
        url='https://github.com/Samarth2506/swirlypy',
        include_package_data=True,
        download_url = 'https://github.com/Samarth2506/swirlypy/archive/0.0.1.tar.gz',
        scripts=['swirlypy/run_swirlypy'],
        packages=['swirlypy', 'swirlypy.questions','courses'],
        install_requires=['pyyaml','numpy', 'pandas', 'sklearn','tqdm'],
        )
