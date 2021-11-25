from setuptools import (
    find_packages,
    setup
)


setup(
    name="aws-mfa-tools",
    version="0.2.0",
    packages=find_packages(),
    author="Daniel Ferrari",
    description="AWS MFA tools to be used on command line.",
    license="MIT",
    keywords="aws cli mfa login",
    url="https://github.com/FerrariDG/aws-mfa-tools",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Topic :: Software Development :: Build Tools"
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
