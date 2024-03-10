# ===========================================================================
#
# file     : make_pin_out.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

import godafoss as gf

def make_pin_out(
    pin
) -> gf.pin_out:
    """
    make a pin_out

    This function returns a pin_out if one can be made from its
    parameter, which can be a pin number, a pin_out, a pin_in_out,
    or a pin_oc.

    When the parameter is a pin_oc, the returned pin_out won't
    drive its physical pin high: a suitable pull-up must be provided
    to do that.

    $macro_start make_pin_out_types
    int,
    :class:`~godafoss.pin_out`,
    :class:`~godafoss.pin_in_out`,
    :class:`~godafoss.pin_oc`
    $macro_end
    """

    if pin is None:
        p = gf.pin_dummy()

    elif isinstance( pin, int ):
        if pin < 0:
            p = gf.pin_dummy()
        else:
            p = gf.gpio_out( pin )

    else:
        p = pin

    return p.as_pin_out()

