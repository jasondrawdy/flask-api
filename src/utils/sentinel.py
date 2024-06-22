# -*- coding: utf-8 -*-
# ########################################################################
# Program: Luminal
# Author: Jason Drawdy
# Version: 1.0.0
# Date: 03/16/23
# #########################################################################
# Description:
# This module creates a system file watcher which monitors all modules and
# system files for garbage directories and miscellaneous data. 
# #########################################################################
from utils.generators import TextUtils
from utils.colors import Colors
from utils.logger import Logger
import _thread
import asyncio
import shutil
import sys
import os

class Sentinel(object): # pragma: no cover
    """Sentinel is a system watching mechanism created to dynamically monitor files or collect garbage."""
    def __init__(self: "Sentinel", id: str = TextUtils().generate_id(10)):
        """Initializes a new system watcher which can be used for monitoring files or collecting garbage.
        
        Parameters
        ----------
        id : Optional[:class:`str`]
            The identifier of the sentinel being deployed.
        """
        self.id = id
        self.authorized = False # Flag which tells the sentinel if it is allowed to load modules.
        self.monitoring = False # Flag which tells the sentinel if it should load modules.
        self.log = Logger(__name__) # Logger for passing information to the console and etc.
    
    def _find_garbage(self: "Sentinel", path: str) -> int:
        """Obtains all blacklisted files and directories recursively within a given path.
        
        Parameters
        ----------
        path : :class:`str`
            The directory that the sentinel should monitor for collection.
        """
        garbage_paths = [ "__pycache__", ".DS_Store"]
        count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if file in garbage_paths:
                    try:
                        os.remove(os.path.join(root, file))
                        count += 1
                    except: pass
            for dir in dirs:
                if dir in garbage_paths:
                    try:
                        found = (os.path.join(root, dir))
                        os.rmdir(found)
                        count += 1
                    except: # Try again with shutil to see if it's recursive or it's permissions.
                        try: shutil.rmtree(found)
                        except: pass
        return count
    
    def _check_system(self: "Sentinel") -> None:
        """Gathers all Python based cache files and removes them recursively."""
        garbage = self._find_garbage(sys.path[-1]) if sys.path[-1] == "../" else self._find_garbage(sys.path[0])
        plural = "object" if garbage == 1 else "objects"
        message = f"{Colors.Foreground.cyan}Sentinel {Colors.Foreground.blue}({self.id}){Colors.Foreground.cyan} has removed "
        message += f"{garbage} garbage {plural} from the current workspace.{Colors.reset}"
        if garbage >= 1:
            self.log.note(message, context="debug")

    def _start_resolving(self: "Sentinel", time: int = 1) -> None: # We should always utilize non-blocking method calls when working with dynamic programming.
        """Creates a monitor resolver by utilizing a non-blocking asynchronous system watcher function.
        
        Parameters
        ----------
        time : Optional[:class:`int`]
            How long the thread should wait before continuing to loop.
        """
        asyncio.run(self.watch_system(time))

    def start(self: "Sentinel") -> None: # Starting a resolving thread that runs parallel to the main thread allows for better process control.
        """Starts the sentinel and allows it to monitor as long as `monitoring` and `authorized` is set to `True`."""
        _thread.start_new_thread(self._start_resolving, ())

    async def watch_system(self: "Sentinel", time: int) -> None: #* Can technically be called by itself, however, it wouldn't be multithreaded.
        """``|coro|``

        Initial sentinel loop which allows the sentinel to monitor for artifacts.
        
        Parameters
        ----------
        time : :class:`int`
            How long the thread should wait before continuing to loop.
        """
        self.monitoring = True
        while self.monitoring: # Monitor modules as long as the script is running.
            if self.authorized: # Only monitor modules if the script is available and ready.
                self._check_system() # For now, we're just going to be collecting and disposing of garbage.
                await asyncio.sleep(time)  # Next, sleep the thread so it doesn't consume resources too quickly.