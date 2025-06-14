import pytest
from pathlib import Path
from utils.records import Dataset
from config import dataset_path


'''Testing each indivudual function of Raw dataset class'''

@pytest.mark.parametrize("file_type, label, operation", 
                            [   
                                ("xyz", "benzene_10", "xtb"),
                                ("sdf", "benzene_cut_10", "mace"),
                                pytest.param("xyz", "benzene__10", None, marks=pytest.mark.xfail)
                            ]
                        )
def test_validity(file_type, label, operation):
    Dataset(file_type=file_type, label=label, operation=operation)


@pytest.mark.parametrize("file_type, label, operation, file_path", 
                            [   
                                ("xyz", "benzene_10", "xtb", "benzene/10"),
                                ("sdf", "benzene_cut_10", "mace","benzene/cut/10"),
                                pytest.param("sdf", "benzene_cut_10", "cp2k", "benzene/cut", marks=pytest.mark.xfail)

                            ]
                        )
def test_file_path(file_type, label, operation, file_path):
    rd = Dataset(file_type=file_type, label=label, operation=operation)
    assert file_path == rd.file_path()


# #Db fomart yet to do

@pytest.mark.parametrize("file_type, label, operation, file_name", 
                            [   
                                ("xyz", "benzene_10", "xtb","benzene_10__dataset__xtb.xyz"),
                                ("sdf", "benzene_cut_10", "mace", "benzene_cut_10__dataset__mace.sdf"),
                                pytest.param("xyz", "benzene_cut_10", "cp2k","benzene_cut_10__raw_dataset__cp2k.xyz", marks=pytest.mark.xfail),
                                pytest.param("xyz", "benzene_cut_10", "duck","benzene_cut_10__dataset_duck.sdf", marks=pytest.mark.xfail)

                            ]
                        )
def test_file_name(file_type, label, operation, file_name):
    rd = Dataset(file_type=file_type, label=label, operation=operation)
    assert file_name == rd.file_name()



@pytest.mark.parametrize("file_type, label, operation, full_path", 
                            [   
                                ("xyz", "benzene_10", "xtb",  dataset_path/Path('benzene/10/benzene_10__dataset__xtb.xyz')),
                                ("sdf", "benzene_cut_10", "mace", dataset_path/Path('benzene/cut/10/benzene_cut_10__dataset__mace.sdf'))

                            ]
                        )
def test_file_full_path(file_type, label, operation,full_path):
    rd = Dataset(file_type=file_type, label=label, operation=operation)
    assert isinstance(rd.full_path(), Path)
    assert full_path == rd.full_path()

