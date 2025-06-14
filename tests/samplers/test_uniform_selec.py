import numpy as np
from sampler.uniform_selector import UniformSelector

frames_count = 20
select_frame = 10

def test_select(atoms_records):
    us = UniformSelector()
    atoms = atoms_records(frames_count)
    indx = np.linspace(0, len(atoms), select_frame, endpoint=False, dtype=int)
    db = us.select(atoms, select_frame)
    for refAt, selAt in zip([atoms[i].copy() for i in indx], db):
        assert refAt==selAt
