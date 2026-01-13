import time

print(motor.hubType)
print(motor.position)
print(motor.angle)
print(motor.speed)
print(motor.position2)
print(motor.angle2)
print(motor.speed2)

motor.run(speed = 100, port = 1, direction = 2)
time.sleep(1)
motor.run_left(speed = 100, direction = 2)
time.sleep(1)
motor.run_right(speed = 100, direction = 2)
time.sleep(1)
motor.run_both(speed = 100, direction = 2)
time.sleep(1)
 
motor.set_speed(speed = 100, port = 1)
time.sleep(1)
motor.set_speedL(speed = 100)
time.sleep(1)
motor.set_speedR(speed = 100)
time.sleep(1)

motor.stop(port = 3)
time.sleep(1)

motor.run_angle(angle = 90, port = 1, direction = 2)
time.sleep(1)
motor.run_angleL(angle = 90, direction = 2)
time.sleep(1)
motor.run_angleR(angle = 90, direction = 2)
time.sleep(1)

motor.run_to(pos = 10, port = 1, direction = 2)
time.sleep(1)
motor.run_toL(pos = 10, direction = 2)
time.sleep(1)
motor.run_toR(pos = 10, direction = 2)
time.sleep(1)

motor.update(rate = 20)
time.sleep(1)

