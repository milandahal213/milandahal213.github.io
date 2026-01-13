from pyscript import document, window, when

print('DOM')

# First set up the buttons
from dom_btns import *

# Next set up channels with the bridge
from SetupChannels import *

# Now setup the ble hub portion
from SetupHub import *

window.init.resolve({"hub_bridge":hub_bridge,"channel_bridge": channel_bridge,})


    