#!/usr/bin/python3
"""console interpreter"""
import cmd
import re
from shlex import split

import models
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.review import Review

CLASSES = [
    "BaseModel",
    "User",
    "City",
    "Place",
    "State",
    "Amenity",
    "Review"
]


def parse(arg):
    """
    Parses a string argument based on the presence of curly braces
    and brackets.
    Args:
        arg (str): The string argument to be parsed.
    Returns:
        list: The parsed argument list.
    Example Usage:
        parse("User")
        This code will parse the string "User" and return a list
        containing the single element ["User"].
    """
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


def check_args(args):
    """
    Parse the given string argument and check if it meets certain
    conditions.

    Args:
        args (str): The string argument to be parsed.

    Returns:
        list: The parsed argument list if it passes the checks.

    Raises:
        None

    Example:
        >>> check_args("User")
        ["User"]

    """
    arg_list = parse(args)

    if len(arg_list) == 0:
        print("** class name missing **")
    elif arg_list[0] not in CLASSES:
        print("** class doesn't exist **")
    else:
        return arg_list


class HBNBCommand(cmd.Cmd):
    """
    The `HBNBCommand` class is a console interpreter that provides
    a command-line interface for interacting with a database.
    It allows the user to perform various operations such as creating,
    showing, updating, and deleting instances of different classes.

    Example Usage:
        command = HBNBCommand()
        command.do_create("User")
        # Output: <new instance id>

        command.do_show("User 123")
        # Output: <instance details>

        command.do_all("User")
        # Output: [<instance 1 details>, <instance 2 details>, ...]

        command.do_update("User 123 name John")
        # Output: <updated instance details>

        command.do_destroy("User 123")
        # Output: None

        command.do_count("User")
        # Output: <number of instances>

    Methods:
        - default(arg): Handles the default behavior when an
        unknown command is entered.
        - do_EOF(argv): Handles the end-of-file command.
        - do_quit(argv): Handles the quit command.
        - do_create(argv): Creates a new instance of a class
        and prints its ID.
        - do_show(argv): Shows the details of a specific instance.
        - do_all(argv): Lists all instances of a specific class.
        - do_destroy(argv): Deletes a specific instance.
        - do_update(argv): Updates the attributes of a specific
        instance.
        - do_count(arg): Counts the number of instances of a
        specific class.

    Fields:
        - CLASSES: A list of class names.
        - action_map: A dictionary mapping command names to their
        corresponding methods.
    """
    prompt = "(hbnb) "
    storage = models.storage

    def emptyline(self):
        """
        Handle behavior when the user enters an empty line in the
        console.

        Inputs:
        - None

        Flow:
        - The method does not take any inputs.
        - It simply passes and does nothing.

        Outputs:
        - None
        """
        pass

    def default(self, arg):
        """default function"""
        action_map = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
            "create": self.do_create
        }

        match = re.search(r"\.", arg)
        if match:
            arg1 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg1[1])
            if match:
                command = [arg1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in action_map:
                    call = "{} {}".format(arg1[0], command[1])
                    return action_map[command[0]](call)

        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_EOF(self, argv):
        """do_EOF function"""
        print("")
        return True

    def do_quit(self, argv):
        """so_qiut function"""
        return True

    def do_create(self, argv):
        """do_create function"""
        args = check_args(argv)
        if args:
            print(eval(args[0])().id)
            self.storage.save()

    def do_show(self, argv):
        """do_show function"""
        args = check_args(argv)
        if args:
            if len(args) != 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in self.storage.all():
                    print("** no instance found **")
                else:
                    print(self.storage.all()[key])

    def do_all(self, argv):
        """do_all function"""
        arg_list = split(argv)
        objects = self.storage.all().values()
        if not arg_list:
            print([str(obj) for obj in objects])
        else:
            if arg_list[0] not in CLASSES:
                print("** class doesn't exist **")
            else:
                print([str(obj) for obj in objects
                       if arg_list[0] in str(obj)])

    def do_destroy(self, argv):
        """do_destroy function"""
        arg_list = check_args(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(*arg_list)
                if key in self.storage.all():
                    del self.storage.all()[key]
                    self.storage.save()
                else:
                    print("** no instance found **")

    def do_update(self, argv):
        """do_update function"""
        arg_list = check_args(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                instance_id = "{}.{}".format(arg_list[0], arg_list[1])
                if instance_id in self.storage.all():
                    if len(arg_list) == 2:
                        print("** attribute name missing **")
                    elif len(arg_list) == 3:
                        print("** value missing **")
                    else:
                        obj = self.storage.all()[instance_id]
                        if arg_list[2] in type(obj).__dict__:
                            v_type = type(obj.__class__.__dict__[arg_list[2]])
                            setattr(obj, arg_list[2], v_type(arg_list[3]))
                        else:
                            setattr(obj, arg_list[2], arg_list[3])
                else:
                    print("** no instance found **")

            self.storage.save()

    def do_count(self, arg):
        """do_count function"""
        arg1 = parse(arg)
        count = 0
        for obj in models.storage.all().values():
            if arg1[0] == type(obj).__name__:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
