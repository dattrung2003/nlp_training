from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CrawlerConfig:
    """Toàn bộ cấu hình của crawler."""

    strategy: str = "BFS"           # "BFS" hoặc "DFS"
    max_depth: int = 2              # Độ sâu tối đa
    max_pages: int = 50             # Số trang tối đa
    include_external: bool = False  # Có crawl domain ngoài không
    request_timeout: int = 10       # Timeout mỗi request (giây)
    headers: Dict[str, str] = field(default_factory=lambda: {
        "User-Agent": (
            "Mozilla/5.0 (compatible; PythonCrawler/1.0)"
        )
    })

    def __post_init__(self):
        if self.strategy not in ("BFS", "DFS"):
            raise ValueError(f"strategy phải là 'BFS' hoặc 'DFS', nhận: {self.strategy!r}")
        if self.max_depth < 0:
            raise ValueError("max_depth phải >= 0")
        if self.max_pages < 1:
            raise ValueError("max_pages phải >= 1")