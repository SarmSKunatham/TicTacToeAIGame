import speech_recognition as sr
import time

#for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
# Microphone
mic = sr.Microphone(2)
# Recognizer
r = sr.Recognizer()

spellLists = {
    "1": ["1", "11", "one", "wan", "fun"],
    "2": ["2", "22", "two", "too", "foo", "tube"],
    "3": ["3", "33", "three", "free", "tree", "tee", "thee"],
    "4": ["4", "44", "four", "for", "fo", "foe"],
    "5": ["5", "55", "five", "fight", "fire"],
    "6": ["6", "66", "six", "sex", "sig", "sit"],
    "7": ["7", "77", "seven", "swan", "sen"],
    "8": ["8", "88", "eight", "egg", "eache"],
    "9": ["9", "99", "nine", "nigh", "night"]
}

while True:
    with mic as source:
        print('Command should be your position that you want to put your mark [1-9].')
        print('Tell your command: ')
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        text = text.lower()
        print(f"text: {text}")
        # command 1
        if str(text) in spellLists["1"]:
            print(f"=====================================")
            print(f"Your command is marking position : 1")
            print(f"=====================================")
        # command 2
        elif str(text) in spellLists["2"]:
            print(f"=====================================")
            print(f"Your command is marking position : 2")
            print(f"=====================================")
        # command 3
        elif str(text) in spellLists["3"]:
            print(f"=====================================")
            print(f"Your command is marking position : 3")
            print(f"=====================================")
        # command 4
        elif str(text) in spellLists["4"]:
            print(f"=====================================")
            print(f"Your command is marking position : 4")
            print(f"=====================================")
        # command 5
        elif str(text) in spellLists["5"]:
            print(f"=====================================")
            print(f"Your command is marking position : 5")
            print(f"=====================================")
        # command 6
        elif str(text) in spellLists["6"]:
            print(f"=====================================")
            print(f"Your command is marking position : 6")
            print(f"=====================================")
        # command 7
        elif str(text) in spellLists["7"]:
            print(f"=====================================")
            print(f"Your command is marking position : 7")
            print(f"=====================================")
        # command 8
        elif str(text) in spellLists["8"]:
            print(f"=====================================")
            print(f"Your command is marking position : 8")
            print(f"=====================================")
        # command 9
        elif str(text) in spellLists["9"]:
            print(f"=====================================")
            print(f"Your command is marking position : 9")
            print(f"=====================================")
        else:
            print('Please give a right command.')
            continue
    except:
        print('Sorry could not recogonize your voice.')
        continue