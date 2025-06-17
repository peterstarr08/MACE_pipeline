import pytest
from pathlib import Path
from mace_aze.cli.splitter import (
    validate_arguments,
    sample_config, calculate,
    save_config,
    AUTO_SPLIT,
    TRAIN_KEY,
    TEST_KEY,
    DEFAULT_VALUE_SPLIT,
    AUTO_SPLIT_RATIO,
    XTB_CALCULATOR_KEY
)

from mace_aze.config import us_0_selected, us_off_selected, dataset_path
from mace_aze.utils.generators import generate_space_offset
import numpy as np


default_key = {
        AUTO_SPLIT: True,
        TRAIN_KEY: DEFAULT_VALUE_SPLIT,
        TEST_KEY: DEFAULT_VALUE_SPLIT
}

us_key = {
        AUTO_SPLIT: False,
        TRAIN_KEY: us_0_selected,
        TEST_KEY: us_off_selected
}


@pytest.mark.parametrize(
    "label, atoms, us, offset, count",
    [
        ("benzene_cut_10", ["C", "H"], True, 1, 10),
        ("benzene_cut_10", ["C"], False, -24, 10),
        pytest.param("benzene_cut_10", ["C"], True, -24, 10 , marks=pytest.mark.xfail),
        pytest.param("benzene_cut_10", [], True, 4, 10 , marks=pytest.mark.xfail)
    ]
)
def test_validate(mocker, tmp_path_factory, label, atoms, us, offset, count):
    tempDir = tmp_path_factory.mktemp("temp",numbered=True)
    mock_raw = mocker.patch('mace_aze.cli.splitter.RawDataset')
    mock_raw.extract_path.return_value = tempDir
    validate_arguments(label=label, atoms=atoms, us=us, offset=offset, count=count)


@pytest.mark.parametrize(
        "count, us, offset, correct_key",
        [
            (10, True, 3, us_key),
            pytest.param(10, True, 3, default_key, marks=pytest.mark.xfail),
            (5, False, 5, default_key),
            pytest.param(10, False, 3, us_key, marks=pytest.mark.xfail),
        ]
)
def test_us_sample_config(atoms_records, count, us, offset, correct_key):
    db = atoms_records
    key = sample_config(db, count, us, offset)
    assert correct_key==key


@pytest.fixture(scope="function")
def fix_record_calculator(atoms_records):
    def _fix_record_calculator(count, offset, key):
        if not key[AUTO_SPLIT]:
            indx, offindx = generate_space_offset(count, len(atoms_records), offset)
            for i in indx:
                atoms_records[i].info[key[TRAIN_KEY]] = True
            for i in offindx:
                atoms_records[i].info[key[TEST_KEY]] = True
        return atoms_records
    return _fix_record_calculator


@pytest.mark.parametrize(
        "count, offset, key, calculator, atoms, expected_atoms",
        [
            (5, 1, us_key, XTB_CALCULATOR_KEY, [('C', 6), ('H', 1)], 12),
            (8, 2, default_key, None, [('C', 6)], 21)
        ]
)
def test_calculate(fix_record_calculator, mocker, count, offset, key, calculator, atoms, expected_atoms):
    mock_xtb = mocker.patch('mace_aze.cli.splitter.XTBCalculator')
    db = fix_record_calculator(count, offset, key)

    conf = calculate(db, key, calculator, [l[0] for l in atoms])
    assert len(conf) == expected_atoms

    for at, z in zip(conf, [sym[1] for sym in atoms]):
        assert z in at.get_atomic_numbers()
        assert at.info['config_type'] == 'IsolatedAtom'
        assert at.info[key[TRAIN_KEY]]

    for at in conf:
        if not key[AUTO_SPLIT]:
            assert (key[TRAIN_KEY] in at.info or key[TEST_KEY] in at.info)

    if calculate==XTB_CALCULATOR_KEY:
        mock_xtb.return_value.calculate.assert_called_once()


@pytest.fixture(scope="function")
def create_conf_save(atoms_records):
    def _create_conf_save(key):
        train_split = []
        test_split = []
        if key==us_key:
            for at in atoms_records[:int(len(atoms_records)/2)]:
                at.info[key[TRAIN_KEY]] = True
                train_split.append(at.copy())
            for at in atoms_records[int(len(atoms_records)/2):]:
                at.info[key[TEST_KEY]] = True
                test_split.append(at.copy())
        elif key==default_key:
            for at in atoms_records[:int(len(atoms_records)*AUTO_SPLIT_RATIO)]:
                # at.info[key[TRAIN_KEY]] = True
                train_split.append(at.copy())
            for at in atoms_records[int(len(atoms_records)*AUTO_SPLIT_RATIO):]:
                # at.info[key[TEST_KEY]] = True
                test_split.append(at.copy())
        return (atoms_records, train_split, test_split)
    return _create_conf_save



@pytest.mark.parametrize(
        "label, calc, key, storage_path_train, storage_path_test",
        [
            (   "benzene_10", XTB_CALCULATOR_KEY, us_key,
                dataset_path/Path('benzene/10/train/benzene_10_train__dataset__xtb.xyz'),
                dataset_path/Path('benzene/10/test/benzene_10_test__dataset__xtb.xyz')
            )
        ]
)
def test_save_config(mocker, create_conf_save, label, calc, key, storage_path_train, storage_path_test):
    mock_write_config = mocker.patch("mace_aze.cli.splitter.write_configs")
    db, trs, tes = create_conf_save(key)
    save_config(label, db, calc, key)
    argVal = (
        (storage_path_train, trs),
        (storage_path_test, tes)
    )

    mock_write_config.assert_called_once()
    actual_call_args = mock_write_config.call_args[0]  # unpacked *args

    assert actual_call_args == argVal