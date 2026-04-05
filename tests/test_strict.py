import unittest

from ihoop import AbstractAttribute, Strict


class TestStrict(unittest.TestCase):
    def test_abstract_instantiation(self):
        class AbstractThing(Strict):
            value: AbstractAttribute[int]

        with self.assertRaises(TypeError):
            AbstractThing()

    def test_concrete_instantiation_and_immutability(self):
        class AbstractThing(Strict):
            value: AbstractAttribute[int]

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

            class Bad(Strict):
                value: AbstractAttribute[int]

    def test_concrete_class_name_prefix_forbidden(self):
        class _AbstractBase(Strict):
            value: AbstractAttribute[int]

        with self.assertRaises(TypeError):

            class AbstractThing(_AbstractBase):
                value: int

                def __init__(self, v: int):
                    self.value = v

    def test_concrete_subclassing_forbidden(self):
        class AbstractBase(Strict):
            value: AbstractAttribute[int]

        class Final(AbstractBase):
            value: int

            def __init__(self, v: int):
                self.value = v

        with self.assertRaises(TypeError):

            class SubFinal(Final):
                pass

    def test_cannot_override_concrete_method(self):
        class AbstractBase(Strict):
            value: AbstractAttribute[int]

            def concrete(self):
                return 1

        class Final(AbstractBase):
            value: int

            def __init__(self, v: int):
                self.value = v

        with self.assertRaises(TypeError):

            class BadOverride(Final):
                def concrete(self):  # type: ignore
                    return 2

    def test_abstract_attribute_value_assignment_forbidden(self):
        with self.assertRaises(TypeError):

            class AbstractBad(Strict):
                attr: AbstractAttribute[int] = 1


    def test_metaclass_methods_not_treated_as_class_methods(self):
        """Methods on the metaclass (e.g. __call__) should not block
        subclasses from defining the same dunder as an abstract method."""
        from abc import ABCMeta, abstractmethod

        class _MetaWithCall(ABCMeta):
            def __call__(cls, *args, **kwargs):
                return super().__call__(*args, **kwargs)

        class _CombinedMeta(_MetaWithCall, Strict.__class__):
            pass

        class AbstractBase(Strict, metaclass=_CombinedMeta):
            @abstractmethod
            def __call__(self, x):
                raise NotImplementedError

        class Concrete(AbstractBase):
            def __init__(self):
                pass

            def __call__(self, x):
                return x

        c = Concrete()
        self.assertEqual(c(42), 42)


if __name__ == "__main__":
    unittest.main()
