from pyscript import document, window, when
import asyncio

async def run_button(event):
    python_terminal.process('\x03')
    code = event.code
    python_terminal.process('\x05')
    mycode = mpython.code
    lines = mycode.split("\n")
    for line in lines:
        python_terminal.process(line)
        await asyncio.sleep(0.1)
    python_terminal.process('\x04')
    return False  # return False to avoid executing on browser

python = document.getElementById('python-local')
python_terminal = document.getElementById('python-terminal')
mpython = document.getElementById('python-worker')
mpython.handleEvent = run_button

@when('click','#REPL_Run')
async def typeIt():
    #python_terminal.process('\x03')
    mycode = mpython.code
    lines = mycode.split("\n")
    for line in lines:
        python_terminal.process(line)
        await asyncio.sleep(0.1)

@when('click','#REPL_RunE')
async def typeIt2():
    python_terminal.process('\x05')
    await typeIt()
    python_terminal.process('\x04')

CtrlC = document.getElementById('myButton')

@when('click','#myButton')
def toggle_button(event):
    CtrlC.classList.toggle("pressed")
    if "pressed" in CtrlC.classList:
        CtrlC.innerText = "Aborting..."
    else:
        CtrlC.innerText = "Abort?"

code_area = document.getElementById('python-worker')

@when('click','#UT_channel')
def on_channel():
    with open('channels_test.py', 'r') as f: mycode = f.read()
    code_area.code = mycode

@when('click','#UT_single')
def on_single():
    with open('single_motor_test.py', 'r') as f: mycode = f.read()
    code_area.code = mycode

@when('click','#UT_double')
def on_double():
    with open('double_motor_test.py', 'r') as f: mycode = f.read()
    code_area.code = mycode
    
@when('click','#UT_color')
def on_color():
    with open('color_sensor_test.py', 'r') as f: mycode = f.read()
    code_area.code = mycode
    
@when('click','#UT_controller')
def on_controller():
    with open('controller_test.py', 'r') as f: mycode = f.read()
    code_area.code = mycode