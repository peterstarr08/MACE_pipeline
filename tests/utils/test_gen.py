import pytest
import numpy as np
from utils.generators import generate_space_offset  # Replace with your actual module

@pytest.mark.parametrize(
    "count, end, offset, overlap, should_raise, expected_len_base",
    [
        (3, 10, 2, False, False, 3),       # Normal case
        (3, 10, 2, True,  False, 3),       # Allow overlap
        (3, 5, 3, False, False, 3),        # Offset exceeds end, gets truncated
        (5, 5, 1, False, False, 5),        # Max fill
        (6, 5, 1, False, True,  None),     # Error: count > end
    ]
)
def test_generate_space_offset(count, end, offset, overlap, should_raise, expected_len_base):
    if should_raise:
        with pytest.raises(ValueError):
            generate_space_offset(count, end, offset, overlap)
    else:
        base, off = generate_space_offset(count, end, offset, overlap)

        assert len(base) == expected_len_base
        assert np.all(base < end)
        assert np.all(off < end)

        if not overlap:
            assert np.intersect1d(base, off).size == 0

        # Optional: Check offset difference for valid pairs
        common_len = min(len(base), len(off))
        diffs = off[:common_len] - base[:common_len]
        assert np.all(diffs >= offset)
