import unittest
from dataclasses import dataclass

from ihoop import AbstractAttribute, Strict


class TestStrict(unittest.TestCase):
    def test_abstract_instantiation(self):
        @dataclass
        class AbstractThing(Strict):
            value: AbstractAttribute[int]

        with self.assertRaises(TypeError):
            AbstractThing()

    def test_concrete_instantiation_and_immutability(self):
        @dataclass
        class AbstractThing(Strict):
            value: AbstractAttribute[int]

        @dataclass
        class Thing(AbstractThing):
            value: int

            def __init__(self, v: int):
                self.value = v

        t = Thing(1)
        self.assertEqual(t.value, 1)
        with self.assertRaises(AttributeError):
            t.value = 2
        with self.assertRaises(AttributeError):
            del t.value

    def test_abstract_class_name_prefix_required(self):
        with self.assertRaises(TypeError):

            @dataclass
            class Bad(Strict):
                value: AbstractAttribute[int]

    def test_concrete_class_name_prefix_forbidden(self):
        @dataclass
        class _AbstractBase(Strict):
            value: AbstractAttribute[int]

        with self.assertRaises(TypeError):

            @dataclass
            class AbstractThing(_AbstractBase):
                value: int

                def __init__(self, v: int):
                    self.value = v

    def test_concrete_subclassing_forbidden(self):
        @dataclass
        class AbstractBase(Strict):
            value: AbstractAttribute[int]

        @dataclass
        class Final(AbstractBase):
            value: int

            def __init__(self, v: int):
                self.value = v

        with self.assertRaises(TypeError):

            @dataclass
            class SubFinal(Final):
                pass

    def test_cannot_override_concrete_method(self):
        @dataclass
        class AbstractBase(Strict):
            value: AbstractAttribute[int]

            def concrete(self):
                return 1

        @dataclass
        class Final(AbstractBase):
            value: int

            def __init__(self, v: int):
                self.value = v

        with self.assertRaises(TypeError):

            @dataclass
            class BadOverride(Final):
                def concrete(self):  # type: ignore
                    return 2

    def test_abstract_attribute_value_assignment_forbidden(self):
        with self.assertRaises(TypeError):

            @dataclass
            class AbstractBad(Strict):
                attr: AbstractAttribute[int] = 1


if __name__ == "__main__":
    unittest.main()
