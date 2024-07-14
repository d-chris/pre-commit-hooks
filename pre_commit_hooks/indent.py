import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence, Union


def indent_version() -> str:
    """Return the version of indent."""

    try:
        subprocess.run(
            ["indent", "--version"],
            check=True,
            encoding="Windows-1252",
            capture_output=True,
        )
    except FileNotFoundError as e:
        raise SystemExit(1) from e
    except subprocess.CalledProcessError as e:
        return e.output

    raise SystemExit(1)


def main(argv: Union[Sequence[str], None] = None) -> int:

    parser = argparse.ArgumentParser(
        description="changes the appearance of a C program by inserting or deleting whitespace.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Files to indent.",
        default=[],
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity level",
    )
    parser.add_argument(
        "--simple-backup-suffix",
        default=os.getenv("SIMPLE_BACKUP_SUFFIX", "~"),
        help="Set the simple backup suffix",
    )
    parser.add_argument(
        "--version-control",
        choices=["simple", "numbered", "numbered-existing", "none"],
        default=os.getenv("VERSION_CONTROL", "simple"),
        help="Backup files",
        type=str.lower,
    ),
    parser.add_argument(
        "--no-version-control",
        action="store_const",
        const="none",
        dest="version_control",
        help="Delete backup files. This is equivalent to --version-control=none.",
    ),
    parser.add_argument(
        "--version-width",
        type=int,
        help="digits of backup versions",
        metavar="N",
        default=os.getenv("VERSION_WIDTH", None),
    )
    parser.add_argument("--version", action="version", version=indent_version())

    args, uargs = parser.parse_known_args(argv)

    env = os.environ.copy()

    if args.simple_backup_suffix:
        env["SIMPLE_BACKUP_SUFFIX"] = args.simple_backup_suffix

    if args.version_control == "none":
        env["VERSION_CONTROL"] = "simple"
    else:
        env["VERSION_CONTROL"] = args.version_control

    if args.version_width:
        env["VERSION_WIDTH"] = str(args.version_width)

    if args.verbose > 0:
        print(f"indent: ", argv + sys.argv[1:])

    try:
        subprocess.run(
            ["indent"] + uargs + args.filenames,
            check=True,
            env=env,
            encoding="Windows-1252",
            capture_output=False if args.verbose > 0 else True,
        )
    except FileNotFoundError:
        return 1
    except subprocess.CalledProcessError as e:
        return e.returncode

    if args.version_control == "none":
        for name in args.filenames:
            file = Path(name + args.simple_backup_suffix)

            if file.is_file():
                try:
                    file.unlink()
                except Exception as e:
                    continue

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
