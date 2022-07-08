import argparse
import json
import os
import sys

from fuzzywuzzy import fuzz
from pick import pick


def load_json(filepath: str) -> object:
    with open(filepath) as f:
        data = json.load(f)
    return data


def parse_args():
    parser = argparse.ArgumentParser(
        description="Correct the season/episode numbers of existing files")
    parser.add_argument("--current", "-c", type=str,
                        help="list of current files, --formats to see required format")
    parser.add_argument("--targets", "-t", type=str,
                        help="list of target titles, --formats to see required format")
    parser.add_argument("--fuzzy-count", "-n", type=int, default=3,
                        dest="n", help="number of fuzzy matches to choose from")
    parser.add_argument("--output", "-o", type=str,
                        default="out", help="output directory")
    parser.add_argument("--formats", action="store_true",
                        help="display input file formats and quit")

    return parser.parse_args()


def find_closest(title, targets, n):
    augmented = list(
        map(
            lambda target:
            {
                **target,
                "ratio": fuzz.partial_ratio(title.lower(), target["title"].lower())
            },
            targets
        )
    )
    return sorted(
        augmented,
        key=lambda aug: -aug["ratio"]
    )[0:3]


def get_choice(raw, targets):
    title = f"{raw}:"
    options = [
        *targets,
        "NONE",
        "QUIT"
    ]
    return pick(options, title)


if __name__ == "__main__":
    args = parse_args()

    if args.formats:
        print(
            """
current.json:
[
  {
    "raw": "/path/to/episode.mkv",
    "number": "S01E03",
    "title": "Title Without Extension"
  },
  ...
]

targets.json:
[
  {
    "number": "S01E03",
    "title": "Title Still No Extension"
  },
  ...
]
"""
        )
        sys.exit(0)

    if not args.current or not args.targets:
        print("Must pass both --current and --targets")
        sys.exit(1)

    if os.path.exists(args.output) and not os.path.isdir(args.output):
        print(f"--output passed is not a directory")
        sys.exit(1)

    current_names = load_json(args.current)
    target_names = load_json(args.targets)

    not_found = []

    for c in current_names:
        closest = find_closest(c["title"], target_names, args.n)
        choice, idx = get_choice(c["raw"], closest)
        if choice == "QUIT":
            # Save results thus far
            break
        elif choice == "NONE":
            # Save file to dead queue
            not_found.append(c["raw"])
        else:
            # Add episode number to current
            c["new_number"] = choice["number"]

    found = list(
        filter(lambda episode: "new_number" in episode.keys(), current_names))
    remaining = list(filter(lambda episode: "new_number" not in episode.keys(
    ) and episode["raw"] not in not_found, current_names))
    finalized = list(map(lambda current: {"old": current["raw"], "new": current["raw"].replace(
        current["number"], current["new_number"])}, found))

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    os.chdir(args.output)

    with open("finalized.json", "w") as f:
        json.dump(finalized, f, indent=2)

    with open("not_found.json", "w") as f:
        json.dump(not_found, f, indent=2)

    with open("remaining.json", "w") as f:
        json.dump(remaining, f, indent=2)
