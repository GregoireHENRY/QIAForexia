"""
Conftest for pytest
"""

import os

import yaml


def pytest_configure():
    """Script that runs before all test of pytest."""

    print("Connection to xStation account..")

    # Account ID and password can be written hard in account.yaml or given in
    # environment variables or entered by user input
    with open(r"account.yaml") as file:
        account = yaml.full_load(file)

    if account.get("ACCOUNT"):
        os.environ["XTB_ACCOUNT"] = str(account["ACCOUNT"])
    if account.get("PASSWORD"):
        os.environ["XTB_PASSWORD"] = account["PASSWORD"]
