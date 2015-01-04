from ..container import (
    Container,
    ContainerEmpty,
    ContainerNotEmpty
)
from nose.tools import raises


def test_init():
    c = Container('gc_vial')
    assert c.is_empty

def test_add_contents():
    c = Container('test')
    assert c.is_empty
    test = dict()
    c.add_contents(test)
    assert c.contents == test

@raises(ContainerNotEmpty)
def test_add_contents_not_empty():
    c = Container('test')
    test = dict()
    c.add_contents(test)
    c.add_contents(test)

def test_remove_contents():
    c = Container('test')
    test = dict()
    c.add_contents(test)
    contents = c.remove_contents()
    assert contents == test

@raises(ContainerEmpty)
def test_remove_contents_empty():
    c = Container('test')
    c.remove_contents()

def test_transfer():
    c_from = Container('test')
    c_to = Container('test')
    test = dict()
    c_from.add_contents(test)
    c_to.transfer(c_from)
    contents = c_to.remove_contents()
    assert contents == test

def test_container_type():
    container_type = 'gc_vial'
    c = Container(container_type)
    assert c.container_type == 'gc_vial'

def test_is_empty():
    c = Container('gc_vial')
    assert c.is_empty is True
    c.add_contents(dict(water=1.0))
    assert c.is_empty is False
