# ===========================================================================
#
# file     : repeater.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2024
# license  : MIT license, see license variable in the __init__.py
#
# ===========================================================================

class repeater:
    """
    iterate the indicated number of iterations, or forever when None

    :param iterations: int | None
        the number of iterations, or None for infinite iterationfs

    This iterator is usefull for iterative demos that by default
    must run forever, but might be used to run a fixed numer of times.

    The first iterator value is 0, the next is 1.
    When a number of iterations is specified, the value increments,
    otherwise it remains 1.

    examples::

        for _ in repeater( 10 ): ...  # ... is repeated 10 times
        for _ in repeater( None ): ...  # ... is repeated forever
    """

    # =======================================================================

    def __init__(
        self,
        iterations: int | None
    ) -> None:
        self.iterations = iterations
        self.n = None

    # =======================================================================

    def __iter__( self ):
        self.n = -1
        return self

    # =======================================================================

    def __next__( self ):
        if self.iterations is not None:
            self.n += 1
            if self.n >= self.iterations:
                raise StopIteration
        else:
            self.n = min( 1, self.n + 1 )
        return self.n

    # =======================================================================

# ===========================================================================
