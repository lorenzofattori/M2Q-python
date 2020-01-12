import logging


def createMessage(messageType, channel, note, settings):
    # creates a chamsys remote message

    logging.debug(
        f"createMessage: messageType: {messageType}, channel: {channel}, note: {note}"
    )

    if settings["wingMode"] == True:
        # check if wingmode is activated (move playback to +10)
        channel += 10

    if messageType == 0:
        if settings["jumpMode"] == True:
            return str(channel) + "," + str(note) + ",0J"

    elif messageType == 1:
        if settings["levelMode"] == True:
            return str(channel) + "," + str(note) + ",L"

    elif messageType == 2:
        if settings["cueStackMode"] == True:
            return "\\<82>," + str(note) + "H"

    elif messageType == 3:
        if settings["cueStackMode"] == True:
            return "\\<83>," + str(note) + "H"

    elif messageType == 4:
        if settings["tapToTempoMode"] == True:
            return "\\<71>2H"

    else:
        return None



def sendUdp(message):
    logging.debug(message)
