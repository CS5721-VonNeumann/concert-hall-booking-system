from abc import ABC, abstractmethod
from enum import Enum

class SeatTypeEnum(Enum):
    REGULAR = 'REGULAR',
    PREMIUM = 'PREMIUM',

class SeatType(ABC):
    """
    Abstract base class for seat types. Enforces the implementation of
    the following methods in subclasses.
    """

    @abstractmethod
    def get_seat_type(self):
        pass

    @abstractmethod
    def get_price(self):
        pass


class RegularSeatType(SeatType):

    def get_seat_type(self):
        return SeatTypeEnum.REGULAR
    
    def get_price(self):
        return 10
    

class PremiumSeatType(SeatType):

    def get_seat_type(self):
        return SeatTypeEnum.PREMIUM
    
    def get_price(self):
        return 20