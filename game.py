# order of precedence
from termcolor import colored
import requests
from art import *
import cowsay


def main():
    computer_choice_list = []
    player_guess = []
    player_guess_cumulative = []
    player_feedback_cumulative = []
    attempts_left = 10
    attempts_made = 0
    greet_player()
    name = get_name()
    while attempts_left > 0:
        if computer_choice_list == []:
            # string version of api response representing the computer player number choices
            computer_numbers = choose_computer_player_numbers()
            # turn the string version of the api response into a list of strings and save to computer_choice_list variable
            computer_choice_list = make_computer_choice_list(computer_numbers)
        # list of strings from user representing their four guesses in order
        player_guess = make_player_guess_list(
            name, player_guess_cumulative, player_feedback_cumulative, attempts_left
        )
        attempts_made += 1

        # checks the player guesses against the computer player choices and returns the number of correct locations
        correct_locations = check_correct_locations(player_guess, computer_choice_list)
        # check the amount of numbers that were guessed correctly
        correct_numbers = check_correct_numbers(player_guess, computer_choice_list)
        # check whether the game should continue and print appropriate message
        game_condition = check_game_condition(correct_locations, correct_numbers, name)

        # make a dictionary of the guess and the feedback
        player_guess_cumulative.append(player_guess)
        player_feedback_cumulative.append(game_condition)

        # reduce the number of attempts until 10 attempts are made
        attempts_left -= 1
    print("\n")
    cowsay.tux(
        "You failed to guess correctly within 10 attempts. Game Over. Play again.",
    )
    print("\n")


def greet_player():
    tprint("Mastermind")

    cowsay.tux(
        "Welcome to Mastermind. Can you guess the four\nnumbers I have picked and their correct order?\nYou have ten chances to guess correctly and\nbecome a Mastermind.",
    ),


def get_name():
    not_valid = True
    name = ""
    while not_valid:
        name = input(colored("\nWhat is your first name? ", "blue"))
        if name.replace(" ", "").isalpha():
            name = name.title()
            print(
                colored(
                    "\nHello, " + name + ". Please make your guesses below.", "blue"
                )
            )
            not_valid = False
        else:
            print("You entered an invalid name. Try again.")
    return name


def choose_computer_player_numbers():
    try:
        api_url = "https://www.random.org/integers?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
        response = requests.get(api_url)
        if response.status_code == 200:
            # string representation of the api response
            return response.text
        else:
            print(
                colored(
                    "The server responded with status code: "
                    + response.status_code
                    + " please try again later.",
                    "red",
                )
            )
            quit()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def make_computer_choice_list(computer_player_numbers):
    # a list of strings representing the numbers chosen by the computer player (from api)
    computer_choice_list = []
    # find the digits in the string representation of the api response and append to list
    for char in computer_player_numbers:
        if char.isdigit():
            computer_choice_list.append(char)
        else:
            continue
    return computer_choice_list


def make_player_guess_list(
    name, player_guess_cumulative, player_feedback_cumulative, attempts
):
    print("---------------------------------------------")
    if attempts > 1:
        print(colored("\nYou have " + str(attempts) + " attempts remaining", "blue"))
    elif attempts == 1:
        print(colored("\nYou have " + str(attempts) + " attempt remaining", "blue"))
    else:
        print(colored("Game over", "blue"))
        quit()
    if player_guess_cumulative != []:
        print(colored(name + ", your previous guesses were:\n", "blue"))
        for i in range(0, len(player_guess_cumulative)):
            print(
                "Guess: "
                + str(player_guess_cumulative[i])
                + "\nFeedback: "
                + str(player_feedback_cumulative[i])
                + "\n",
            )

    guess1 = ""
    guess2 = ""
    guess3 = ""
    guess4 = ""

    while guess1 == "":
        guess1 = input(colored("Please input a number between 0-7: ", "blue"))
        if guess1.isnumeric() and int(guess1) >= 0 and int(guess1) <= 7:
            break
        else:
            print("Invalid input. Try again. ")
            guess1 = ""
            continue
    while guess2 == "":
        guess2 = input(colored("Please input a second number between 0-7: ", "blue"))
        if guess2.isnumeric() and int(guess2) >= 0 and int(guess2) <= 7:
            break
        else:
            print("Invalid input. Try again. ")
            guess2 = ""
            continue
    while guess3 == "":
        guess3 = input(colored("Please input a third number between 0-7: ", "blue"))
        if guess3.isnumeric() and int(guess3) >= 0 and int(guess3) <= 7:
            break
        else:
            print("Invalid input. Try again. ")
            guess3 = ""
            continue
    while guess4 == "":
        guess4 = input(colored("Please input a fourth number between 0-7: ", "blue"))
        if guess4.isnumeric() and int(guess4) >= 0 and int(guess4) <= 7:
            break
        else:
            print("Invalid input. Try again. ")
            guess4 = ""
            continue
    guess_list = [guess1, guess2, guess3, guess4]
    return guess_list


