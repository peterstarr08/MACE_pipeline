import numpy as np
import pytest
from config import us_0_selected, us_off_selected
from sampler.uniform_selector import UniformSelector

frames_count = 20



def test_clear_initial_selection(atoms_records):
    atoms = atoms_records(frames_count)
    rnd = np.random.randint(0, frames_count, 5)

    for i in rnd:
        if i%2==0:
            atoms[i].info[us_0_selected] = True
        else:
            atoms[i].info[us_off_selected] = True
    
    UniformSelector.clear_initial_selection(atoms)

    for at in atoms:
        assert not (us_0_selected in at.info or us_off_selected in at.info)


@pytest.mark.parametrize(
        "select_count, offset",
        [
            (15, 5),
            (12, 0),
            pytest.param(frames_count+1, 2,marks=pytest.mark.xfail)
        ]
)
def test_select(atoms_records, select_count, offset):
    atoms = atoms_records(frames_count)

    us = UniformSelector(offset=offset)
    indx = np.linspace(0, len(atoms), select_count, endpoint=False, dtype=int)
    offset_indx = np.linspace(offset, len(atoms), select_count, endpoint=False, dtype=int)

    us.select(atoms, select_count)

    for i in range(len(atoms)):
        if i in indx:
            assert atoms[i].info[us_0_selected] == True
        if i in offset_indx:
            assert atoms[i].info[us_off_selected] == True


