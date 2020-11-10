import pathlib
import os

THIS_DIR = pathlib.Path(__file__).parent
MESH_DIR = pathlib.Path(os.environ.get("MESH_DIR", THIS_DIR / "meshes"))


class PathManager:
    def __init__(self):
        self._mesh_directory = self._pathify(MESH_DIR, path_type="dir")

    @property
    def mesh_directory(self):
        return self._mesh_directory

    @staticmethod
    def _pathify(path, path_type="file", required=False):
        if path_type not in ("file", "dir"):
            raise ValueError(f"{path_type} is not a valid path_type value")

        path = pathlib.Path(path)
        if path_type == "file" and required and not path.is_file():
            raise FileNotFoundError(f"{path} cannot be found and is required")
        elif path_type == "dir" and not path.is_dir():
            path.mkdir(parents=True)
        return path
