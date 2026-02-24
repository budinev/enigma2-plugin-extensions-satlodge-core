# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor

# Questa funzione serve solo a far sì che Enigma2 "veda" il plugin
# ma non aggiungiamo nessuna icona nei menu (dove = [])
def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="SatLodgeCore",
            description="Core Library for SatLodge Plugins",
            where=[],  # Lasciandolo vuoto, non appare nei menu
            fnc=None
        )
    ]
