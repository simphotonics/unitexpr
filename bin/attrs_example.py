from attr import *

@attr.s
class Coordinates(object):
    x = attr.ib()
    y = attr.ib()
