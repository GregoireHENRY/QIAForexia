"""
QIAForexia main test
"""

# pylint: disable=invalid-name

import os
import sys

import QIAForexia.kit as kit
from QIAForexia import QIAForexia


def test_main() -> None:
    """QIAForexia main test"""

    # Get identifiants
    if os.environ.get("XTB_ACCOUNT"):
        if kit.represent_int(os.environ["XTB_ACCOUNT"]):
            account = int(os.environ["XTB_ACCOUNT"])
        else:
            sys.exit("Error: XTB_ACCOUNT variable is not an integer")
    else:
        sys.exit("Error: set XTB_ACCOUNT envionment variables")

    if os.environ.get("XTB_PASSWORD"):
        password = os.environ["XTB_PASSWORD"]
    else:
        sys.exit("Error: set XTB_PASSWORD envionment variables")

    # Start
    QIAForexia.start(account, password)
