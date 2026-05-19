from collections import deque
from typing import Tuple
from .base import BaseCrawlStrategy


class BFSStrategy(BaseCrawlStrategy):

    def __init__(self):
        super().__init__()
        self._frontier = deque()

    def add(self, item: Tuple[str, int]) -> None:
        self._frontier.append(item)  

    def next(self) -> Tuple[str, int]:
        return self._frontier.popleft()  

    def is_empty(self) -> bool:
        return len(self._frontier) == 0

    def __len__(self) -> int:
        return len(self._frontier)