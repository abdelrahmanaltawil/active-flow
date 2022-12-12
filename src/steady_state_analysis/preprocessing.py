# env imports
import pathlib
import zipfile
import numpy as np
import pandas as pd

# local imports
import helpers.register as re


def parse_parameters() -> None:
    '''
    Placeholder
    '''

    ## snapshot locations
    # check validity of snapshot locations
    # make sure they are 6, raise warning if they are not


# def fetch(experiment_file: object, temp_download_path: pathlib.Path) -> np.ndarray or pd.DataFrame:
#     '''
#     Placeholder
#     '''

#     experiment_file.download(destination= temp_download_path)

#     if temp_download_path.suffix == ".zip":
#         unzip_delete_file(temp_download_path)

#     elif temp_download_path.suffix == ".csv":

    
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


def load_arrays(read_path: pathlib.Path, snapshots_locations: list[str]) -> tuple[np.ndarray]:
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
        snapshots_paths.extend(read_path.joinpath("snapshots/w_k").glob(pattern)) 

    for path in snapshots_paths:
        snapshots[path.stem] = np.load(path)

    # register
    re.register["operators"] = operators
    re.register["snapshots"] = snapshots

    return operators, snapshots


def load_table(read_path: pathlib.Path) -> pd.DataFrame:
    '''
    Placeholder
    '''

    monitor_table = pd.read_csv(read_path)

    return monitor_table
    

