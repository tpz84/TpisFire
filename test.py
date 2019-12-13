import string

for items in string.printable:
    print([items, ord(items)*11039])