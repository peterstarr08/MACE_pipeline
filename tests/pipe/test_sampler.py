import pytest
from ase import Atoms
from mace_aze.pipe.samplers import thershold_sample, top_disagreement_sample  # adjust import as needed

# Helper to create mock Atoms with a given value in .info
def make_atoms(val, key="error"):
    at = Atoms("H")
    at.info[key] = val
    return at

@pytest.fixture
def mock_configs():
    return [
        make_atoms(0.1),
        make_atoms(0.5),
        make_atoms(0.9),
        make_atoms(0.2),
        make_atoms(0.8)
    ]

def test_threshold_sample(mock_configs):
    selected = thershold_sample(mock_configs, threshold=0.4, key="error")
    values = [at.info["error"] for at in selected]
    assert all(v > 0.4 for v in values)
    assert len(selected) == 3

def test_top_disagreement_sample(mock_configs):
    top_k = 2
    selected = top_disagreement_sample(mock_configs, count=top_k, key="error")
    values = [at.info["error"] for at in selected]
    assert len(selected) == top_k
    assert values == sorted(values, reverse=True)

def test_top_disagreement_fallback(mock_configs):
    selected = top_disagreement_sample(mock_configs[:1], count=5, key="error")
    assert selected == mock_configs[:1]
