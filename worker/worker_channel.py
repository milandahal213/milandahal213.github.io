from pyscript import document, window, when, sync

CtrlC = document.getElementById('myButton')

def check_CtrlC():
    if CtrlC.classList.contains("pressed"):
        CtrlC.classList.toggle("pressed")
        CtrlC.innerText = "Abort?"
        raise KeyboardInterrupt("Manual interruption triggered.")

class Channel:
    def __init__(self):
        pass
    @property  # turns this into a read-only variable
    def msg(self):
        check_CtrlC()
        return sync.channel_bridge('msg',None)
    def send(self, msg):
        check_CtrlC()
        return sync.channel_bridge('send',msg)
    def post(self, topic, msg):
        check_CtrlC()
        payload = {}
        payload['topic'] = topic
        payload['msg'] = msg
        return sync.channel_bridge('post',payload)