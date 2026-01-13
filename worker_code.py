import code
code.interact()

from pyscript import document, window, when, sync
await window.init.promise

from worker_channel import Channel
channel = Channel()

from worker_motors import Motor
motor = Motor()

from worker_sensors import Sensor
sensor = Sensor()

_e1 = document.getElementById('var_1')

@when('change','#var_1')
def rename():
    _e1.value = _e1.value.replace(' ','_')
    exec(f"{_e1.value} = motor ")