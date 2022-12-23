# env imports
import zipfile
import pathlib 
import numpy as np
from re import search

# local imports
import active_flow.hyperuniformity_analysis.helpers.register as re


def unzip_delete_file(file_path: pathlib.Path) -> None:
    '''
    Placeholder
    '''

    # unzip
    with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(".")
        zip_file.close()

    # delete
    file_path.unlink()


def load_arrays(read_path: pathlib.Path, snapshots_locations: list[str]) -> tuple[dict]:
    '''
    Placeholder
    '''

    operators={}
    for path in read_path.glob("*.npy"):
        operators[path.stem] = np.load(path)
    
    snapshots={}
    snapshots_paths =[]

    snapshots_file_pattern = ["*"+str(location).zfill(8)+"*" for location in snapshots_locations]
    for pattern in snapshots_file_pattern:
        snapshots_paths.append(read_path.joinpath("snapshots/extrema").glob(pattern)) 

    
    keys = ["Iteration = " + str(location) for location in snapshots_locations]
    for iteration, iteration_extrema_paths in zip(keys, snapshots_paths):
        extrema={}
        for path in iteration_extrema_paths:
            key = path.stem[:search(r"\d", path.stem).start()-1]
            extrema[key] = np.load(path)
        
        snapshots[iteration] = extrema

    # register
    re.register["operators"] = operators
    re.register["snapshots"] = snapshots

    return operators, snapshots