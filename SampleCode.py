import time

sensor.update(20)
while True:
    time.sleep(0.05)
    speed = int(sensor.leftAngle/40)
    channel.send(speed)



import time

motor.update(20)  # 20 msec between updates
while True:
    time.sleep(0.05)
    s=motor.run(channel.msg)