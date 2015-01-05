from ..robot import Robot
from ..position import Position
from ..vial import Vial


def test_init():
    Robot()

def test_wash():
    bot = Robot()
    assert bot._arm._syringe.is_washed is False
    bot.wash_tip()
    assert bot._arm._syringe.is_washed is True
def test_prime():
    bot = Robot()
    assert bot._arm.is_primed is False
    bot.prime()
    assert bot._arm.is_primed is True

def test_aspirate_dispense():
    bot = Robot()
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
    bot = Robot()
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
    bot = Robot()
    bot.add_container(vial)
    bot.uncap(vial)
    assert vial.is_capped is False
    bot.cap(vial)
    assert vial.is_capped is True

def test_vortex():
    bot = Robot()
    container = Vial('sample')
    container.position = Position(0,0)
    bot.add_container(container)
    bot.vortex(container)
    assert container.is_mixed is True

def test_to_str():
    bot = Robot()
    bot.to_str()

def test_blow_off():
    bot = Robot()
    assert bot._arm._syringe._blown_off is False
    bot.blow_off()
    assert bot._arm._syringe._blown_off is True
