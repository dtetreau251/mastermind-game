import requests


def main():
    # add input validation
    name = input("What is your name? ")
    computer_choice_list_master = []
    player_guess_list_master = []
    player_guess_list_cumulative = []
    attempts = 10
    while attempts > 0:
        if not computer_choice_list_master:
            # string version of api response representing the computer player number choices
            computer_player_numbers = choose_computer_player_numbers()
            # turn the string version of the api response into a list of strings
            computer_choice_list_master = make_computer_choice_list(
                computer_player_numbers
            )
        print(computer_choice_list_master)
        # list of strings from user representing their four guesses in order
        player_guess_list_master = make_player_guess_list(
            name, player_guess_list_cumulative
        )
        # add the current guesses to the list of previous guesses
        player_guess_list_cumulative.append(player_guess_list_master)
        # checks the player guesses against the computer player choices and returns the number of correct locations
        correct_locations = check_correct_locations(
            player_guess_list_master, computer_choice_list_master
        )
        # check the amount of numbers that were guessed correctly
        correct_numbers = check_correct_numbers(
            player_guess_list_master, computer_choice_list_master
        )
        # check whether the game should continue and print appropriate message
        check_game_condition(correct_locations, correct_numbers, name)
        # reduce the number of attempts until 10 attempts are made
        attempts -= 1
    print(
        "You have failed to guess the secret numbers within "
        + str(attempts)
        + " attempts. Game Over."
    )


def choose_computer_player_numbers():
    # add async await python equivalent
    api_url = "https://www.random.org/integers?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
    response = requests.get(api_url)
    if response.status_code == 200:
        # string representation of the api response
        return response.text
    else:
        print("The server responded with status code: " + response.status_code)
        quit()


def make_computer_choice_list(computer_player_numbers):
    # a list of strings representing the numbers chosen by the computer player (from api)
    computer_number_choices = []
    # find the digits in the string representation of the api response and append to list
    for char in computer_player_numbers:
        if char.isdigit():
            computer_number_choices.append(char)
        else:
            continue
    return computer_number_choices


def make_player_guess_list(name, player_guess_list_cumulative):
    # add terminal colors and effects
    # add termainal text formatting
    if player_guess_list_cumulative:
        print(
            name + ", your previous guesses were " + str(player_guess_list_cumulative)
        )
    # add input validation
    guess1 = input("Please guess the first number: ")
    guess2 = input("Please guess the second number: ")
    guess3 = input("Please guess the third number: ")
    guess4 = input("Please guess the fourth number: ")
    return [guess1, guess2, guess3, guess4]


def check_correct_locations(player_guess_list, computer_choice_list):
    correct_locations = 0
    if player_guess_list[0] == computer_choice_list[0]:
        correct_locations += 1
    if player_guess_list[1] == computer_choice_list[1]:
        correct_locations += 1
    if player_guess_list[2] == computer_choice_list[2]:
        correct_locations += 1
    if player_guess_list[3] == computer_choice_list[3]:
        correct_locations += 1
    return correct_locations


def check_correct_numbers(player_guess_list, computer_choice_list):
    correct_numbers = 0
    # sort the lists in order
    player_guess_list.sort()
    computer_choice_list.sort()
    # check if the player list contains elements of the computer list
    for player_num in player_guess_list:
        for computer_num in computer_choice_list:
            if player_num == computer_num:
                correct_numbers += 1
    return correct_numbers


def check_game_condition(correct_locations, correct_numbers, name):
    if correct_locations == 4:
        print(
            name
            + ", you have guessed all the numbers and locations correctly. You win!"
        )
        quit()
    elif correct_locations > 0:
        print(
            name
            + ", you have guessed "
            + str(correct_locations)
            + " locations and "
            + str(correct_numbers)
            + " numbers correctly."
        )
    elif correct_locations == 0 and correct_numbers > 0:
        print(
            name
            + ", you have guessed "
            + str(correct_numbers)
            + ", but not in the correct locations."
        )
    elif correct_locations == 0 and correct_numbers == 0:
        print(name + ", you have guessed incorrectly.")


main()
