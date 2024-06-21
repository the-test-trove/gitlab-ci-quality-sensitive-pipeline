#!/usr/bin/python3
import argparse

from lib.api import get_user
from lib.io import output_stdout, validate


def main(user_id):
    """Main application logic."""
    validate(user_id)
    user = get_user(user_id)
    output_stdout(user)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", type=int, help="user_id int")
    args = parser.parse_args()
    main(args.user_id)
