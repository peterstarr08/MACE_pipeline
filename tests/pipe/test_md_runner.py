import pytest

from mace_aze.pipe.md_runner import get_args

@pytest.mark.parametrize(
    "conf_dic, openmm_args",
    [
        (
            {
                "key0": 123,
                "key1": "Hello",
                "key2": 32
            },
            ["--key0","123","--key1","Hello","--key2","32"]
        ),
        pytest.param(
            {
                "key0": 123,
                "key1": "Hello",
                "key2": 32
            },
            ["--key0","123","--key1","Hello","--key3","32"],
            marks=pytest.mark.xfail
        )
    ]
)
def test_get_args(conf_dic, openmm_args):
    assert openmm_args==get_args(conf_dic)