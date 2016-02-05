"""Pearson correlation."""

from math import sqrt


def pearson(pairs):
    """Return Pearson correlation for pairs.
    Using a set of pairwise ratings, produces a Pearson similarity rating.
    """

    series_1 = [float(pair[0]) for pair in pairs]
    series_2 = [float(pair[1]) for pair in pairs]

    sum_1 = sum(series_1)
    sum_2 = sum(series_2)

    squares_1 = sum([n * n for n in series_1])
    squares_2 = sum([n * n for n in series_2])
    print squares_1, "sq 1"
    print squares_2, "sq 2"

    product_sum = sum([n * m for n, m in pairs])
    print product_sum, "I AM SUM-PRODUCT"
    print sum_1, "SUM 1"
    print sum_2, "SUM 2"

    size = len(pairs)

    print size, "SIZE"

    numerator = product_sum - ((sum_1 * sum_2) / size)

    denominator = sqrt(
        (squares_1 - (sum_1 * sum_1) / size) *
        (squares_2 - (sum_2 * sum_2) / size)
    )

    print denominator, "denominator"
    print numerator, "numerator"

    if denominator == 0:
        return 0

    return numerator / denominator
