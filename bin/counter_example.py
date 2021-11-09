from collections import Counter

from frozendict import frozendict

# initializing two dictionaries
dict1 = {'a': 12, 'for': 25, 'c': 9}
dict2 = {'Geeks': 100, 'geek': 200, 'for': 300}


# adding the values with common key

fdict = Counter(dict1) + Counter(dict2)
print(frozendict(fdict))
