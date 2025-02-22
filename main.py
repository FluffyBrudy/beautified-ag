import argparse
from arguments import *


def main():
    """
    Ag command but beutify search result by presenting data
    in 2d-table
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(**TERM)
    parser.add_argument(nargs="--dir", **DIR)
    args = parser.parse_args()
    print(args.dir)


if __name__ == "__main__":
    main()
