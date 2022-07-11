import argparse
import json
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser("Renames files")
    parser.add_argument("--file", "-f", type=str,
                        help="input file, --format to see required format")
    parser.add_argument("--base-dir", "-b", dest="base_dir", default=".",
                        type=str, help="base directory to chdir into before renaming files")
    parser.add_argument("--dry-run", "-d", action="store_true", dest="dry_run",
                        help="check input files exist and print files to be renamed")
    parser.add_argument("--format", action="store_true",
                        help="print input file format")

    return parser.parse_args()


def print_format():
    print(
        """
input.json:
[
  {
    "old": "/path/to/current/file",
    "new": "/new/path/to/file"
  },
  ...
]
"""
    )


if __name__ == "__main__":
    args = parse_args()

    if args.format:
        print_format()
        sys.exit(0)

    with open(args.file) as f:
        files = json.load(f)

    os.chdir(args.base_dir)

    if args.dry_run:
        do_not_exist = list(
            filter(lambda e: not os.path.exists(e["old"]), files))
        if len(do_not_exist) > 0:
            print("The following files were not found:")
            print("\n".join(map(lambda f: f["old"], files)))
            sys.exit(1)

        print("All files exist. The following will be renamed:")
        print("\n".join(map(lambda f: f"{f['old']} -> {f['new']}", files)))
        sys.exit(0)

    for f in files:
        os.rename(f['old'], f['new'])

    print("Done")
