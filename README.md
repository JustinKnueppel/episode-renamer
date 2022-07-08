# Episode Renamer

This collection of scripts assists in finding the correct season and episode number for a given list of episode files. For example, let's say we have the following file:

```
./The Office (2005)/Season 1/The Office(2005) S02E03 - Diversity Day.mkv
```

The season and episode designation in the file name does not match what is found on [IMDb](https://www.imdb.com/title/tt0664514/) which lists "Diversity Day" to be season 1 episode 2 of The Office. Given a correctly formatted input list of such files and a correctly formatted list of the true titles from a source such as [IMDb](https://www.imdb.com/), these scripts would help convert the former to:

```
./The Office (2005)/Season 1/The Office(2005) S01E02 - Diversity Day.mkv
```

## Scripts

### `fuzzy.py`

This script uses fuzzy pattern matching to determine which episodes most closely match the title of the current file. For each file to be renamed, a [curses](https://docs.python.org/3/library/curses.html) interface will show allowing the user to choose between the `n` files, 3 by default, that most closely match the current file's title. If none of the options match, there is a `NONE` option, and if there are too many to do in one sitting there is a `QUIT` option.

Upon either finishing all episodes or quitting, three files will be written. `finalized.json` will output a list of files to be renamed in a format that `rename.py` accepts. `not_found.json` will output a list of files that were marked `NONE` in the same format as `finalized.json`, but without a change in file name so that these episodes can be manually addressed before renaming. Finally `remaining.json` will have be a file that is ready to be processed again by `fuzzy.py` containing all remaining files if the `QUIT` option was used.

#### Arguments

| Option                | Default | Description                            |
| --------------------- | ------- | -------------------------------------- |
| `--current`, `-c`     | N/A     | List of current files                  |
| `--targets`, `-t`     | N/A     | List of real episodes                  |
| `--output`, `-o`      | `out`   | Output directory                       |
| `--fuzzy-count`, `-n` | `3`     | Number of fuzzy matches to choose from |
| `--formats`           | N/A     | Print help text for input file formats |

### `rename.py`

This script takes a list files to be renamed and renames them accordingly

#### Arguments

| Option             | Default | Description                                            |
| ------------------ | ------- | ------------------------------------------------------ |
| `--file`, `-f`     | N/A     | List of files to be renamed                            |
| `--base-dir`, `-b` | `.`     | Directory to `chdir` into before reading/writing files |
| `--format`         | N/A     | Print help text for input file format                  |

## File Formats

### `fuzzy.py`

There are two json files expected as input. The first, specified with `--current <FILE>`, holds the current file list formatted as such:

```json
[
  {
    "raw": "./The Office (2005)/Season 1/The Office(2005) S01E02 - Diversity Day.mkv",
    "number": "S02E03",
    "title": "Diversity Day"
  },
  ...
]
```

The second, specified with `--targets <FILE>`, holds the list of current titles and season/episode numbers formatted as such:

```json
[
  {
    "number": "S01E02",
    "title": "Diversity Day"
  },
  ...
]
```

There will also be 3 files outputted with the following formats:

`remaining.json` will have the same format as the file passed with `--current <FILE>`

`finalized.json` will be prepared to rename the files with the following format

```json
[
  {
    "old": "./The Office (2005)/Season 1/The Office(2005) S02E03 - Diversity Day.mkv",
    "new": "./The Office (2005)/Season 1/The Office(2005) S01E02 - Diversity Day.mkv"
  },
  ...
]
```

`not_found.json` will have the same format as `finalized.json`, but with the `old` and `new` keys being identical to prepare for manual replacement.

### `rename.py`

There is one json file expected as input using the `--file <FILE>` flag that must be in the following format:

```json
[
  {
    "old": "./The Office (2005)/Season 1/The Office(2005) S02E03 - Diversity Day.mkv",
    "new": "./The Office (2005)/Season 1/The Office(2005) S01E02 - Diversity Day.mkv"
  },
  ...
]
```
