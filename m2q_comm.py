import logging
import socket
import sys


def create_message(message_type, channel, note, wing_mode):
    # creates a chamsys remote message

    logging.debug("createMessage: message_type: %s, channel: %s, note: %s",
                  message_type, channel, note)

    # Handles weird case where note or channel are out of the expected midi ranges
    if note < 0 or note > 127:
        return None
    if channel < 0 or channel > 15:
        return None

    if wing_mode:
        # check if wing_mode is activated (move playback to +10)
        channel += 10

    if message_type == 0:
        return str(channel) + "," + str(note) + ",0J"

    if message_type == 1:
        return str(channel) + "," + str(note) + ",L"

    if message_type == 2:
        return "\\<82>," + str(note) + "H"

    if message_type == 3:
        return "\\<83>," + str(note) + "H"

    if message_type == 4:
        return "\\<71>,2H"

    return None


def send_udp(udp_socket, message, destination_ip, dest_port, user_interface):
    logging.debug(message)
    logging.debug("%s %s", destination_ip, dest_port)

    try:
        udp_socket.sendto(bytes(message, "utf-8"), (destination_ip, dest_port))
        user_interface.flash("chamsys")
    except socket.error:
        logging.warning("Failed send UDP")
        user_interface.flash("ERROR")
        # sys.exit()


def udp_setup():

    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        logging.warning("Failed to create UDP Socket")
        sys.exit()

    # allow broadcasts
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    return udp_socket
