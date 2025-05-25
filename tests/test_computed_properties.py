from computed_properties import ComputedPropertyCache

# Global instance of the caching system
w = ComputedPropertyCache()


class Example(metaclass=w):
    """Example class using computed properties with dependency tracking."""

    def __init__(self):
        super().__init__()
        self.x = 1
        self.y = 2
        self.z = 3

    @w.computed_property
    def a(self):
        """Depends on x."""
        return self.x + 1

    @w.computed_property
    def b(self):
        """Depends on a and y."""
        return self.a + self.y

    @w.computed_property
    def c(self):
        """Depends on b and z."""
        return self.b + self.z


# Pytest-based test cases


def test_initial_computation():
    """Check initial values of computed properties."""
    e = Example()
    assert e.a == 2
    assert e.b == 4
    assert e.c == 7


def test_change_x_affects_all():
    """Changing x should affect a, b, and c."""
    e = Example()
    _ = e.a, e.b, e.c  # warm up cache
    e.x = 10
    assert e.a == 11
    assert e.b == 13
    assert e.c == 16


def test_change_y_affects_b_and_c():
    """Changing y should affect b and c but not a."""
    e = Example()
    _ = e.a, e.b, e.c
    e.y = 5
    assert e.a == 2  # unchanged
    assert e.b == 7
    assert e.c == 10


def test_change_z_affects_only_c():
    """Changing z should only affect c."""
    e = Example()
    _ = e.a, e.b, e.c
    e.z = 8
    assert e.a == 2  # unchanged
    assert e.b == 4  # unchanged
    assert e.c == 12
