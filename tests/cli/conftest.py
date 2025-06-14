import pytest

from ase import Atoms
from ase.io import write
import numpy as np
from pathlib import Path


read_dir = "out"
save_dir = "dumped_files"

frames_size = 20

@pytest.fixture(scope="session")
def read_io_save_path(tmp_path_factory):
    dump_path = tmp_path_factory.mktemp(read_dir, numbered=False)
    return dump_path

@pytest.fixture(scope="session")
def frames_save_setup_path(tmp_path_factory):
    frames_save_setup_path = tmp_path_factory.mktemp(save_dir, numbered=False)
    return frames_save_setup_path

@pytest.fixture(scope="session")
def atoms_records():
    symbols = ['C', 'H', 'O']
    atoms_list = []
    for i in range(frames_size):
        pos = np.random.rand(len(symbols),3)
        atoms_list.append(Atoms(symbols=symbols, positions=pos, cell=[10,10,10], pbc=True))
    return atoms_list

@pytest.fixture(autouse=True)
def save_frames(atoms_records, frames_save_setup_path):
    for i, at in enumerate(atoms_records):
        write(str(frames_save_setup_path/Path(f'config{i}.xyz')), at)
    print(f"All files written in {str(frames_save_setup_path)}")
