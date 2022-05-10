"""mvc_exceptions.py: exceptions for inventory items management app"""

__author__      = "Silvia Nittel"
__copyright__   = "Copyright 2022, SIE508, University of Maine"
__credits__     = ["Silvia Nittel"]


class ItemAlreadyStored(Exception):
    pass

class ItemNotStored(Exception):
    pass