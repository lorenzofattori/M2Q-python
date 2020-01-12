import json


def loadSettings():
    settings = {
        "destinationIP": [255, 255, 255, 255],
        "sourcePort": 6553,
        "destPort": 6553,
        "jumpMode": True,
        "levelMode": True,
        "cueStackMode": True,
        "tapToTempoMode": True,
        "wingMode": False,
    }
    # load settings from file
    try:
        with open("settings.json") as prefs_file:
            settings = json.load(prefs_file)
    except FileNotFoundError:
        print("Error, settings.json file not found, using default values")

    print("Current settings:")
    print(settings)

    return settings


def saveSettings(settings):
    # save settings to file
    with open("settings.json", "w") as prefs_file:
        json.dump(settings, prefs_file)
