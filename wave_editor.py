import math
import os
import wave_helper

MIN = -32768
MAX = 32767
SAMPLE_RATE = 2000

# main menu #
EDIT = '1'
COMPOSE = '2'
EXIT = '3'

# change wav file #
REVERSE = '1'
INVERSE = '2'
SPEED_UP = '3'
SPEED_DOWN = '4'
VOLUME_UP = '5'
VOLUME_DOWN = '6'
LOW_PASS_FILTER = '7'
EXIT_MENU = '8'
POSSIBLE_INPUTS = ['1', '2', '3', '4', '5', '6', '7', '8']

# compose wav file #
NOTES = {'A': 440, 'B': 494, 'C': 523, 'D': 587, 'E': 659, 'F': 698,
         'G': 784, 'Q': 0}


def print_main_menu():
    """
    prints the main menu of the program for the user
    :return: None
    """
    print("* MAIN MENU *")
    print("Welcome to the wav-file editor! Here are your options:")
    print("To edit a wav file - enter 1")
    print("To compose a new tune - enter 2")
    print("To exit the program - enter 3")


def print_edit_menu():
    """
    prints the edit menu of the program
    :return: None
    """
    print("* EDIT MENU *")
    print("Options:")
    print("Enter 1 to reverse the tune")
    print("Enter 2 to inverse the tune")
    print("Enter 3 to speed up the tune")
    print("Enter 4 to speed down the tune")
    print("Enter 5 to increase volume")
    print("Enter 6 to decrease volume")
    print("Enter 7 to apply a low pass filter")
    print("Enter 8 to save and go to exit menu")


def main_menu():
    """
    main menu of the program, prints the menu and asks the user to pick
    their desired action, then redirects the code to chosen action's function
    :return: None
    """
    while True:
        print_main_menu()
        user_input = input()
        if user_input == EDIT:
            edit_wav()
        elif user_input == COMPOSE:
            composed = compose_tune()
            edit_wav(composed)
        elif user_input == EXIT:
            return
        else:
            print("Invalid input.")


def calc_average(lst_of_lst):
    """
    takes a list of lists, and calculates the average of every column.
    :param lst_of_lst: a list of list
    :return: a list: [average of column 1, average of column 2]
    """
    sum_col_0 = 0
    sum_col_1 = 0
    for lst in lst_of_lst:
        sum_col_0 += lst[0]
        sum_col_1 += lst[1]
    avg_col_0 = int(sum_col_0 / len(lst_of_lst))
    avg_col_1 = int(sum_col_1 / len(lst_of_lst))
    return [avg_col_0, avg_col_1]


# edit wav file #
def edit_wav(data_list=None):
    """
    responsible for redirecting the code to the requested editing options,
    according to the user's choice.
    :param data_list: audio wav file as a list of lists. set to None as
    default when the user is editing an existing file (then the data is
    extracted by another function).
    :return: None
    """
    if data_list is None:  # if user is editing an existing wav file
        sample_rate, data_list = get_file_input()
    else:  # if user is editing a composed tune
        sample_rate = SAMPLE_RATE
    while True:
        print_edit_menu()  # prints the menu with the various editing options
        option_input = get_option_input()
        if option_input == REVERSE:
            new_data_list = reverser(data_list)
        if option_input == INVERSE:
            new_data_list = inverse(data_list)
        if option_input == SPEED_UP:
            new_data_list = inc_speed(data_list)
        if option_input == SPEED_DOWN:
            new_data_list = dec_speed(data_list)
        if option_input == VOLUME_UP:
            new_data_list = inc_volume(data_list)
        if option_input == VOLUME_DOWN:
            new_data_list = dec_volume(data_list)
        if option_input == LOW_PASS_FILTER:
            new_data_list = low_pass_filter(data_list)
        if option_input == EXIT_MENU:
            save_file(sample_rate, data_list)
            return
        print("Editing done!")
        data_list = new_data_list  # as returned from the editor function


