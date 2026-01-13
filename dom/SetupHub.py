from pyscript import document, window, when
import asyncio

import Hub 
class Element:
    """You can use this function to read or write to a tech element.
        element.update_rate(1000) will update all sensor readings every 1 sec
        element.value has the latest sensor reading selected by the dropdown menu
    """
    def __init__(self, divName = 'all_things_hubs', suffix = '_repl'): # hub0 = spike, hub1 = Old TE, hub2 = TE
        self._hub = Hub.Hub_basic(divName, suffix)  
        self.value = -1
        self.hubType = None
        self._hub.final_callback = self._new_data
        self._hub.info_callback = self._information

    async def _information(self, info):
        self.info = info
        try:
            self.hubType = info['GroupID']
            window.console.log(self.hubType)
            if self.hubType == 512:  # Single Motor
                def run(speed = 100, port = 1, direction = 2):
                    if speed != None:
                        self.set_speed(speed, port)
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_run')
                    self._send(fmt, ID, [port,direction]) 
                
                def myspeed(speed_value = 100, port = 1): 
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_speed')
                    self._send(fmt, ID, [port,speed_value]) 
                
                def stop(port = 1):  
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_stop')
                    self._send(fmt, ID, [port]) 
                    
                def moveAngle(angle = 100, port = 1, direction = 1):
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_angle')
                    self._send(fmt, ID, [port,angle,direction])
                    
                def movePos(pos = 100, port = 1, direction = 2):
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_abs_pos')
                    self._send(fmt, ID, [port,pos,direction])

                self.run = run
                self.stop = stop
                self.set_speed = myspeed  
                self.run_angle = moveAngle
                self.run_to = movePos
                
            if self.hubType == 513:  # Double Motor
                def run(speed = 100, port = 1, direction = 2): 
                    cmds = []
                    if port == 3:
                        if speed != None:
                            fmt, ID, val = self._hub.hubInfo.commands.get('motor_speed')
                            cmds.append((fmt, ID, [1,speed])) 
                            cmds.append((fmt, ID, [2,speed])) 
                        fmt, ID, val = self._hub.hubInfo.commands.get('motor_run')
                        cmds.append((fmt, ID, [1,direction & 0x03])) 
                        cmds.append((fmt, ID, [2,direction & 0x03])) 
                        self._sendMult(cmds) 
                    else:
                        if speed != None:
                            self.set_speed(speed, port)
                        fmt, ID, val = self._hub.hubInfo.commands.get('motor_run')
                        self._send(fmt, ID, [port,direction & 0x03]) 
                
                def myspeed(speed_value = 100, port = 1): 
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_speed')
                    self._send(fmt, ID, [port,speed_value]) 
                
                def stop(port = 3):  
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_stop')
                    cmds = []
                    if port == 3:
                        cmds.append((fmt, ID, [1])) 
                        cmds.append((fmt, ID, [2])) 
                        self._sendMult(cmds) 
                    else:
                        self._send(fmt, ID, [port]) 
                    
                def runL(speed = 100):
                    if speed != None:
                        self.set_speed(speed, 1)
                    self.run(None, 1,2)

                def runR(speed = 100):
                    if speed != None:
                        self.set_speed(-speed, 2)
                    self.run(None, 2,2)

                def runB(speed_value = 100):
                    cmds = []
                    if speed_value != None:
                        cmds = []
                        fmt, ID, val = self._hub.hubInfo.commands.get('motor_speed')
                        cmds.append((fmt, ID, [1,-speed_value])) 
                        cmds.append((fmt, ID, [2,speed_value])) 
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_run')
                    cmds.append((fmt, ID, [1,1])) 
                    cmds.append((fmt, ID, [2,2])) 
                    self._sendMult(cmds) 

                def moveAngle(angle = 100, port = 1, direction = 1):
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_angle')
                    self._send(fmt, ID, [port,angle,direction])

                def moveAngleL(angle = 100, direction = 1):
                    moveAngle(angle, direction)
                    
                def moveAngleR(angle = 100, direction = 1):
                    moveAngle(angle,2, direction)
                    
                def movePos(pos = 100, port = 1, direction = 2):
                    fmt, ID, val = self._hub.hubInfo.commands.get('motor_abs_pos')
                    self._send(fmt, ID, [port,pos,direction])

                def movePosL(pos = 100, direction = 2):
                    movePos(pos,1, direction)
                    
                def movePosR(pos = 100, direction = 2):
                    movePos(pos,2, direction)

                self.run = run
                self.stop = stop
                self.set_speed = myspeed  
                self.run_left = runL
                self.run_right = runR
                self.run_both = runB
                self.run_angle = moveAngle
                self.run_angle_left = moveAngleL
                self.run_angle_right = moveAngleR
                self.run_to = movePos
                self.run_to_left = movePosL
                self.run_to_right = movePosR
                
        except Exception as e:
            window.console.log('Error in _information: ',e)

    async def _sendIt(self, fmt, ID, val):
        try:
            await self._hub.send(fmt, ID, val) 
            window.console.log('sent: ',fmt, ID, val)
            return True
        except asyncio.CancelledError:
            print("Task was cancelled due to timeout.")
            raise
        return  False
        
    async def _sendItMult(self, cmds):
        try:
            for (fmt, ID, val) in cmds:
                await self._hub.send(fmt, ID, val) 
                await asyncio.sleep(0.1)
                window.console.log('sent: ',fmt, ID, val)
            return True
        except asyncio.CancelledError:
            print("Task was cancelled due to timeout.")
            raise
        return  False
        
    def _send(self, fmt, ID, val):
        loop = asyncio.get_event_loop()
        # window.console.log('I think I sent: ',fmt, ID, val)
        try:
            task = asyncio.wait_for(self._sendIt(fmt, ID, val), timeout=6)
            loop.create_task(task)
            return True
        except asyncio.TimeoutError:
            print("A timeout occurred in the sync function!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    def _sendMult(self,cmds):
        loop = asyncio.get_event_loop()
        # window.console.log('I think I sent: ',cmds)
        try:
            task = asyncio.wait_for(self._sendItMult(cmds), timeout=6)
            loop.create_task(task)
            return True
        except asyncio.TimeoutError:
            print("A timeout occurred in the sync function!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    async def _new_data(self, reply):
        try:
            self.value = self._hub.value
            reply = self._hub.reply
            if 'Motor_1' in reply.keys():
                self.position = reply['Motor_1']['position']
                #window.console.log(self.position)
                self.angle = reply['Motor_1']['angle']
                self.speed = reply['Motor_1']['speed']
                #self.battery = reply['hub info']['Battery']
                
            if 'Motor_2' in reply.keys():
                self.position2 = reply['Motor_2']['position']
                self.angle2 = reply['Motor_2']['angle']
                self.speed2 = reply['Motor_2']['speed']
                #self.battery2 = reply['hub info']['Battery']
                
            if 'Color' in reply.keys(): #'color', 'reflection', 'red', 'green', 'blue', 'hue', 'saturation', 'value'
                self.color = reply['Color']['color']
                self.reflection = reply['Color']['reflection']
                self.rgb = (reply['Color']['red'], reply['Color']['green'], reply['Color']['blue'])
                self.hsv = (reply['Color']['hue'], reply['Color']['stauration'], reply['Color']['value'])
                #self.battery = reply['hub info']['Battery']
                
            if 'Joystick' in reply.keys():  #'leftStep', 'rightStep','leftAngle','rightAngle'
                self.leftStep = reply['Joystick']['leftStep']
                self.rightStep = reply['Joystick']['rightStep']
                self.leftAngle = reply['Joystick']['leftAngle']
                self.rightAngle = reply['Joystick']['rightAngle']
                #self.battery = reply['hub info']['Battery']
        except:
            pass

    async def update_rate(self,rate = 20):
        await self._hub.feed_rate(rate)  #millisec - 20 is the fastest

tech = Element('all_things_hubs', '_1')

#   This is now all done in ask...
#await tech.update_rate(20)
#_e1 = document.getElementById('var_1')
#_e1.value = 'motor'

@when('change','#var_1')
def rename():
    _e1.value = _e1.value.replace(' ','_')
    exec(f"{_e1.value} = tech ")

def hub_bridge(cmd, array = []):
    try:
        if cmd == 'hubType':
            return tech.hubType
        elif cmd == 'reply':
            return tech._hub.reply
        elif cmd == 'run':
            tech.run(*array) # speed=speed, port=port, direction=direction      
        elif cmd == 'runboth':
            tech.run_both(*array) # speed=speed, port=port, direction=direction      
        elif cmd == 'stop':
            tech.stop(*array) # port=port       
        elif cmd == 'myspeed':
            tech.set_speed(*array)  #  speed=speed, port=port        
        elif cmd == 'run_angle':
            tech.run_angle(*array) # angle=angle, port = port, direction=direction        
        elif cmd == 'run_to':
            tech.run_to(*array) # pos=position, port = port, direction=direction    
        elif cmd == 'update_rate':
            await tech.update_rate(*array)  # update rate
        else:
            return None   
    except Exception as e:
        print('George Error ', e)
        return False
    return True