def check_correct_locations(player_list, computer_list):
    correct_locations = 0
    if player_list and computer_list:
        if player_list[0] == computer_list[0]:
            correct_locations += 1
        if player_list[1] == computer_list[1]:
            correct_locations += 1
        if player_list[2] == computer_list[2]:
            correct_locations += 1
        if player_list[3] == computer_list[3]:
            correct_locations += 1
    else:
        print("there was a problem with the player numbers or the computer numbers")
    return correct_locations


def check_correct_numbers(player_list, computer_list):
    computer_list_copy = computer_list.copy()
    correct_nums = 0
    for i in range(0, len(player_list)):
        if player_list[i] in computer_list_copy:
            index_of_match = computer_list_copy.index(player_list[i])
            computer_list_copy.pop(index_of_match)
            correct_nums += 1
    return correct_nums


def check_game_condition(correct_locations, correct_numbers, name):
    if correct_locations == 4:
        print(
            colored(
                name
                + ", you have guessed all the numbers and locations correctly. You are a Mastermind!\n",
                "green",
            )
        )
        quit()

    elif correct_locations == 1 and correct_numbers == 1:
        feedback = f"{str(correct_locations)} correct location and {str(correct_numbers)} correct number"
        print(
            colored(
                str(correct_locations)
                + " correct location and "
                + str(correct_numbers)
                + " correct number",
                "green",
            )
        )
        return feedback
    elif correct_locations == 1 and correct_numbers > 1:
        feedback = f"{str(correct_locations)} correct location and {str(correct_numbers)} correct numbers"
        print(
            colored(
                str(correct_locations)
                + " correct location and "
                + str(correct_numbers)
                + " correct numbers",
                "green",
            )
        )
        return feedback
    elif correct_locations > 1 and correct_numbers == 1:
        feedback = f"{str(correct_locations)} correct locations and {str(correct_numbers)} correct number"
        print(
            colored(
                str(correct_locations)
                + " correct locations and "
                + str(correct_numbers)
                + " correct number",
                "green",
            )
        )
        return feedback
    elif correct_locations > 1 and correct_numbers > 1:
        feedback = f"{str(correct_locations)} correct locations and {str(correct_numbers)} correct numbers"
        print(
            colored(
                str(correct_locations)
                + " correct locations and "
                + str(correct_numbers)
                + " correct numbers",
                "green",
            )
        )
        return feedback
    elif correct_locations == 0 and correct_numbers > 1:
        feedback = f"{str(correct_locations)} correct locations and {str(correct_numbers)} correct numbers"
        print(
            colored(
                str(correct_locations)
                + " correct locations and "
                + str(correct_numbers)
                + " correct numbers",
                "green",
            )
        )
        return feedback
    elif correct_locations > 1 and correct_numbers == 0:
        feedback = f"{str(correct_locations)} correct locations and {str(correct_numbers)} correct numbers"
        print(
            colored(
                str(correct_locations)
                + " correct locations and "
                + str(correct_numbers)
                + " correct numbers",
                "green",
            )
        )
        return feedback
    elif correct_locations == 1 and correct_numbers == 0:
        feedback = f"{str(correct_locations)} correct location and {str(correct_numbers)} correct numbers"
        print(
            colored(
                str(correct_locations)
                + " correct location and "
                + str(correct_numbers)
                + " correct numbers",
                "green",
            )
        )
        return feedback
    elif correct_locations == 0 and correct_numbers == 1:
        feedback = f"{str(correct_locations)} correct locations and {str(correct_numbers)} correct number"
        print(
            colored(
                str(correct_locations)
                + " correct locations and "
                + str(correct_numbers)
                + " correct number",
                "green",
            )
        )
        return feedback
    elif correct_locations == 0 and correct_numbers == 0:
        feedback = "all incorrect"
        print(colored("all incorrect", "red", attrs=["bold"]))
        return feedback


main()