def get_file_input():
    """
    loads the file the user wants to edit after asking for a file name as input
    :return: a tuple with the sample rate and data list of loaded wav file
    """
    while True:
        file_input = input("Pick a file to edit: ")
        tup = wave_helper.load_wave(file_input)
        if tup == -1:
            print("There was a problem loading the file, please try again.")
        else:
            return tup


def get_option_input():
    """
    asks the user for an input of the change they'd like to make to their
    file, and checks if the given input is valid (i.e if the input is one
    of the 8 possible options given). if the input is invalid, it asks the
    user to enter another input.
    :return: user input- string
    """
    while True:
        option_input = input("Pick the change you would like to make to your file: ")
        if option_input not in POSSIBLE_INPUTS:
            print("Invalid input, try again.")
        else:
            return option_input


def reverser(data_list):  # 1
    """
    reverses the sound to play backwards
    :param data_list: audio wav file as list of lists
    :return: list of lists with the reversed sound
    """
    new_data_list = data_list[::-1]  # flips the order of the list
    return new_data_list


def inverse(data_list):  # 2
    """
    inverses the audio sound by replacing the ints in the list with their
    opposite number
    :param data_list: audio wav file as list of lists
    :return: edited list of lists
    """
    inverse_lst = []
    for lst in data_list:
        inverse_ind = []
        for elem in lst:
            if elem == MIN:  # in case int is the minimum value, then the
                # opposite is beyond the limits
                inverse_ind.append(MAX)
            else:
                elem *= -1
                inverse_ind.append(elem)
        inverse_lst.append(inverse_ind)
    return inverse_lst


def inc_speed(data_list):  # 3
    """
    speeds up the audio by removing half of sounds
    :param data_list: audio wav file as list of lists
    :return: list of lists with the alternated sound
    """
    new_data_list = [data_list[i] for i in range(len(data_list))
                     if i % 2 == 0]  # takes only even locations from list
    return new_data_list


def dec_speed(data_list):  # 4
    """
    decreases the speed of the audio by adding the average of each couple
    of consecutive objects in the middle of them
    :param data_list: audio wav file as list of lists
    :return: edited list of lists
    """
    if data_list == []:
        return []
    new_data_lst = [data_list[0]]  # starts with the first object of the
    # original list already inside, since it has no previous object

    # calculates average for the rest of the list
    for i in range(len(data_list) - 1):
        avg = calc_average([data_list[i], data_list[i+1]])
        new_data_lst.append(avg)
        new_data_lst.append(data_list[i+1])
    return new_data_lst


def inc_volume(data_list):  # 5
    """
    increases the volume by multiplying the values by 1.2
    :param data_list: audio wav file as list of lists
    :return: edited list of lists with higher volume
    """
    if not data_list:
        return []
    if data_list == [[]]:
        return data_list
    new_data_list = [[int(note[0] * 1.2), int(note[1] * 1.2)] for note in data_list]
    for note in new_data_list:
        # corrects in case the values exceed the maximum/minimum values:
        for i in range(len(note)):
            if note[i] > MAX:
                note[i] = MAX
            elif note[i] < MIN:
                note[i] = MIN
    return new_data_list


def dec_volume(data_list):  # 6
    """
    lowers the volume of the audio by dividing the values by 1.2
    :param data_list: audio wav file as list of lists
    :return: edited list of lists with lower volume
    """
    decreased_lst = []
    for lst in data_list:
        decreased_ind = []
        for elem in lst:
            elem = int(elem / 1.2)
            if elem < MIN:  # in case the values exceed the max/min values:
                elem = MIN
            decreased_ind.append(elem)
        decreased_lst.append(decreased_ind)
    return decreased_lst


