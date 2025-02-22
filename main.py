import argparse

## ARGUMENTS
DIR = {"dest": "dir", "metavar": "", "help": "directory to look for search term"}
TERM = {"dest": "term", "metavar": "SEARCH_TERM", "help": "term to search for"}


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
