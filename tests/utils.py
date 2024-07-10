from itertools import chain, combinations


def powerset_dict(d: dict):
    items = list(d.items())
    subsets = list(chain.from_iterable(combinations(items, r) for r in range(len(items) + 1)))

    powerset = [dict(subset) for subset in subsets]

    return powerset
