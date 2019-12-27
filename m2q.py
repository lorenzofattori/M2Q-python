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

# log = logging.getLogger("midiin_callback")
# logging.basicConfig(level=logging.DEBUG)


# Main Function
if __name__ == "__main__":
    midiin = m2q_midi.midiSetup()

    # beatCounter = 0 # Used for Midi BeatClock (counting 24 times every 4/4)

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
