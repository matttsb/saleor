from decimal import Decimal

from prices.discount import (
    fixed_discount, percentage_discount as prices_percentage_discount)


class FixedDiscount:
    """Reduces price by a fixed amount."""

    def __init__(self, amount, name=None):
        self.amount = amount
        self.name = name

    def __repr__(self):
        return 'FixedDiscount(%r, name=%r)' % (self.amount, self.name)

    def apply(self, base):
        return fixed_discount(base, self.amount)


def percentage_discount(base, percentage, name=None):
    discounted_base = prices_percentage_discount(base, percentage)
    fixed_discount_amount = base - discounted_base
    return FixedDiscount(fixed_discount_amount, name)
