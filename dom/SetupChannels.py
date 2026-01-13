from pyscript import document, window
import asyncio
import channel as _ch

mytopic = '/LEGO'
myChannel = _ch.CEEO_Channel("hackathon", "@chrisrogers", "talking-on-a-channel",
                                 divName = 'all_things_channels', suffix='_test', default_topic = mytopic)
document.getElementById('topic_test').innerHTML = mytopic

class Channel:
    """You can use this function to read or write to the channel.
        channel.send('some text') will send a string (or number) on topic '/LEGO'
        channel.msg has the latest message on the '/LEGO' channel
    """
    def __init__(self):
        self.msg = None
        self.topic = None
        self.value = -1
        myChannel.callback = self._receive 
    
    def _receive(self, message):
        thetopic = document.getElementById('topic_test').value
        topic, msg = myChannel.check(thetopic, message)
        if msg:  
            self.msg = msg
            self.topic = topic
            try:
                number = float(msg)
                self.value = int(number) if number % 1.0 == 0 else number
            except:
                self.value = -1
            
    async def _sendIt(self, msg):
        thetopic = document.getElementById('topic_test').value
        await myChannel.post(thetopic, msg)
        await asyncio.sleep(0.1)
        
    def send(self, msg):
        loop = asyncio.get_event_loop()
        success = loop.create_task(self._sendIt(msg))
        
    async def _postIt(self, topic, msg):
        await myChannel.post(topic, msg)
        await asyncio.sleep(0.1)
        
    def post(self, topic, msg):
        loop = asyncio.get_event_loop()
        success = loop.create_task(self._postIt(topic, msg))

channel = Channel()

def channel_bridge(cmd,msg):
    if cmd == 'msg':
        return channel.msg
    elif cmd == 'post':
        return channel.post(msg['topic'], msg['msg'])
    else:
        return channel.send(msg)
