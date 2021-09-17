from functools import partial

def radix_sort(values, key, step=0):
    if len(values) < 2:
        for value in values:
            yield value
        return

    bins = {}
    for value in values:
        bins.setdefault(key(value, step), []).append(value)

    for k in sorted(bins.keys()):
        for r in radix_sort(bins[k], key, step + 1):
            yield r

def bw_key(text, value, step):
    print("Value is: ", value)
    print("Step is: ", step)
    return text[(value + step) % len(text)]

def burroughs_wheeler_custom(text):
    return ''.join(text[i - 1] for i in radix_sort(range(len(text)), partial(bw_key, text)))