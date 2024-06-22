# -*- coding: utf-8 -*-
# ########################################################################                          
# Program: Luminal
# Author: Jason Drawdy
# Version: 1.0.0
# Date: 03/16/23
# #########################################################################
# Description:
# This module allows customized logging of all i/o throughout Luminal.
# #########################################################################
from utils.colors import Colors
from dataclasses import dataclass
from datetime import datetime

#TODO add appending to a file

class Logger(object):
    """Logging class with a high degree of customization."""
    @dataclass(frozen=True)
    class Verbosity():
        """Encapsulates the varying degrees of logging output detail."""
        low: int = 0
        default: int = 1
        high: int = 2
        debug: int = 3
        
    def __init__(self: "Logger", module_name: __name__, allow_same_message: bool = False):
        """
        Initializes a custom logger object with the provided parameters.
        
        Parameters
        ----------
        module_name : :class:`str`
            The name of the module calling the logging object.
        allow_same_message : :class:`bool`
            A flag allowing or disallowing the logger to keep print the same message continuously.
        """
        self.module_name = module_name
        self.allow_same_message = allow_same_message
        self._last_messages = []

    def _print(self: "Logger", message: tuple[str, str]) -> None:
        """
        Prints the provided message while also checking if duplicates are allowed or not.

        Parameters
        ----------
        message : :class:`tuple[str, str]`
            A tuple containing the original message and the message to be printed to the console.

        Notes
        ----------
        The original message is used to compare the last printed message and to prevent the logger
        from spamming the console or whichever IO stream has been provided.
        """
        original_data, new_data = message
        if not self.allow_same_message: # pragma: no cover
            if original_data in self._last_messages:
                return
            self._last_messages.append(original_data)
            if len(self._last_messages) > 3: 
                self._last_messages.pop(0)
        print(new_data)

    def info(self: "Logger", message: str, print_output: bool = True) -> None:
        """
        Displays a non-critical information based message to the console.
        
        Parameters
        ----------
        message : :class:`str`
            The message to log to the local system.
        print_output : Optional[:class:`bool`]
            A boolean, ``True`` for printing the message to the console, or ``False`` if not.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        entry = (f"{Colors.Foreground.pink}{timestamp}{Colors.reset} | {Colors.Foreground.darkgrey}INFO{Colors.reset} | {Colors.Foreground.blue}{self.module_name}{Colors.reset} > {message}")
        if print_output: self._print((message, entry))
        return True

    def note(self: "Logger", message: str, print_output: bool = True) -> bool:
        """
        Displays a note-worthy information based message to the console.
        
        Parameters
        ----------
        message : :class:`str`
            The message to log to the local system.
        print_output : Optional[:class:`bool`]
            A boolean, ``True`` for printing the message to the console, or ``False`` if not.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        entry = (f"{Colors.Foreground.pink}{timestamp}{Colors.reset} | {Colors.Foreground.lightgrey}NOTE{Colors.reset} | {Colors.Foreground.blue}{self.module_name}{Colors.reset} > {message}")
        if print_output: self._print((message, entry))
        return True

    def success(self: "Logger", message: str, print_output: bool = True) -> bool:
        """
        Displays a success message to the console.
        
        Parameters
        ----------
        message : :class:`str`
            The message to log to the local system.
        print_output : Optional[:class:`bool`]
            A boolean, ``True`` for printing the message to the console, or ``False`` if not.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        entry = (f"{Colors.Foreground.pink}{timestamp}{Colors.reset} | {Colors.Foreground.green}PASS{Colors.reset} | {Colors.Foreground.blue}{self.module_name}{Colors.reset} > {message}")
        if print_output: self._print((message, entry))
        return True

    def warning(self: "Logger", message: str, print_output: bool = True) -> bool:
        """
        Displays a warning message to the console.
        
        Parameters
        ----------
        message : :class:`str`
            The message to log to the local system.
        print_output : Optional[:class:`bool`]
            A boolean, ``True`` for printing the message to the console, or ``False`` if not.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        entry = (f"{Colors.Foreground.pink}{timestamp}{Colors.reset} | {Colors.Foreground.yellow}WARN{Colors.reset} | {Colors.Foreground.blue}{self.module_name}{Colors.reset} > {message}")
        if print_output: self._print((message, entry))
        return True

    def error(self: "Logger", message: str, print_output: bool = True) -> bool:
        """
        Displays an error based message to the console.
        
        Parameters
        ----------
        message : :class:`str`
            The message to log to the local system.
        print_output : Optional[:class:`bool`]
            A boolean, ``True`` for printing the message to the console, or ``False`` if not.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        entry = (f"{Colors.Foreground.pink}{timestamp}{Colors.reset} | {Colors.Foreground.red}FAIL{Colors.reset} | {Colors.Foreground.blue}{self.module_name}{Colors.reset} > {Colors.Foreground.red}{message}{Colors.reset}")
        if print_output: self._print((message, entry))
        return True

    def private(self: "Logger", message: str, print_output: bool = True) -> bool:
        """
        Displays a private based message to the console.
        
        Parameters
        ----------
        message : :class:`str`
            The message to log to the local system.
        print_output : Optional[:class:`bool`]
            A boolean, ``True`` for printing the message to the console, or ``False`` if not.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        entry = (f"{Colors.Foreground.pink}{timestamp}{Colors.reset} | {Colors.Foreground.orange}{Colors.bold}PRIV{Colors.reset} | {Colors.Foreground.blue}{Colors.bold}{self.module_name}{Colors.reset} > {Colors.Foreground.orange}{message}{Colors.reset}")
        if print_output: self._print((message, entry))
        return True

    def debug(self: "Logger", message: str, print_output: bool = True) -> bool:
        """
        Displays a debug based message to the console.
        
        Parameters
        ----------
        message : :class:`str`
            The message to log to the local system.
        print_output : Optional[:class:`bool`]
            A boolean, ``True`` for printing the message to the console, or ``False`` if not.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        entry = (f"{Colors.Foreground.pink}{timestamp}{Colors.reset} | {Colors.Foreground.pink}{Colors.bold}DEVS{Colors.reset} | {Colors.Foreground.pink}{Colors.bold}{self.module_name}{Colors.reset} > {Colors.Foreground.pink}{message}{Colors.reset}")
        if print_output: self._print((message, entry))
        return True