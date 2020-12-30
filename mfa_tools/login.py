"""Tool to get AWS credentials from AWS STS when MFA is required to AWS CLI."""
from configparser import ConfigParser
from typing import (
    Dict,
    Optional
)
from os.path import (
    expanduser,
    join
)
from sys import (
    exit,
    stderr
)

import argparse
import json
import os
import subprocess


__version__ = "0.1.0"


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

    # Delete any AWS Session Token in place
    env_vars = os.environ.copy()
    if "AWS_SESSION_TOKEN" in env_vars:
        del env_vars["AWS_SESSION_TOKEN"]

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


def export_credentials(aws_profile: str, aws_credentials: Dict[str, str], credentials_file: str) -> None:
    """Export the session credentials to the AWS credential file.

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

    aws_file[aws_profile] = {
        "AWS_ACCESS_KEY_ID": aws_credentials["AccessKeyId"],
        "AWS_SECRET_ACCESS_KEY": aws_credentials["SecretAccessKey"],
        "AWS_SESSION_TOKEN": aws_credentials["SessionToken"]
    }

    with open(credentials_file, "w") as f:
        aws_file.write(f)

    print(f"AWS credentials file {credentials_file} for profile {aws_profile} updated.")


def parse_args() -> argparse.Namespace:
    """Create argument parser.

    Returns
    -------
    argparse.Namespace
        object with arguments and values.
    """
    config_file = join(expanduser("~"), ".aws", "config")
    mfa_file = join(expanduser("~"), ".aws", "mfa_credentials")
    aws_file = join(expanduser("~"), ".aws", "credentials")

    parser = argparse.ArgumentParser(
        prog="aws-mfa-login",
        description="AWS MFA Tool",
        usage="%(prog)s [options]",
        epilog="Helping manage AWS Session tokens for MFA authentication.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
        )
    parser.add_argument(
        "--profile",
        default="default",
        help="aws profile to get mfa serial."
        )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="mfa token to login."
    )
    parser.add_argument(
        "--config",
        type=str,
        metavar="CONFIG_FILE",
        default=config_file,
        help="path to aws config file."
    )
    parser.add_argument(
        "--mfa",
        type=str,
        metavar="MFA_FILE",
        default=mfa_file,
        help="path to mfa credentials file."
    )
    parser.add_argument(
        "--aws",
        type=str,
        metavar="AWS_FILE",
        default=aws_file,
        help="path to aws credentials file."
    )
    parser.add_argument(
        "--export",
        action="store_true",
        default=False,
        help="show export command, does NOT update credentials file."
    )

    return parser.parse_args()


def main():
    """Process credentials request."""
    args = parse_args()

    credentials = get_aws_credentials(args.profile, args.config, args.mfa, args.token)

    if args.export:
        print(f"export AWS_ACCESS_KEY_ID={credentials['AccessKeyId']}")
        print(f"export AWS_SECRET_ACCESS_KEY={credentials['SecretAccessKey']}")
        print(f"export AWS_SESSION_TOKEN={credentials['SessionToken']}")
    else:
        export_credentials(args.profile, credentials, args.aws)


if __name__ == "__main__":
    main()
