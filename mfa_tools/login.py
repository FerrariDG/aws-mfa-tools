"""Tool to get AWS credentials from AWS STS when MFA is required to AWS CLI."""
from configparser import ConfigParser
from typing import (
    Dict,
    Optional
)

from sys import (
    exit,
    stderr
)

import json
import os
import subprocess


def get_aws_credentials(
    aws_profile: str,
    aws_config_file: str,
    mfa_credentials_file: str,
    aws_mfa_token: Optional[str] = None
) -> Dict[str, str]:
    """Get AWS credentials for a given profile.

    Parameters
    ----------
    aws_profile : str
        Profile name in the AWS config/mfa files.
    aws_config_file : str
        AWS config file with MFA serial for the profile.
    mfa_credentials_file : str
        MFA credentials file to access AWS STS for the profile.
    aws_mfa_token : Optional[str], optional
        MFA token for AWS STS, by default None (it will be asked).

    Returns
    -------
    Dict[str, str]
        AWS Session credentials for the profile.
    """
    config = ConfigParser()
    config.read(aws_config_file)

    try:
        profile = config[aws_profile]
    except KeyError:
        print(f"AWS profile {aws_profile} not found at {aws_config_file}.", file=stderr)
        exit(-1)

    try:
        mfa_serial = profile["mfa_serial"]
    except KeyError:
        print(f"AWS profile {aws_profile} does not have mfa_serial configured at {aws_config_file}", file=stderr)
        exit(-1)

    mfa_token = input(f"MFA token for profile {aws_profile}: ") if aws_mfa_token is None else aws_mfa_token

    # Delete any AWS environment variable in place
    env_vars = os.environ.copy()
    for key in env_vars.keys():
        if key.startswith("AWS_"):
            del env_vars[key]

    # AWS credentials file with access keys for the profile MFA
    env_vars["AWS_SHARED_CREDENTIALS_FILE"] = mfa_credentials_file

    # Get the session token
    proc = subprocess.Popen(
        [
            "aws", "sts", "get-session-token",
            "--profile", aws_profile,
            "--serial-number", mfa_serial,
            "--token-code", mfa_token
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env_vars
    )
    data, _ = proc.communicate()
    if proc.returncode != 0:
        print(f"Get session token for profile {aws_profile} failed: {data.decode('utf-8')}.", file=stderr)
        exit(-1)

    # Get temporary credentials
    credentials = json.loads(data.decode("utf-8"))["Credentials"]
    return credentials


def save_credentials(aws_profile: str, aws_credentials: Dict[str, str], credentials_file: str) -> None:
    """Save the session credentials into the AWS credential file.

    Parameters
    ----------
    aws_profile : str
        AWS profile name in the credentials file.
    aws_credentials : Dict[str, str]
        AWS Session credentials for the profile.
    credentials_file : str
        AWS credentials file location.
    """
    aws_file = ConfigParser()
    aws_file.read(credentials_file)
    aws_file[aws_profile] = aws_credentials

    with open(credentials_file, "w") as f:
        aws_file.write(f)

    print(f"AWS credentials file {credentials_file} for profile {aws_profile} updated.")
