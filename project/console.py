from typing import List

import project.commands
from project.commands import ExecutionException

__all__ = ["run_app", "InputException"]

command_names = ["get_graph_info", "create_two_cycles", "save_to_dot", "quit"]

command_dict = {
    command_names[0]: project.commands.get_graph_info,
    command_names[1]: project.commands.create_two_cycles,
    command_names[2]: project.commands.save_to_dot,
    command_names[3]: project.commands.quit_app,
}


class InputException(Exception):
    """
    Exception raised for errors in the input.

    Attributes
    ----------
        message: str
            Explanation of the error
    """

    def __init__(self, message):
        self.message = message


def print_options():
    print(
        "\n(1) get_graph_info [graph_name] : Get info about graph - number of nodes, number of edges, labels;"
    )
    print(
        "(2) create_two_cycles [graph_name] [nodes_number_first] [nodes_number_second] [label_1] [label_2]: Create "
        "graph with two cycles;"
    )
    print(
        "(3) save_to_dot [graph_name] [folder_path]: Save graph with graph_name to dot file in folder_path;"
    )
    print("(4) quit : Quit application.")


def check_command(input_split: List[str]) -> None:
    """
    Checks whether list of string matches to command of the application

    Parameters
    ----------
    input_split: List[str]
        List of strings to check

    Returns
    -------
    None

    Raises
    ------
    InputException
        If there is no command with such name, or there is an error in the arguments

    """
    current_command_name = input_split[0]

    if current_command_name not in command_names:
        raise InputException("Command not found!")

    if current_command_name == command_names[0]:
        if len(input_split) != 2:
            raise InputException("Error in argument's number!")

    elif current_command_name == command_names[1]:
        if len(input_split) != 6:
            raise InputException("Error in argument's number!")

        if not input_split[2].isnumeric() or not input_split[3].isnumeric():
            raise InputException("Wrong types of arguments!")

    elif current_command_name == command_names[2]:
        if len(input_split) != 3:
            raise InputException("Error in argument's number!")

    elif current_command_name == command_names[3]:
        if len(input_split) != 1:
            raise InputException("Error in argument's number!")


def run_app() -> None:
    """
    Runs a console application

    Returns
    -------
    None
    """
    print_options()
    while True:

        input_text = input(">>> ")
        input_split = input_text.split(sep=" ")

        try:
            check_command(input_split)
        except InputException as ie:
            print(ie.message + " Try again!")
            continue

        name = input_split[0]

        try:
            command_dict[name](*input_split[1:])
        except ExecutionException as ee:
            print(ee.message + " Try again!")
            continue
