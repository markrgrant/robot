from ..reader import (
    Reader,
    ReaderEmpty,
    ReaderOccupied
)
from ..vial import Vial
from nose.tools import raises


def test_init():
    reader = Reader()
    assert reader._contents is None

def test_add_container():
    reader = Reader()
    container = Vial('gc_vial')
    reader.add_container(container)
    assert reader._contents == container

def test_remove_container():
    reader = Reader()
    container = Vial('gc_vial')
    reader.add_container(container)
    assert reader._contents == container
    removed_container = reader.remove_container()
    assert container == removed_container
    assert reader._contents is None
    assert reader.is_empty

def test_read_barcode():
    reader = Reader()
    container = Vial('gc_vial')
    reader.add_container(container)
    reader.read_barcode()

@raises(ReaderOccupied)
def test_read_occupied():
    reader = Reader()
    container = Vial('gc_vial')
    reader.add_container(container)
    reader.add_container(container)

@raises(ReaderEmpty)
def test_read_empty():
    reader = Reader()
    reader.read_barcode()

@raises(ReaderEmpty)
def test_remove_empty():
    reader = Reader()
    reader.remove_container()

def test_shared_barcode_iterator():
    reader_a = Reader()
    reader_b = Reader()
    container_a = Vial('gc_vial')
    container_b = Vial('gc_vial')
    reader_a.add_container(container_a)
    reader_b.add_container(container_b)
    reader_a.read_barcode()
    reader_b.read_barcode()
    assert container_a.barcode + 1 == container_b.barcode

def test_to_str():
    reader = Reader()
    reader.to_str()




