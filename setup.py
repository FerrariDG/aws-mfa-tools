from setuptools import (
    find_packages,
    setup
)

__version__ = "0.2.2"

with open("mfa_tools/version.py", "w") as f:
    f.write(f"VERSION = '{__version__}'")


setup(
    name="aws-mfa-tools",
    version=__version__,
    packages=find_packages(),
    author="Daniel Ferrari",
    description="AWS MFA tools to be used on command line.",
    license="MIT",
    keywords="aws cli mfa login",
    url="https://github.com/FerrariDG/aws-mfa-tools",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Software Development :: Build Tools",
        "Typing :: Typed"
    ],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "awslogin=mfa_tools.main:main"
        ]
    },
    python_requires=">=3.7"
)
