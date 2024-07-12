import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence, Union


def main(argv: Union[Sequence[str], None] = None) -> int:

    args = argv or sys.argv[1:]
    delete = True

    try:
        args.remove("--delete-bak")
    except ValueError:
        delete = False

    try:
        subprocess.run(
            ["indent"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        sys.stderr.write(
            "indent not found on system path. Please install `indent` package"
        )
        if os.name == "nt":
            sys.stderr.write("On Windows install `GnuWin32 Indent`")

        return 1
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr)
        return 1

    if delete:
        for file in map(lambda x: Path(x + "~"), args):
            if file.is_file():
                try:
                    file.unlink()
                except Exception as e:
                    return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
