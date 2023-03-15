import os
import pathlib


def assemble_file_structure():

    mode = 0o666
    global_path = pathlib.Path(__file__).parent.resolve()
    project_path = None

    for composition in range(0, 9999):

        directory = f'Composition{composition}'
        directory_path = os.path.join(global_path, directory)

        if not os.path.exists(directory_path):
            project_path = directory_path
            os.mkdir(project_path, mode)
            break

    return global_path, project_path
