import meshio
import pygmsh

from holtzman import path_handler


class MeshMetadata:
    def __init__(self):
        self._mesh_dir = path_handler.mesh_directory
        self._mesh_file_name = "test_cylinder.msh"
        self._mesh_path = self._mesh_dir / self._mesh_file_name
        self._lcar = 30 * 0.025

    @property
    def mesh_dir(self):
        return self._mesh_dir

    @property
    def mesh_file_name(self):
        return self._mesh_file_name

    @property
    def mesh_path(self):
        return self._mesh_path

    @property
    def lcar(self):
        return self._lcar


def create_geometry(lcar):
    geom = pygmsh.built_in.Geometry()
    geom.add_pipe(21, 22, 100, lcar=lcar)
    return geom


def create_mesh(geo_obj, file_name, write_to_file=False):
    mesh = pygmsh.generate_mesh(geo_obj)
    if write_to_file:
        meshio.write(file_name, mesh)
        print(f"Written to {file_name}")


if __name__ == "__main__":
    metadata = MeshMetadata()

    geometry = create_geometry(metadata.lcar)
    mesh = create_mesh(geometry, metadata.mesh_path, write_to_file=True)
