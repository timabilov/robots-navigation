import pytest

from core.geo import Direction


class TestDirection:

    @pytest.mark.parametrize("direction, to_the_right", (
        (Direction.NORTH, Direction.EAST),
        (Direction.EAST, Direction.SOUTH),
        (Direction.SOUTH, Direction.WEST),
        (Direction.WEST, Direction.NORTH)
    ))
    def test_right(self, direction, to_the_right):

        assert direction.right() == to_the_right, f'right of the {direction} should be {to_the_right}'

    @pytest.mark.parametrize("direction, to_the_left", (
            (Direction.NORTH, Direction.WEST),
            (Direction.WEST, Direction.SOUTH),
            (Direction.SOUTH, Direction.EAST),
            (Direction.EAST, Direction.NORTH)
    ))
    def test_left(self, direction, to_the_left):

        assert direction.left() == to_the_left, f'left of the {direction} should be {to_the_left}'
