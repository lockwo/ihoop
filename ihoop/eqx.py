from typing import FrozenSet

import equinox as eqx

from .strict import _StrictMeta, Strict


class _StrictEqxMeta(_StrictMeta, eqx._module._module._ModuleMeta):
    @staticmethod
    def _strict_extra_abstracts(cls: type) -> tuple[FrozenSet, FrozenSet]:
        """Report equinox abstract vars/classvars left unresolved on ``cls``."""
        return (
            frozenset(getattr(cls, "__abstractvars__", ())),
            frozenset(getattr(cls, "__abstractclassvars__", ())),
        )


class AbstractStrictModule(eqx.Module, Strict, metaclass=_StrictEqxMeta):
    pass
