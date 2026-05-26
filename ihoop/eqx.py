import equinox as eqx

from .strict import _StrictMeta, Strict


class _StrictEqxMeta(_StrictMeta, eqx._module._module._ModuleMeta):
    pass


class AbstractStrictModule(eqx.Module, Strict, metaclass=_StrictEqxMeta):
    pass
