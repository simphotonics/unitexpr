from numbers import Number

from .qarray import qarray


def quantity(value: Number, unit=1.0, info=""):
    """
    Constructs a quantity described by
    a numerical value or a numerical array,
    a unit and an optional string
    containing additional information.
    The instance attribute `info` can be used to store
    object documentation.

    ---
    Example:
    ```
    from numpy import identity
    from unitexpr import quantity
    from unitexpr.sc_units import nm, ps

    # Quantity defined by a numerical value.
    electron_diffusion_constant = quantity(
        3.0e3,
        unit=nm ** 2 / ps,
        info="Electron diffusion rate.",
    )

    # Quantity defined by an array.
    eta = quantity(identity(4, dtype=int), info='Minkovsky space metric')
    eta[0, 0] = -1
    ```
    """
    return qarray.from_input(value, unit=unit, info=info)
