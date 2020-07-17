#!/usr/bin/env python3

import argparse
import pandas as pd
import pathlib
import pydriller


def get_commits_from_path(path: pathlib.Path) -> pd.DataFrame:
    commit_data = {"repo": [], "sha": [], "username": [], "email": [], "time": []}
    repo_name = path.absolute().name

    for commit in pydriller.RepositoryMining(str(path.absolute())).traverse_commits():
        author = commit.author

        commit_data["repo"].append(repo_name)
        commit_data["sha"].append(commit.hash)
        commit_data["username"].append(author.name)
        commit_data["email"].append(author.email)
        commit_data["time"].append(commit.committer_date)

    return pd.DataFrame(commit_data)


def main():
    parser = argparse.ArgumentParser(
        description="Extract commit history data from local repositories."
    )
    parser.add_argument(
        "-r",
        "--repo",
        required=True,
        nargs="*",
        type=pathlib.Path,
        help="Path to repository.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        type=pathlib.Path,
        default=pathlib.Path("./commits.csv"),
        help="CSV file to save commit data to.",
    )

    args = parser.parse_args()

    # Append commit data to dataframe.
    df = pd.DataFrame()
    for path in args.repo:
        if path.exists():
            df = pd.concat([df, get_commits_from_path(path)])

    if not args.output.exists():
        args.output.touch()

    df.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
