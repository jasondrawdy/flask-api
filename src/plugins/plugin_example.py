# -*- coding: utf-8 -*-
# ########################################################################                          
# Program: Luminal
# Author: Jason Drawdy
# Version: 1.0.0
# Date: 07/07/23
# #########################################################################
# Description:
# Basic photon which shows the creation structure with no input or output.
# #########################################################################
from luminal.interfaces.photon import IPhoton

# φ #
class PluginExample(IPhoton): # pragma: no cover
    """A photon developed for unit testing and contains a finalizer, but no output."""
    def __init__(self: "PluginExample"):
        print("Hello, World!")
        
    async def finalize(self: "PluginExample") -> bool: 
        print("This allows for thread cleanup and whatever else is required.")