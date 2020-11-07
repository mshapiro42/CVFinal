import cv2
import numpy as np
import musicalbeeps

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    player = musicalbeeps.Player(volume=0.3,
                                 mute_output=False)

    # Examples:
    tempo = 60 # beats per minute
    spb = 60/tempo
    notes = ["E","D","C","D","E","E","E","D","D","D","E","G","G",
             "E","D","C","D","E","E","E","D","E","E","E","D","C"]
    durations = [.25,.25,.25,.25,.25,.25,.5,.25,.25,.5,.25,.25,.5,
                 .25,.25,.25,.25,.25,.25,.25,.25,.25,.25,.25,1]
    for i in range(len(notes)):
        player.play_note(notes[i],spb*durations[i])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
