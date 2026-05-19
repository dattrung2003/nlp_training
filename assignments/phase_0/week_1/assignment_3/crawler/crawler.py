import logging
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from .config import CrawlerConfig
from .utils import (
    get_domain,
    is_same_domain,
    is_valid_url,
    extract_links,
)
from .strategies import BaseCrawlStrategy, BFSStrategy, DFSStrategy

logger = logging.getLogger(__name__)


@dataclass
class CrawlResult:
    """Kết quả sau khi crawl xong."""
    visited: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)

    @property
    def total_visited(self) -> int:
        return len(self.visited)

    @property
    def total_failed(self) -> int:
        return len(self.failed)

    def __str__(self) -> str:
        return (
            f"CrawlResult(visited={self.total_visited}, "
            f"failed={self.total_failed})"
        )


class Crawler:
    """
    Web Crawler hỗ trợ cả BFS và DFS.

    Ví dụ:
        crawler = Crawler(strategy="BFS", max_depth=2, max_pages=30)
        result  = crawler.crawl("https://example.com")
        print(result.visited)
    """

    def __init__(
        self,
        strategy: str = "BFS",
        max_depth: int = 2,
        max_pages: int = 50,
        include_external: bool = False,
    ):
        self._config = CrawlerConfig(
            strategy=strategy,
            max_depth=max_depth,
            max_pages=max_pages,
            include_external=include_external,
        )



    def crawl(self, url: str) -> CrawlResult:
        """
        Crawl toàn bộ URL bắt đầu từ `url`.

        Args:
            url: URL trang bắt đầu (entrypoint).

        Returns:
            CrawlResult chứa danh sách visited và failed.
        """
        if not is_valid_url(url):
            raise ValueError(f"URL không hợp lệ: {url!r}")

        result = CrawlResult()
        visited_set: set[str] = set()
        base_domain = get_domain(url)

        frontier = self._make_strategy()
        frontier.add((url, 0))   # (url, depth)

        logger.info(
            "Bắt đầu crawl | strategy=%s | max_depth=%d | max_pages=%d | url=%s",
            self._config.strategy,
            self._config.max_depth,
            self._config.max_pages,
            url,
        )

        while not frontier.is_empty():
            if len(result.visited) >= self._config.max_pages:
                logger.info("Đạt max_pages=%d, dừng.", self._config.max_pages)
                break

            current_url, depth = frontier.next()

            if current_url in visited_set:
                continue

            visited_set.add(current_url)

            html = self._fetch(current_url, result)
            if html is None:
                continue

            result.visited.append(current_url)
            logger.debug("[depth=%d] ✓ %s", depth, current_url)

            if depth >= self._config.max_depth:
                continue

            for link in extract_links(html, current_url):
                if link in visited_set:
                    continue
                if not self._config.include_external and not is_same_domain(link, base_domain):
                    continue
                frontier.add((link, depth + 1))

        logger.info("Hoàn thành: %s", result)
        return result



    def _make_strategy(self) -> BaseCrawlStrategy:
        """Factory: trả về strategy phù hợp theo config."""
        strategies = {
            "BFS": BFSStrategy,
            "DFS": DFSStrategy,
        }
        return strategies[self._config.strategy]()

    def _fetch(self, url: str, result: CrawlResult) -> Optional[str]:
        """
        Tải nội dung HTML của `url`.

        Returns:
            Nội dung HTML (str) hoặc None nếu thất bại.
        """
        try:
            req = Request(url, headers=self._config.headers)
            with urlopen(req, timeout=self._config.request_timeout) as resp:
                content_type = resp.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    logger.debug("Bỏ qua (không phải HTML): %s", url)
                    return None
                return resp.read().decode("utf-8", errors="replace")

        except HTTPError as e:
            logger.warning("HTTP %d: %s", e.code, url)
        except URLError as e:
            logger.warning("URLError %s: %s", e.reason, url)
        except Exception as e:
            logger.warning("Lỗi không xác định (%s): %s", type(e).__name__, url)

        result.failed.append(url)
        return None