import argparse
import os
import shutil
from pathlib import Path
from os import access, R_OK
from shutil import SameFileError


def copy_files(path: Path, dest: Path) -> None:
    if path.is_dir():
        for child in path.iterdir():
            copy_files(child, dest)

        return

    if not os.access(path, R_OK):
        return

    ext = path.suffix
    if ext == "":
        ext = "none"

    target_dir = os.path.join(dest, ext)
    target_path = Path(target_dir)

    try:
        if not target_path.is_dir():
            target_path.mkdir(parents=True)

        shutil.copy(path, target_path)
    except SameFileError:
        pass
    except PermissionError as e:
        print(e)
    except Exception as e:
        print(f"failed to copy file {path} to {target_path}, error: {e}")


def main():
    parser = argparse.ArgumentParser(
        prog='fgroup',
        description='Recursively copies files from target to dist based on a file extension')

    parser.add_argument('source')
    parser.add_argument('-d', '--destination', default='dist', required=False, help='Destination directory')

    args = parser.parse_args()

    src = Path(os.path.abspath(args.source))
    dist = Path(os.path.abspath(args.destination))

    copy_files(src, dist)

if __name__ == '__main__':
    main()