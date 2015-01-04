from ..arm import (
    Arm,
    SyringeNotPrimed,
)
from ..material_container import MaterialContainer
from nose.tools import raises


arm_config = dict(
    gripper=dict(),
    syringe=dict(max_volume_in_ml=2.0))


def test_init():
    arm = Arm(arm_config)
    assert arm._gripper is not None
    assert arm._syringe is not None

def test_wash_tip():
    arm = Arm(arm_config)
    arm.wash_tip()
    assert arm._syringe.is_washed is True

def test_prime():
    arm = Arm(arm_config)
    arm.prime()
    assert arm._syringe.is_primed is True

def test_aspirate():
    arm = Arm(arm_config)
    arm.prime()
    container = MaterialContainer(container_type='test', max_volume_in_ml=1.5)
    container.add_contents(water=1.0)
    volume = 0.5
    arm.aspirate(container, volume)
    assert arm._syringe._contents['water'] == 0.5

@raises(SyringeNotPrimed)
def test_aspirate_no_prime():
    arm = Arm(arm_config)
    container = MaterialContainer(container_type='test', max_volume_in_ml=1.5)
    volume = 1.0
    arm.aspirate(container, volume)

def test_dispense():
    arm = Arm(arm_config)
    arm.prime()
    water_container = MaterialContainer(
        container_type='water_container', max_volume_in_ml=20.0)
    water_container.add_contents(water=1.0)
    arm.aspirate(water_container, 1.0)
    container = MaterialContainer(container_type='test', max_volume_in_ml=1.5)
    volume_in_ul = 0.5
    arm.dispense(container, volume_in_ul)
    assert container._contents['water'] == 0.5
    assert arm._syringe._contents['water'] == 0.5

def test_to_str():
    arm = Arm(arm_config)
    arm.to_str()