def low_pass_filter(data_list):  # 7
    """
    filters the sound by averaging each sound with its predecessor and follower
    :param data_list: audio wav file as list of lists
    :return: edited list of lists, with low pass filter
    """
    if len(data_list) == 1:
        return data_list
    first_avg = calc_average([data_list[0], data_list[1]])  # calculates the
    # first average separately because the first object has no predecessor
    new_data_list = [first_avg]

    for i in range(1, len(data_list) - 1):  # average for the rest of the list
        avg = calc_average([data_list[i-1], data_list[i], data_list[i+1]])
        new_data_list.append(avg)

    last_avg = calc_average([data_list[-2], data_list[-1]])  # calculates the
    # last average separately because the last object has no follower
    new_data_list.append(last_avg)
    return new_data_list


def save_file(sample_rate, data_list):
    """
    saves the edited file after asking the user for a file name as input
    :param sample_rate: the audio's original sample rate- an integer
    :param data_list: edited data list- list of lists
    :return: None
    """
    while True:
        name_input = input("Pick a name for the file to be saved as: ")
        save = wave_helper.save_wave(sample_rate, data_list, name_input)
        if save == -1:
            print("There was a problem saving the file, please try again.")
        else:
            return


# compose tune #
def compose_tune():
    """
    directs the code to the sub functions that are responsible for
    composing a new tune- gets an input of instructions as a .txt file then
    translates them into the desired audio.
    :return: None
    """
    raw_instructions = get_composition_file()
    sound_instructions = instructions_breaker(raw_instructions)
    data_list = sound_interpreter(sound_instructions)
    return data_list


def get_composition_file():
    """
    gets the name of a file with the audio instructions and checks if it
    exists. if the file exists, the function reads it's contents.
    :return: a list containing the instructions as a string
    """
    while True:
        file_input = input("Enter the name of the file with your "
                           "composition instructions: ")
        if os.path.exists(file_input) is False:
            print("Invalid input, try again.")
        else:
            with open(file_input, 'r') as comp_file:
                instructions = comp_file.readlines()
            return instructions


def instructions_breaker(instructions):
    """
    edits the raw instructions taken from the file into the correct format
    that the function sound_interpreter uses.
    :param instructions: a list of the raw instructions, containing letters
    and ints
    :return: a list of lists, where every sublist contains the key of the
    note as a string, and the length of the note as an int.
    """
    all_in_one_line = ""
    for line in instructions:
        all_in_one_line += line.replace('\n', ' ')  # adds all elements to one
        # long string by replacing newlines with spaces
    all_in_one_list = all_in_one_line.split()  # puts each element as a
    # separate string

    final_instructions = []
    for i in range(0, len(all_in_one_list), 2):
        final_instructions.append([all_in_one_list[i], int(all_in_one_list[
            i+1])])  # arranges the elements as sublists in pairs of key, int
    return final_instructions


def note_breaker(note):
    """
    the function that do the complex calculations of changing each note
    into it's digital sin wave
    :param note: a list with the key of a single note
    ('A' for example), and the length of the note as an int.
    :return: list of lists with the digital waves of the note
    """
    diginote = []
    if NOTES[note[0]] == 0:  # in case the key is 'Q'
        samples_per_cycle = 0
    else:
        samples_per_cycle = SAMPLE_RATE / NOTES[note[0]]
    for i in range(note[1] * 125):
        # the amount of returns according to the time of the note
        if samples_per_cycle == 0:  # in case the key is 'Q'
            diginote.append([0, 0])
        else:
            result = MAX * math.sin(math.pi * 2 * (i / samples_per_cycle))
            diginote.append([int(result), int(result)])
    return diginote


def sound_interpreter(sound_instructions):
    """
    translates the written notes and lengths into the digital waves
    :param sound_instructions: a list of lists, where every sublist contains
    the key of the note ('A' for example) as a string, and the length of the
    note as an int
    :return: list of lists with the digital waves of the notes according to
    their lengths
    """
    final_output = []
    for note in sound_instructions:
        diginote = note_breaker(note)
        for note in diginote:
            final_output.append(note)
    return final_output


if __name__ == '__main__':
    main_menu()
