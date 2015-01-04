from ..balance import (
    Balance,
    BalanceEmpty,
    BalanceOccupied
)
from ..vial import Vial
from nose.tools import raises


def test_balance_init():
    balance = Balance()
    assert balance._contents is None

def test_balance_add_remove_container():
    balance = Balance()
    container = Vial(container_type='gc_vial')
    balance.add_container(container)
    assert balance.is_empty() is False
    weight = balance.weigh_container()
    container = balance.remove_container()
    assert balance.is_empty() is True
    assert weight == Balance._default_weight


@raises(BalanceOccupied)
def test_balance_occupied():
    balance = Balance()
    container = Vial(container_type='gc_vial')
    balance.add_container(container)
    container = Vial(container_type='gc_vial')
    balance.add_container(container)

@raises(BalanceEmpty)
def test_balance_weigh_empty():
    balance = Balance()
    balance.weigh_container()

@raises(BalanceEmpty)
def test_balance_remove_empty():
    balance = Balance()
    balance.remove_container()

def test_balance_to_str():
    balance = Balance()
    balance.to_str()
