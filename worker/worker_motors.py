from pyscript import document, window, when, sync

CtrlC = document.getElementById('myButton')

def check_CtrlC():
    if CtrlC.classList.contains("pressed"):
        CtrlC.classList.toggle("pressed")
        CtrlC.innerText = "Abort?"
        raise KeyboardInterrupt("Manual interruption triggered.")

class Motor:
    def __init__(self):
        pass
    @property
    def hubType(self):
        check_CtrlC()
        return sync.hub_bridge('hubType')

    def _read(self, parameter):
        try:
            myType = self.hubType
            if not myType: 
                return None
            check_CtrlC()
            self.reply = sync.hub_bridge('reply')
            #if parameter == 'battery': 
            #    return self.reply['hub info']['Battery']
            motor_info = {}
            if myType == 512: #'color', 'reflection', 'red', 'green', 'blue', 'hue', 'saturation', 'value'
                motor_info['position'] = self.reply['Motor_1']['position']
                motor_info['angle'] = self.reply['Motor_1']['angle']
                motor_info['speed'] = self.reply['Motor_1']['speed']
                
            if myType == 513:  #'leftStep', 'rightStep','leftAngle','rightAngle'
                motor_info['position'] = self.reply['Motor_1']['position']
                motor_info['angle'] = self.reply['Motor_1']['angle']
                motor_info['speed'] = self.reply['Motor_1']['speed']
                motor_info['position2'] = self.reply['Motor_2']['position']
                motor_info['angle2'] = self.reply['Motor_2']['angle']
                motor_info['speed2'] = self.reply['Motor_2']['speed']
            #print(motor_info, parameter, motor_info[parameter])
            return motor_info[parameter]
        except Exception as e:
            #print('Error in determining the motor value: ',e)
            return None
    @property
    def position(self):  return self._read('position')
    @property
    def angle(self): return self._read('angle')
    @property
    def speed(self): return self._read('speed')
    @property
    def position2(self):  return self._read('position2')
    @property
    def angle2(self): return self._read('angle2')
    @property
    def speed2(self): return self._read('speed2')

    def run(self, speed = 100, port = 1, direction = 2):
        return sync.hub_bridge("run", [speed, port, direction])
    def run_left(self, speed = 100, direction = 2):
        return sync.hub_bridge("run", [speed, 1, direction])
    def run_right(self, speed = 100, direction = 2):
        return sync.hub_bridge("run", [speed, 2, direction])
    def run_both(self, speed = 100, direction = 2):
        return sync.hub_bridge("runboth", [speed])
    def stop(self, port = 3):
        return sync.hub_bridge("stop", [port])
    def set_speed(self, speed = 100, port = 1):
        return sync.hub_bridge("myspeed", [speed, port])
    def set_speedL(self, speed = 100):
        return sync.hub_bridge("myspeed", [speed, 1])
    def set_speedR(self, speed = 100):
        return sync.hub_bridge("myspeed", [speed, 2])
    def run_angle(self, angle = 90, port = 1, direction = 2):
        return sync.hub_bridge("run_angle", [angle, port, direction])
    def run_angleL(self, angle = 90, direction = 2):
        return sync.hub_bridge("run_angle", [angle, 1, direction])
    def run_angleR(self, angle = 90, direction = 2):
        return sync.hub_bridge("run_angle", [angle, 2, direction])
    def run_to(self, pos = 10, port = 1, direction = 2):
        return sync.hub_bridge("run_to", [pos, port, direction])
    def run_toL(self, pos = 10, direction = 2):
        return sync.hub_bridge("run_to", [pos, 1, direction])
    def run_toR(self, pos = 10, direction = 2):
        return sync.hub_bridge("run_to", [pos, 2, direction])
    def update(self, rate = 20):
        return sync.hub_bridge("update_rate", [rate])
        