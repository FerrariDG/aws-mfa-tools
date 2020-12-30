from setuptools import (
    find_packages,
    setup
)


setup(
    name="aws-mfa-tools",
    version="0.0.1",
    packages=find_packages(),
    author="Daniel Ferrari",
    description="AWS MFA tools to be used on command line.",
    license="MIT",
    keywords="aws cli mfa login",
    url="https://github.com/FerrariDG/aws-mfa-tools",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7"
    ],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "awslogin=mfa_tools.login:main"
        ]
    },
    python_requires=">=3.7"
)
