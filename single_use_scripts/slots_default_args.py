class A:
	__slots__ = ['x']

class B:
	def __init__(self, foo=A()):
		self.a = foo

b1 = B()
b1.a.x = 14

b2 = B()
print(b2.a.x)


'''
>>> class A:
...     __slots__ = ('x')
... 
>>> a1 = A()
>>> a1.x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: x
>>> a1.x = 15
>>> a1.x
15
>>> 
>>> a2 = A()
>>> a2.x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: x

>>> class A:
...     __slots__ = ['x']
... 
>>> class B:
...     def __init__(self, a=A()):
...             self.a = a
... 
>>> b1 = B()
>>> b1.a.x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: x
>>> b1.a.x = 123
>>> b1.a.x
123
>>> b2 = B()
>>> b2.a.x
123
>>> b1.a
<__main__.A object at 0x10640c558>
>>> b2.a
<__main__.A object at 0x10640c558>


It turns out that default arguments work the same way in __init__() as they would in regular functions. 
That is, in the declaration "def __init__(self, a=A()):", the "a" argument is only ever ONCE default 
initialized to a new instance of A. Subsequent invocations of the constructor will result in the self.a 
referencing the exact same instance. This is an issue in nltk's PunktSentenceTokenizer.

def __init__(self, train_text=None, verbose=False, lang_vars=PunktLanguageVars(), token_cls=PunktToken):
	...

The problem is lang_vars=PunktLanguageVars(). Python default arguments should NEVER be assigned to mutable 
objects.
http://docs.python-guide.org/en/latest/writing/gotchas/
'''

