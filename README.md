# AWS MFA Tools

![MIT License](https://img.shields.io/pypi/l/aws-mfa-tools)
![Package Version](https://img.shields.io/pypi/v/aws-mfa-tools)
![Python Version](https://img.shields.io/pypi/pyversions/aws-mfa-tools)

- [Usage](#usage)
- [AWS Files](#aws-files)
- [Requirements](#requirements)
- [Install](#install)

---

Command-line tool for MFA authentication for the AWS CLI.

Manages the AWS credentials file to be used with the AWS CLI under MFA authentication and will, by default, ask for the MFA token for the `default` profile (you must add MFA serial to AWS config file).

You **must have** valid authentication for AWS CLI already set up to successfully call the AWS STS. The authentication file is similar to the AWS credentials file and must be located in the same folder.

The tool will generate temporary credential accesses and manage them on the AWS credentials file.

---

## Usage

```text
usage: awslogin [options]

AWS MFA Tool

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --profile PROFILE     aws profile to get mfa serial. (default: default)
  --token TOKEN         mfa token to login. (default: None)
  --config CONFIG_FILE  path to aws config file. (default: <path to>/.aws/config)
  --mfa MFA_FILE        path to mfa credentials file. (default: <path to>/.aws/mfa_credentials)
  --aws AWS_FILE        path to aws credentials file. (default: <path to>/.aws/credentials)
  --export              show export command, does NOT update credentials file.(default: False)
  --list                list all profiles on AWS folder. (default: False)

Helping manage AWS Session tokens for MFA authentication.
```

---

## AWS Files

The AWS CLI uses two files for configuration (`config`) and authentication (`credentials`), and they must be located under the path `~/.aws` (Linux and MAC) or `c:\~\.aws` (Windows). The `~` indicates the path to the user's home folder.

The tool will create and maintain the `credentials` file with temporary access granted via MFA authentication. The expiration time for the session token will be the default one defined by AWS Security Token Service ([to know more](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html)).

To use this tool, you will need to create a `config` file with your `mfa_serial` identification and a `mfa_credentials` file with your access keys to the AWS account where `mfa_serial` is configured.

The default path to all three files can be check using `awslogin -h`. If needed, it is possible to specify the path for each file, check the optional arguments.

Example for a `config` file with profiles:

```text
[default]
region = us-east-1
output = json

[company]
mfa_serial = arn:aws:iam::000000000000:mfa/user.name
region = eu-west-1
output = json

[datalake]
mfa_serial = arn:aws:iam::888888888888:mfa/user.name
region = us-east-2
output = json
```

Example for a `mfa_credentials` file with profiles:

```text
[default]
aws_access_key_id = *******
aws_secret_access_key = *******

[company]
aws_access_key_id = *******
aws_secret_access_key = *******

[datalake]
aws_access_key_id = *******
aws_secret_access_key = *******
```

The `credentials` file will be maintained by the tool and will have something similar to this:

```text
[default]
aws_access_key_id = ********
aws_secret_access_key = *******
aws_session_token = *******
aws_session_token_expiration = <datetime>

[company]
aws_access_key_id = ********
aws_secret_access_key = *******
aws_session_token = *******
aws_session_token_expiration = <datetime>

[datalake]
aws_access_key_id = *******
aws_secret_access_key = *******
aws_session_token = *******
aws_session_token_expiration = <datetime>
```

---

## Requirements

- `Python 3.7+`
- `AWS CLI installed` ([instructions](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html))
- `MFA enabled on AWS account` ([instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html))
- `Access keys to AWS account` ([instructions](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys))

---

## Install

You can use `pip` to install:

```shell
pip3 install aws-mfa-tools
```

You can install directly from Github:

```shell
pip3 install --user git+https://github.com/FerrariDG/aws-mfa-tools.git
```

Or you can clone the repository:

```shell
pip3 install --user <full path to>/aws-mfa-tools
```
