from pathlib import Path

from cli.batch_yeet import validate_arguments, collect_frames, export_config



def test_validate_args(frames_save_setup_path):
    validate_arguments(str(frames_save_setup_path), "_")

def test_collect_frames(frames_save_setup_path, atoms_records):
    print(f"Reading from: {frames_save_setup_path}")
    db = collect_frames(frames_save_setup_path)
    assert len(db) == len(atoms_records)

def test_export_frames(mocker, atoms_records, read_io_save_path):
    svpath =  read_io_save_path / Path("benzene/10/benzene_10__raw_dataset.xyz")
    mock_full_path = mocker.patch("cli.batch_yeet.RawDataset.full_path")
    mock_full_path.return_value = svpath
    assert not svpath.exists()
    export_config(db=atoms_records, label="benzene_10",ext="xyz") 
    assert svpath.exists()
