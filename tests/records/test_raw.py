import pytest
from pathlib import Path
from mace_aze.utils.records import RawDataset
from mace_aze.config import raw_dataset_path


'''Testing each indivudual function of Raw dataset class'''

@pytest.mark.parametrize("file_type, label", 
                            [   
                                ("xyz", "benzene_10"),
                                ("sdf", "benzene_cut_10"),
                                pytest.param("xyz", "benzene__10", marks=pytest.mark.xfail)
                            ]
                        )
def test_validity(file_type, label):
    RawDataset(file_type=file_type, label=label)


@pytest.mark.parametrize("file_type, label, file_path", 
                            [   
                                ("xyz", "benzene_10", "benzene/10"),
                                ("sdf", "benzene_cut_10", "benzene/cut/10"),
                                pytest.param("sdf", "benzene_cut_10", "benzene/cut", marks=pytest.mark.xfail)

                            ]
                        )
def test_file_path(file_type, label, file_path):
    rd = RawDataset(file_type=file_type, label=label)
    assert file_path == rd.file_path()


#Db fomart yet to do

@pytest.mark.parametrize("file_type, label, file_name", 
                            [   
                                ("xyz", "benzene_10", "benzene_10__raw_dataset.xyz"),
                                ("sdf", "benzene_cut_10", "benzene_cut_10__raw_dataset.sdf"),
                                pytest.param("xyz", "benzene_cut_10", "benzene_cut_10__raw_dataset", marks=pytest.mark.xfail),
                                pytest.param("xyz", "benzene_cut_10", "benzene_cut_10.sdf", marks=pytest.mark.xfail)

                            ]
                        )
def test_file_name(file_type, label, file_name):
    rd = RawDataset(file_type=file_type, label=label)
    assert file_name == rd.file_name()



@pytest.mark.parametrize("file_type, label, full_path", 
                            [   
                                ("xyz", "benzene_10", raw_dataset_path/Path('benzene/10/benzene_10__raw_dataset.xyz')),
                                # ("sdf", "benzene_cut_10", "benzene_cut_10__raw_dataset.sdf"),
                                pytest.param("xyz", "benzene_cut_10", "benzene_cut_10__raw_dataset", marks=pytest.mark.xfail),
                                pytest.param("xyz", "benzene_cut_10", "benzene_cut_10.sdf", marks=pytest.mark.xfail)

                            ]
                        )
def test_file_full_path(file_type, label, full_path):
    rd = RawDataset(file_type=file_type, label=label)
    assert isinstance(rd.full_path(), Path)
    assert full_path == rd.full_path()


@pytest.mark.parametrize("file_type, label, full_path", 
                            [   
                                ("xyz", "benzene_10", raw_dataset_path/Path('benzene/10/benzene_10__raw_dataset.xyz')),
                                # ("sdf", "benzene_cut_10", "benzene_cut_10__raw_dataset.sdf"),
                                pytest.param("xyz", "benzene_cut_10", "benzene_cut_10__raw_dataset", marks=pytest.mark.xfail),
                                pytest.param("xyz", "benzene_cut_10", "benzene_cut_10.sdf", marks=pytest.mark.xfail)

                            ]
                        )
def test_path_parser(file_type, label, full_path):
    rd = RawDataset.extract_path(label=label)
    assert isinstance(rd, Path)
    assert full_path == rd


