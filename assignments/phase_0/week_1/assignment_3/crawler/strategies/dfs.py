from typing import Tuple
from .base import BaseCrawlStrategy


class DFSStrategy(BaseCrawlStrategy):

    def __init__(self):
        super().__init__()
        self._frontier = []

    def add(self, item: Tuple[str, int]) -> None:
        self._frontier.append(item)  

    def next(self) -> Tuple[str, int]:
        return self._frontier.pop()  