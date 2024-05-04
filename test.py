a = {'s': 123}
b = {'c': 49}
a.update(b)
print(a)
b['c'] = 50
a.update(b)
print(a)