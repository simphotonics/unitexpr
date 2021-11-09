from unitexpr.errors import *

e = UnitError('hello')

n = NotSupportedError(message=89)

print(n)

o = OperationNotSupported('a', 'b', '*', '')
print(o)
print(o.invert())
