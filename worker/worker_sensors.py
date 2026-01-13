from pyscript import document, window, when, sync

CtrlC = document.getElementById('myButton')

def check_CtrlC():
    if CtrlC.classList.contains("pressed"):
        CtrlC.classList.toggle("pressed")
        CtrlC.innerText = "Abort?"
        raise KeyboardInterrupt("Manual interruption triggered.")

class Sensor:
    def __init__(self):
        self._Type = None

    def __dir__(self):
        # Get standard attributes
        attrs = list(type(self).__dict__.keys()) + list(self.__dict__.keys())

        if self._Type == 514:
            if 'color' not in attrs: attrs.append('color')
            if 'reflection' not in attrs: attrs.append('reflection')
            if 'rgb' not in attrs: attrs.append('rgb')
            if 'hsv' not in attrs: attrs.append('hsv')
        elif self._Type == 515:
            if 'leftStep' not in attrs: attrs.append('leftStep')
            if 'rightStep' not in attrs: attrs.append('rightStep')
            if 'leftAngle' not in attrs: attrs.append('leftAngle')
            if 'rightAngle' not in attrs: attrs.append('rightAngle')
        else:
            if 'color' in attrs:  attrs.remove('color')
            if 'reflection' in attrs:  attrs.remove('reflection')
            if 'rgb' in attrs:  attrs.remove('rgb')
            if 'hsv' in attrs:  attrs.remove('hsv')
            if 'leftStep' in attrs:  attrs.remove('leftStep')
            if 'rightStep' in attrs:  attrs.remove('rightStep')
            if 'leftAngle' in attrs:  attrs.remove('leftAngle')
            if 'rightAngle' in attrs:  attrs.remove('rightAngle')
        
        return sorted(set(attrs))
        
    @property
    def hubType(self):
        check_CtrlC()
        self._Type = sync.hub_bridge('hubType')
        return self._Type

    def _read(self, parameter):
        try:
            if not self.hubType: 
                return None
            check_CtrlC()
            self.reply = sync.hub_bridge('reply')
            #if parameter == 'battery': 
            #    return self.reply['hub info']['Battery']
            sensor_info = {}
            if self._Type == 514: #'color', 'reflection', 'red', 'green', 'blue', 'hue', 'saturation', 'value'
                sensor_info['color'] = self.reply['Color']['color']
                sensor_info['reflection'] = self.reply['Color']['reflection']
                sensor_info['rgb'] = (self.reply['Color']['red'], self.reply['Color']['green'], self.reply['Color']['blue'])
                sensor_info['hsv'] = (self.reply['Color']['hue'], self.reply['Color']['stauration'], self.reply['Color']['value'])
                
            if self._Type == 515:  #'leftStep', 'rightStep','leftAngle','rightAngle'
                sensor_info['leftStep'] = self.reply['Joystick']['leftStep']
                sensor_info['rightStep'] = self.reply['Joystick']['rightStep']
                sensor_info['leftAngle'] = self.reply['Joystick']['leftAngle']
                sensor_info['rightAngle'] = self.reply['Joystick']['rightAngle']
            #print(sensor_info, parameter, sensor_info[parameter])
            return sensor_info[parameter]
        except Exception as e:
            #print('Error in determining the sensor value: ',e)
            return None
    @property
    def color(self): return self._read('color')
    @property
    def reflection(self): return self._read('reflection')
    @property
    def rgb(self): return self._read('rgb')
    @property
    def hsv(self): return self._read('hsv')
    @property
    def leftStep(self): return self._read('leftStep')
    @property
    def rightStep(self): return self._read('rightStep')
    @property
    def leftAngle(self): return self._read('leftAngle')
    @property
    def rightAngle(self): return self._read('rightAngle')
        
    def update(self, rate = 20):
        return sync.hub_bridge("update_rate", [rate])
        