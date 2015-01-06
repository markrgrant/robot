from ..robot import Robot
from ..position import Position
from ..vial import Vial
from collections import OrderedDict


config = {
    'racks': OrderedDict([
        ('sample', {'x': 10, 'y': 3}),
        ('intermediate', {'x': 20, 'y': 5}),
        ('final', {'x': 20, 'y': 5}),
        ('tetradecane', {'x': 1, 'y': 1}),
        ('hexane', {'x': 1, 'y': 1})
    ]),
    'vortexer': {'container_types': ['sample', 'intermediate', 'final']},
    'capper': {'container_types': ['sample', 'intermediate', 'final']},
    'arm': {
        'gripper':{},
        'syringe': {'max_volume_in_ml': 2}
    }
}


def test_init():
    Robot(config)

def test_wash():
    bot = Robot(config)
    assert bot._arm._syringe.is_washed is False
    bot.wash_tip()
    assert bot._arm._syringe.is_washed is True
def test_prime():
    bot = Robot(config)
    assert bot._arm.is_primed is False
    bot.prime()
    assert bot._arm.is_primed is True

def test_aspirate_dispense():
    bot = Robot(config)
    bot.prime()
    source_vial = Vial('sample')
    source_vial.add_contents(water=1.0)
    bot.aspirate(source_vial, 0.5)
    assert source_vial._contents['water'] == 0.5
    assert bot._arm._syringe._contents['water'] == 0.5
    dest_vial = Vial('sample')
    bot.dispense(dest_vial, 0.25)
    assert dest_vial._contents['water'] == .25
    assert bot._arm._syringe._contents['water'] == 0.25

def test_transfer():
    bot = Robot(config)
    bot.prime()
    source_vial = Vial('sample')
    source_vial.add_contents(water=1.0)
    dest_vial = Vial('sample')
    bot.transfer(source_vial, dest_vial, 0.5)
    assert source_vial._contents['water'] == 0.5
    assert dest_vial._contents['water'] == 0.5

def test_cap_uncap():
    vial = Vial('sample')
    vial.position = Position(0,0)
    bot = Robot(config)
    bot.add_container(vial)
    bot.uncap(vial)
    assert vial.is_capped is False
    bot.cap(vial)
    assert vial.is_capped is True

def test_vortex():
    bot = Robot(config)
    container = Vial('sample')
    container.position = Position(0,0)
    bot.add_container(container)
    bot.vortex(container)
    assert container.is_mixed is True

def test_to_str():
    bot = Robot(config)
    bot.to_str()

def test_blow_off():
    bot = Robot(config)
    assert bot._arm._syringe._blown_off is False
    bot.blow_off()
    assert bot._arm._syringe._blown_off is True
