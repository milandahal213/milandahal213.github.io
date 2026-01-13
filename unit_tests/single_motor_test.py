import time

print(motor.hubType)
print(motor.position)
print(motor.angle)
print(motor.speed)

motor.run(speed = 100, port = 1, direction = 2)
time.sleep(1)

motor.set_speed(speed = 50)
time.sleep(1)

motor.stop(port = 1) 
time.sleep(1)
    
motor.run_angle(angle = 90, port = 1, direction = 2)
time.sleep(1)
motor.run_angle(angle = 90, port = 1, direction = 2)
time.sleep(1)
    
motor.run_to(pos = 10, port = 1, direction = 2)
time.sleep(1)
motor.run_to(pos = 10, port = 1, direction = 2)
time.sleep(1)