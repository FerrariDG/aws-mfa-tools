"""Module to print AWS profiles."""
from configparser import ConfigParser
from datetime import datetime

from typing import Tuple


def get_token_expiration(parser: ConfigParser, profile: str) -> Tuple[str, str]:
    """Return token expiration date and whether it is expired.

    Parameters
    ----------
    parser : ConfigParser
        Parser with all configuration files.
    profile : str
        Profile name.

    Returns
    -------
    Tuple[str, str]
        Tuple with expiration date and whether it is expired.
    """
    expiration = parser.get(profile, 'aws_session_token_expiration', fallback=None)

    if expiration is None:
        return "", ""

    dt = datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S%z")

    expired = "N" if dt > datetime.now(dt.tzinfo) else "Y"

    return f"{dt:%Y-%m-%d %H:%M:%S}", expired


def has_configured(parser: ConfigParser, profile: str, parameter: str) -> str:
    """Return whether a parameter is configured.

    Parameters
    ----------
    parser : ConfigParser
        Parser with all configuration files.
    profile : str
        Profile name.
    parameter : str
        Parameter name.

    Returns
    -------
    str
        Whether the parameter is configured.
    """
    return "N" if parser.get(profile, parameter, fallback=None) is None else "Y"


def print_profiles(config_file: str, mfa_file: str, credentials_file: str) -> None:
    """Print all profiles and data related.

    Parameters
    ----------
    config_file : str
        AWS configuration file.
    mfa_file : str
        MFA credentials file.
    credentials_file : str
        AWS credentials file.
    """
    config = ConfigParser()
    config.read(config_file)

    mfa = ConfigParser()
    mfa.read(mfa_file)

    credentials = ConfigParser()
    credentials.read(credentials_file)

    profiles = sorted(set(config.sections() + mfa.sections() + credentials.sections()))

    print("")
    print(
        f"|{'Profile name':^22}|{'Region':^11}|{'MFA':^5}|{'AccessKey':^11}" +
        f"|{'Token':^7}|{'Expiration':^21}|{'Expired':^9}|"
    )
    print(f"|{'-' * 22}|{'-' * 11}|{'-' * 5}|{'-' * 11}|{'-' * 7}|{'-' * 21}|{'-' * 9}|")

    for profile in profiles:
        region = config.get(profile, "region", fallback=None)
        has_mfa = has_configured(config, profile, "mfa_serial")
        has_key = has_configured(mfa, profile, "aws_access_key_id")
        has_token = has_configured(credentials, profile, "aws_session_token")
        expiration, expired = get_token_expiration(credentials, profile)

        print(f"| {profile:21}|{region:^11}|{has_mfa:^5}|{has_key:^11}|{has_token:^7}|{expiration:^21}|{expired:^9}|")

    print("")
