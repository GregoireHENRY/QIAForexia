"""
QIAForexia library's main.
"""

import os
import sys

import stdiomask
import yaml

import QIAForexia.kit as kit
from QIAForexia import QIAForexia

print("Connection to xStation account..")

# Account ID and password can be written hard in account.yaml or given in
# environment variables or entered by user input
with open(r"account.yaml") as file:
    account_id = yaml.full_load(file)

if account_id.get("ACCOUNT"):
    account = account_id["ACCOUNT"]
else:
    if not os.environ.get("XTB_ACCOUNT"):
        print("ACCOUNT", end="", flush=True)
        while True:
            account = input("> ")
            if kit.represent_int(account):
                account = int(account)
                break
    else:
        if kit.represent_int(os.environ["XTB_ACCOUNT"]):
            account = int(os.environ["XTB_ACCOUNT"])
        else:
            sys.exit("Error: XTB_ACCOUNT variable is not an integer")
if account_id.get("PASSWORD"):
    password = account_id["PASSWORD"]
else:
    if not os.environ.get("XTB_PASSWORD"):
        password = stdiomask.getpass("PASSWORD> ")
    else:
        password = os.environ["XTB_PASSWORD"]

# Start session
QIAForexia.start(account, password)
