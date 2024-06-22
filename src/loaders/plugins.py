from luminal.managers import Loader
from settings import Settings
import asyncio

class Plugins:
    def __init__(self: "Plugins") -> None:
        """Create a new program to hold a photon manager and photon paths."""
        self.photons = Settings.CONFIG['plugins_directory']
        self.loader = Loader(logging=True)

    async def watch(self):
        """Spawns a sentinel, loads photons, and watches for changes to reload."""
        await self.loader.watch_photons(self.photons)

    async def stop(self):
        """Stops the spawned sentinel and begin unloading all photons."""
        await self.loader.stop_watching_photons(halt_threads=True)