from os.path import (
    expanduser,
    join
)

from sys import exit

import argparse

from mfa_tools.list import print_profiles
from mfa_tools.login import (
    get_aws_credentials,
    save_credentials
)


__version__ = "0.2.0"


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
        prog="awslogin",
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
    parser.add_argument(
        "--list",
        action="store_true",
        default=False,
        help="list all profiles on AWS folder."
    )

    return parser.parse_args()


def main():
    """Process credentials request."""
    args = parse_args()

    if args.list:
        print_profiles(args.config, args.mfa, args.aws)
        exit(0)

    credentials = get_aws_credentials(args.profile, args.config, args.mfa, args.token)

    aws_credentials = {
        "AWS_ACCESS_KEY_ID": credentials["AccessKeyId"],
        "AWS_SECRET_ACCESS_KEY": credentials["SecretAccessKey"],
        "AWS_SESSION_TOKEN": credentials["SessionToken"],
        "AWS_SESSION_TOKEN_EXPIRATION": credentials["Expiration"]
    }

    if args.export:
        for key, value in aws_credentials.items():
            print(f"export {key}={value}")
    else:
        save_credentials(args.profile, aws_credentials, args.aws)


if __name__ == "__main__":
    main()
