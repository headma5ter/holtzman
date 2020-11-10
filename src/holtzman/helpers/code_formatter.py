import pathlib
import black
import os


def find_top_dir() -> pathlib.Path:
    top_dir = None
    for dir_path in pathlib.Path(__file__).resolve().parents:
        if dir_path.stem == "src":
            top_dir = dir_path

    if top_dir is None:
        raise FileNotFoundError(
            "Cannot find top directory (looking for 'holtzman/src')"
        )

    return top_dir


if __name__ == "__main__":
    top_dir = find_top_dir()
    for file_dir, _, files in os.walk(top_dir):
        for file in files:
            file = pathlib.Path(file_dir) / file
            if file.suffix != ".py":
                continue
            if black.format_file_in_place(
                file, fast=True, mode=black.FileMode(), write_back=black.WriteBack.YES
            ):
                print(f"Reformatted {file}")
