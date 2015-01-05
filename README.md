## summary

A simulation of a robot that performs liquid transfers

## usage

### create a robot instance

robot = Robot(config)

### transfer and weigh reagents

robot.transfer(source, dest, vol_in_ml)
robot.transfer_and_weigh(source, dest, vol_in_ml)




## methods
- transfer(source, dest, vol_in_ml)
- weigh(container)
- prime()
- wash()
- blow_off()
- mix(vial)

