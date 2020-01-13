#   m2q.py
#   THIS IS m2q in python
#   version 0.1
#   Date: 27/12/2019
#   Author: Lorenzo Fattori
#

# used libraries
import logging

import time

# other project files
import m2q_midi
import config
import m2q_comm

logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s", level=logging.DEBUG
)


# Main Function
if __name__ == "__main__":

    # load settings
    settings = config.loadSettings()

    # initialize UDP socket
    udpSocket = m2q_comm.udpSetup(settings["destinationIP"])

    # initialize midi
    midiin = m2q_midi.midiSetup(settings, udpSocket)

    # This is the main loop in the example
    print("Entering main loop. Press Control-C to exit.")
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("")
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin
