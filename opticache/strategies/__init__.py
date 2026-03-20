from .base import EvictionStrategy
from .lfu import LFUStrategy
from .lru import LRUStrategy
from .fifo import FIFOStrategy
from .fifo_fast_delete import FIFOStrategyFastDelete
from .mru import MRUStrategy
from .sieve import SIEVEStrategy
from .random import RandomStrategy

__all__ = ['EvictionStrategy', 'LFUStrategy',
           'LRUStrategy', 'FIFOStrategy',
           'FIFOStrategyFastDelete', 'MRUStrategy',
           'SIEVEStrategy', 'RandomStrategy']
