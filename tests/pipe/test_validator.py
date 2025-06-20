import pytest
from mace_aze.pipe.validator import validate_yml, validate_backward_dependencies
from mace_aze.pipe.conf import pipeline, generation, models_path, md_path, new_ds, meta, calc, sampler


@pytest.fixture
def valid_cfg():
    return {
        pipeline: [
            {f"{generation}0": {models_path: [], md_path: [], new_ds: []}}
        ],
        meta: {
            calc: {},
            sampler: {}
        }
    }

@pytest.fixture
def invalid_dependencies():
    return {
        pipeline: [
            {f"{generation}0": {new_ds: [],  models_path: []}}
        ],
        meta: {
            calc: {},
            sampler: {}
        }
    }

@pytest.fixture
def missing_meta_cfg():
    return {
        pipeline: [
            {f"{generation}0": {models_path: [], md_path: [], new_ds: []}}
        ]
        # meta key missing
    }

@pytest.fixture
def partial_meta_cfg():
    return {
        pipeline: [
            {f"{generation}0": {models_path: [], md_path: [], new_ds: []}}
        ],
        meta: {
            calc: {}  # sampler missing
        }
    }

# ---------- Tests ---------- #

def test_valid_cfg(valid_cfg):
    validate_yml(valid_cfg)  # Should pass without exception

def test_invalid_dependencies(invalid_dependencies):
    with pytest.raises(SyntaxError):
        validate_yml(invalid_dependencies)

def test_missing_meta(missing_meta_cfg):
    with pytest.raises(SyntaxError):
        validate_yml(missing_meta_cfg)

def test_partial_meta(partial_meta_cfg):
    with pytest.raises(SyntaxError):
        validate_yml(partial_meta_cfg)

@pytest.mark.parametrize("order, dependencies, should_raise", [
    (["a", "b", "c"], {"c": ["b"], "b": ["a"], "a": []}, False),
    ([ "c", "b"], {"c": ["b"], "b": ["a"], "a": []}, True),
])
def test_validate_backward_dependencies(order, dependencies, should_raise):
    if should_raise:
        with pytest.raises(SyntaxError):
            validate_backward_dependencies(order, dependencies)
    else:
        validate_backward_dependencies(order, dependencies)
