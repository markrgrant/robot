## summary
This project provides a simulation of a robot that performs liquid transfers
along with an API for controlling this simulation and a simple web application
through which the state of the simulation can be viewed and interacted with.

#!/usr/bin/env bash

# transfer(source, dest, vol_in_ml)
# weigh(container)
# prime()
# wash()
# blow_off()
# mix(vial)


curl -H "Content-Type: application/json" -d '{"name":"wash_tip", "inputs":null, "outputs":null}' http://localhost:5000/task

curl -H "Content-Type: application/json" -d '{"name":"prime", "inputs":null, "outputs":null}' http://localhost:5000/task

curl -H "Content-Type: application/json" -d '{"name":"blow_off", "inputs":null, "outputs":null}' http://localhost:5000/task

curl -H "Content-Type: application/json" -d '{"name":"get_samples", "inputs": {"num_samples": 8}, "outputs":null}' http://localhost:5000/task

