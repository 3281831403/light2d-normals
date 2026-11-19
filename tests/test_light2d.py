import pytest

from render import light2d as mod

CASES = [
    ('decode_normal', [0.5, 0.5], [0.0, 0.0, 1.0], True),
    ('decode_normal', [0.0, 0.0], [-1.0, -1.0, 0.0], True),
    ('falloff', [5, 10, 2], 0.25, True),
    ('cone_mask', [0, 10, 20], 1.0, True),
    ('cone_mask', [30, 10, 20], 0.0, True),
    ('blend_light', [0.2, 0.5, 0.5], 0.45, True),
    ('ray_segment_intersect', [[0, 0], [1, 0], [5, -1], [5, 1]], 5.0, True),
    ('ray_segment_intersect', [[0, 0], [1, 0], [-5, -1], [-5, 1]], -1.0, True),
    ('cull_lights', [[0, 0], 5, [[1, 0], [10, 0]]], [0], False),
    ('batch_count', [1000, 64], 16, False),
    ('normal_strength', [[0.5, 0.5, 0.5], 2], [1.0, 1.0, 0.5], True),
    ('attenuate_color', [[1, 1, 1], 5, 10], [0.5, 0.5, 0.5], True),
    ('commit_lights', [[True, True]], True, False),
    ('falloff', [0, 10, 3], 1.0, True),
    ('ray_segment_intersect', [[0, 0], [0, 1], [0, 1], [1, 1]], 1.0, True),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_light2d_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected
