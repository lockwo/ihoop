from abc import abstractmethod
from unittest import TestCase

from ihoop.eqx import AbstractStrictModule


class TestEqxIntegration(TestCase):
    def test_marker_base_is_not_instantiable(self):
        with self.assertRaises(TypeError):
            AbstractStrictModule()

    def test_subclassing_marker_base_works(self):
        class AbstractFoo(AbstractStrictModule):
            @abstractmethod
            def bar(self):
                raise NotImplementedError

        class Foo(AbstractFoo):
            x: float

            def __init__(self, x: float):
                self.x = x

            def bar(self):
                return self.x + 1

        f = Foo(2.0)
        self.assertEqual(f.bar(), 3.0)

    def test_concrete_is_final(self):
        class AbstractFoo(AbstractStrictModule):
            @abstractmethod
            def bar(self):
                raise NotImplementedError

        class Foo(AbstractFoo):
            def bar(self):
                return 42

        with self.assertRaises(TypeError):

            class SubFoo(Foo):  # noqa: F841
                pass

    def test_no_synthetic_strict_base_method(self):
        class AbstractFoo(AbstractStrictModule):
            @abstractmethod
            def bar(self):
                raise NotImplementedError

        class Foo(AbstractFoo):
            def bar(self):
                return 1

        self.assertFalse(hasattr(Foo, "_strict_base_"))
