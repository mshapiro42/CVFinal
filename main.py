import cv2
import numpy as np
import musicalbeeps


def playHardCoded():
    player = musicalbeeps.Player(volume=0.3,
                                 mute_output=False)

    # Examples:
    tempo = 60 # beats per minute
    spb = 60/tempo # seconds per beat
    notes = ["E","D","C","D","E","E","E","D","D","D","E","G","G",
             "E","D","C","D","E","E","E","E","D","D","E","D","C"]
    durations = [.25,.25,.25,.25,.25,.25, .5,.25,.25, .5,.25,.25,.5,
                 .25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25, 1] #note lengths in beats
    for i in range(len(notes)):
        player.play_note(notes[i], spb * durations[i])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
        playHardCoded()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
