import pytest
from ase import Atoms
import numpy as np

@pytest.fixture(scope="session")
def atoms_records():
    def gen_atoms_list(frames_size):
        symbols = ['C', 'H', 'O']
        atoms_list = []
        for i in range(frames_size):
            pos = np.random.rand(len(symbols),3)
            atoms_list.append(Atoms(symbols=symbols, positions=pos, cell=[10,10,10], pbc=True))
        return atoms_list
    return gen_atoms_list