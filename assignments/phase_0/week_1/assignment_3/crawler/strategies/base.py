from abc import ABC, abstractmethod
from typing import Tuple


class BaseCrawlStrategy(ABC):
    """Abstract base class định nghĩa interface cho các chiến lược duyệt."""

    def __init__(self):
        self._frontier = []  

    @abstractmethod
    def add(self, item: Tuple[str, int]) -> None:
        """Thêm (url, depth) vào frontier."""
        pass

    @abstractmethod
    def next(self) -> Tuple[str, int]:
        """Lấy (url, depth) tiếp theo từ frontier."""
        pass

    def is_empty(self) -> bool:
        return len(self._frontier) == 0

    def __len__(self) -> int:
        return len(self._frontier)