from abc import abstractmethod
from typing import ClassVar
from unittest import TestCase

import equinox as eqx

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


class TestEqxAbstractVarStrictness(TestCase):

    def test_abstractvar_only_module_is_abstract(self):
        class AbstractHolder(AbstractStrictModule):
            x: eqx.AbstractVar[int]

            def doubled(self) -> int:
                return self.x * 2

        with self.assertRaises(TypeError):
            AbstractHolder()

    def test_field_resolves_abstractvar(self):
        class AbstractHolder(AbstractStrictModule):
            x: eqx.AbstractVar[int]

            def doubled(self) -> int:
                return self.x * 2

        class Holder(AbstractHolder):
            x: int

        self.assertEqual(Holder(3).doubled(), 6)

    def test_property_resolves_abstractvar(self):
        class AbstractHolder(AbstractStrictModule):
            x: eqx.AbstractVar[int]

        class Holder(AbstractHolder):
            @property
            def x(self) -> int:
                return 7

        self.assertEqual(Holder().x, 7)

    def test_method_complete_intermediate_stays_abstract(self):
        class AbstractBase(AbstractStrictModule):
            x: eqx.AbstractVar[int]

            @abstractmethod
            def f(self) -> int:
                raise NotImplementedError

        class AbstractMid(AbstractBase):
            def f(self) -> int:
                return self.x

        with self.assertRaises(TypeError):
            AbstractMid()

        class Final(AbstractMid):
            x: int

        self.assertEqual(Final(5).f(), 5)

    def test_unresolved_abstractvar_on_concrete_name_is_rejected(self):
        with self.assertRaises(TypeError):

            class Holder(AbstractStrictModule):  # noqa: F841
                x: eqx.AbstractVar[int]

    def test_abstractclassvar_counts_and_resolves(self):
        class AbstractHolder(AbstractStrictModule):
            y: eqx.AbstractClassVar[int]

        class Holder(AbstractHolder):
            y: ClassVar[int] = 3

        self.assertEqual(Holder.y, 3)
