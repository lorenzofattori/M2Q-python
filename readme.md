<img src="https://i.imgur.com/skcF7OB.png" title="M2Q" alt="M2Q">

# M2Q

> A powerful MIDI to Chamsys Remote converter designed to trigger playbacks, cuestacks and synchronize tap to tempo with MIDI Clock
>

<img src="https://i.imgur.com/n8j722k.png" title="M2Q" alt="M2Q">



# About M2Q
- It's written in Python by Lorenzo Fattori from an idea of Manuel Rodrigues.
- It went trought multiple iterations before landing as a Python application.
- It's the first time I write a Python application and GUI, I'm sure there are a lot of improvements points, feel free to send a PR!
- It's still in development phase, any problem, suggestion or bug requests please create an Issue on Github.


# How it works
- M2Q Listens to MIDI Note, MIDI ControlChange and MIDI Clock messages incoming in the selected MIDI interface.
- When one of these messages it's received, it gets processed and a Chamsys Remote message is sent out to the destination IP address and Port specified.
- Works with both Chamsys consoles and MagicQ PC, software needs to be unlocked and only the first 10 playbacks are available in the PC version.

### Triggering Playbacks
Triggering Playbacks is used for remotely activate and switch cues inside a playback of MagicQ. This can be useful for real-time cue triggering without having to use Timecode.
- When you send a Note ON message on note X of MIDI Channel Y, M2Q will convert it in trigger Note X of Playback Y.
- Works witrh Playback 1-15 an corresponds of the first 15 Playbacks of the Console (Note: M2Q PC is limited to the first 10 Playbacks).
- Up to 126 Cues can be triggered.

### Changing Playback Level
Changing Playback Level is used for remotely change level of a playback of MagicQ like moving the console faders Up/Down. This can be useful for real-time ifades without having to use Timecode.
- When you send a ControlChange message with value X on Controller 1 of MIDI Channel Y, M2Q will convert it in change playback Y level to X value (0-100%).
- Works witrh Playback 1-15 an corresponds of the first 15 Playbacks of the Console (Note: M2Q PC is limited to the first 10 Playbacks).
- Value from 0 to 100 corresponds to playback level 0 to 100%, from 101 to 126 is kept to 100%.

### Triggering The Stack Store
Triggering The Stack Store is used for remotely activate/deactivate cue stacks inside the Stack Store of MagicQ. This can be useful for real-time cue flashing or activating chases having to use Timecode.
- When you send a Note ON or Note OFF message on note X of MIDI Channel 16, M2Q will convert it in activate/deactivate cuestack X of the Stack Store.
- Works witrh Playback 1-15 an corresponds of the first 15 Playbacks of the Console (Note: M2Q PC is limited to the first 10 Playbacks).
- Up to 126 Cues can be triggered.

### Tap2Tempo Trigger
Tap2Tempo Trigger is used to synchronize the MIDI clock to the internal console global tempo (BPM) by remotely tap to the GO button of MagicQ. This can be useful for synchronizing Chamsys effects to MIDI Clock.
- When a MIDI clock message is received, a Chamsys message for the remote trigger is sent out.
- The remote trigger needs to be set up as Tap to time sel PB.

### Wing Mode
When selected, it will trigger the playbacks from 11 to 25 instead of 1 to 25, in this way you can still use your first 10 playbacks manually and have the "automated" triggering on the first wing playbacks


# Set UP Chamsys
- Software needs to be unlocked in order to receive remote control messages
- Settings > Multi Console > Enable remote control and Enabler remote access: YES
- Settings > Network > Chamsys remote protocol: Chamsys Rem (TX+RX no header)
- Settings > Network > Playback sync port: must be the same of M2Q (default 6553)
- Settings > Ports > Remote trigger type: Make + Break
- Settings > Ports > Remote trigger action: Tap to time sel PB
- Settings > Playback > Crossfade button function: Global Tap to time

