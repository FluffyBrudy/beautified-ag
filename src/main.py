#!/usr/bin/env python3

import argparse
from argparse import ArgumentError
from arguments import *
from initializer import init
import subprocess


def run_beautified_ag():
    """
    Ag command but beutify search result by presenting data
    in 2d-table
    """

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(**TERM)
        parser.add_argument("--dir", **DIR)
        args = parser.parse_args()
        
        if not args.dir or not args.term:
            parser.print_help()
            return
    except ArgumentError as e:
        print('error')
    try:
        result = subprocess.run(
            ["ag", "--nobreak", "--noheading", args.term, args.dir],
            capture_output=True,
            text=True,
            check=True,
        )
        rows = result.stdout.splitlines()

        filenames = []
        lines = []
        matches = []
        max_filenames_col_len = 0
        max_lines_col_len = 0
        max_matches_col_len = 0
        max_dash_lines = 0
        for row in rows:
            file, line, _match = row.split(":", 2)
            max_filenames_col_len = max(max_filenames_col_len, len(file))
            max_lines_col_len = max(max_lines_col_len, len(line))
            max_matches_col_len = max(max_matches_col_len, len(_match))
            filenames.append(file)
            lines.append(line)
            matches.append(
                _match.strip().replace(args.term, f"\033[42m{args.term}\033[0m")
            )
        max_dash_lines = (
            max_filenames_col_len + max_lines_col_len + max_matches_col_len + 2
        )
        print(
            "-" * (max_filenames_col_len + max_lines_col_len + max_matches_col_len + 6)
        )
        print(
            f"{'Filename'.ljust(max_filenames_col_len)} | "
            f"{'Lines'.ljust(max_lines_col_len)} | "
            f"{'Matches'.ljust(max_matches_col_len)}"
        )
        print(
            "-" * (max_filenames_col_len + max_lines_col_len + max_matches_col_len + 6)
        )

        for file, line, _match in zip(filenames, lines, matches):
            print(
                f"{file.ljust(max_filenames_col_len)} | "
                f"{line.ljust(max_lines_col_len + 5 - max_lines_col_len)} | "
                f"{_match.ljust(max_matches_col_len)}"
            )

        print(
            "-" * (max_filenames_col_len + max_lines_col_len + max_matches_col_len + 6)
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            print(f"No match found, (STATUS_CODE: {e.returncode})")
        else:
            print(f"{e.stderr}, (STATUS_CODE: {e.returncode})")
    except Exception as e:
         print(f"{e.stderr}, (STATUS_CODE: ${e.returncode})")
    


def main():
    init()
    run_beautified_ag()


if __name__ == "__main__":
    main()
