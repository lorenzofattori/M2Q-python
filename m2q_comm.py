import logging
import socket
import sys


def createMessage(messageType, channel, note, wingMode):
    # creates a chamsys remote message

    logging.debug(
        f"createMessage: messageType: {messageType}, channel: {channel}, note: {note}"
    )

    if wingMode == True:
        # check if wingmode is activated (move playback to +10)
        channel += 10

    if messageType == 0:
        return str(channel) + "," + str(note) + ",0J"

    elif messageType == 1:
        return str(channel) + "," + str(note) + ",L"

    elif messageType == 2:
        return "\\<82>," + str(note) + "H"

    elif messageType == 3:
        return "\\<83>," + str(note) + "H"

    elif messageType == 4:
        return "\\<71>,2H"

    else:
        return None


def sendUdp(udpSocket, message, destinationIP, destPort):
    logging.debug(message)
    logging.debug(f"{destinationIP}, {destPort}")

    try:
        udpSocket.sendto(bytes(message, "utf-8"), (destinationIP, destPort))
    except socket.error:
        logging.warning("Failed send UDP")
        # sys.exit()


def udpSetup(destinationIP):

    try:
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        logging.warning("Failed to create UDP Socket")
        sys.exit()

    # udpSocket.bind(("", srcPort))

    # this command is used to enable broadcasts, if you use unicast it's not necessary
    if destinationIP == "255.255.255.255":
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    return udpSocket
