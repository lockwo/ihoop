import unittest
from typing import ClassVar

from ihoop import AbstractAttribute, AbstractClassVar, Strict


class TestAbstractClassVar(unittest.TestCase):
    def test_abstract_class_with_classvar_cannot_instantiate(self):
        class AbstractBase(Strict):
            FACTOR: AbstractClassVar[int]

        with self.assertRaisesRegex(
            TypeError,
            r"Cannot instantiate abstract class AbstractBase.*classvars=\['FACTOR'\]",
        ):
            AbstractBase()

    def test_concrete_subclass_with_classvar_can_instantiate(self):
        class AbstractBase(Strict):
            FACTOR: AbstractClassVar[int]

        class Thing(AbstractBase):
            FACTOR = 2

            def __init__(self):
                pass

        t = Thing()
        self.assertEqual(Thing.FACTOR, 2)
        self.assertEqual(t.FACTOR, 2)

    def test_cannot_supply_value_on_abstract_declaration(self):
        with self.assertRaisesRegex(
            TypeError, r"Abstract class variable '.*\.X' cannot be defined with a value"
        ):

            class AbstractBad(Strict):
                X: AbstractClassVar[int] = 1

    def test_annotation_only_not_enough_in_subclass(self):
        class AbstractBase(Strict):
            FACTOR: AbstractClassVar[int]

        # Without a value, it remains abstract
        with self.assertRaisesRegex(
            TypeError,
            r"Abstract class '.*\.AlmostConcrete' must have a name "
            "starting with 'Abstract'",
        ):

            class AlmostConcrete(AbstractBase):
                FACTOR: ClassVar[int]  # No value provided

    def test_freeze_classvars_on_concrete_classes(self):
        class AbstractBase(Strict):
            FACTOR: AbstractClassVar[int]

        class Thing(AbstractBase):
            FACTOR = 2

        # Cannot modify frozen classvar
        with self.assertRaisesRegex(
            AttributeError,
            r"Cannot set frozen class variable 'FACTOR' on class 'Thing'",
        ):
            Thing.FACTOR = 3

        # Cannot delete frozen classvar
        with self.assertRaisesRegex(
            AttributeError,
            r"Cannot delete frozen class variable 'FACTOR' on class 'Thing'",
        ):
            del Thing.FACTOR

    def test_mix_instance_attribute_and_classvar(self):
        class AbstractConfig(Strict):
            value: AbstractAttribute[str]
            MAX_RETRIES: AbstractClassVar[int]

        # Cannot instantiate abstract class
        with self.assertRaisesRegex(
            TypeError,
            r"Cannot instantiate abstract class AbstractConfig.*attributes="
            r"\['value'\].*classvars=\['MAX_RETRIES'\]",
        ):
            AbstractConfig()

        # Partial resolution still abstract
        with self.assertRaisesRegex(
            TypeError,
            r"Abstract class '.*\.PartialConfig' must have a name starting with "
            "'Abstract'",
        ):

            class PartialConfig(AbstractConfig):
                MAX_RETRIES = 5
                # Missing value attribute

        # Full resolution allows instantiation
        class FullConfig(AbstractConfig):
            value: str
            MAX_RETRIES = 3

            def __init__(self):
                self.value = "test"

        config = FullConfig()
        self.assertEqual(config.value, "test")
        self.assertEqual(FullConfig.MAX_RETRIES, 3)

    def test_multiple_classvars(self):
        class AbstractMulti(Strict):
            NAME: AbstractClassVar[str]
            VERSION: AbstractClassVar[int]
            DEBUG: AbstractClassVar[bool]

        class Multi(AbstractMulti):
            NAME = "MyApp"
            VERSION = 1
            DEBUG = False

        self.assertEqual(Multi.NAME, "MyApp")
        self.assertEqual(Multi.VERSION, 1)
        self.assertEqual(Multi.DEBUG, False)

    def test_inherited_frozen_classvars(self):
        class AbstractBase(Strict):
            CONFIG: AbstractClassVar[str]

        class AbstractMiddle(AbstractBase):
            CONFIG = "base_config"
            EXTRA: AbstractClassVar[int]

        class Final(AbstractMiddle):
            EXTRA = 42

        # Cannot modify inherited frozen classvar
        with self.assertRaisesRegex(
            AttributeError,
            r"Cannot set frozen class variable 'CONFIG' on class 'Final'",
        ):
            Final.CONFIG = "new_config"

        # Cannot modify own frozen classvar
        with self.assertRaisesRegex(
            AttributeError, r"Cannot set frozen class variable 'EXTRA' on class 'Final'"
        ):
            Final.EXTRA = 100

    def test_abstract_naming_with_classvar(self):
        class _AbstractPrivate(Strict):
            VALUE: AbstractClassVar[int]

        class Public(_AbstractPrivate):
            VALUE = 10

        self.assertEqual(Public.VALUE, 10)

        with self.assertRaisesRegex(
            TypeError,
            r"Abstract class '.*\.BadName' must have a name starting with 'Abstract'",
        ):

            class BadName(Strict):
                SETTING: AbstractClassVar[str]

    def test_override_non_abstract_classvar(self):
        class AbstractBase(Strict):
            DEFAULT: ClassVar[int] = 10
            REQUIRED: AbstractClassVar[str]

        class AbstractDerived(AbstractBase):
            DEFAULT: ClassVar[int] = 20

        self.assertEqual(AbstractDerived.DEFAULT, 20)

        class Concrete(AbstractDerived):
            REQUIRED = "value"

        Concrete.DEFAULT = 30
        self.assertEqual(Concrete.DEFAULT, 30)

        with self.assertRaisesRegex(
            AttributeError,
            r"Cannot set frozen class variable 'REQUIRED' on class 'Concrete'",
        ):
            Concrete.REQUIRED = "new_value"


if __name__ == "__main__":
    unittest.main()
