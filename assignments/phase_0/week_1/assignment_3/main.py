import logging
from crawler import Crawler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def crawl(
    url: str,
    strategy: str = "BFS",
    max_depth: int = 2,
    max_pages: int = 50,
    include_external: bool = False,
):
    """
    Hàm crawl toàn bộ URL từ một trang web bắt đầu (entrypoint).

    Args:
        url:              URL trang bắt đầu.
        strategy:         "BFS" (queue) hoặc "DFS" (stack).
        max_depth:        Độ sâu tối đa tính từ trang gốc.
        max_pages:        Số trang tối đa được crawl.
        include_external: True → crawl cả link ngoài domain.

    Returns:
        CrawlResult với .visited (list URL thành công)
                    và .failed  (list URL thất bại).
    """
    crawler = Crawler(
        strategy=strategy,
        max_depth=max_depth,
        max_pages=max_pages,
        include_external=include_external,
    )
    return crawler.crawl(url)


if __name__ == "__main__":
    TARGET_URL = "https://books.toscrape.com"   

    print("=" * 60)
    print(f"{'BFS':^60}")
    print("=" * 60)
    result_bfs = crawl(TARGET_URL, strategy="BFS", max_depth=1, max_pages=10)
    print(f"\n✅ Visited ({result_bfs.total_visited}):")
    for u in result_bfs.visited:
        print(f"   {u}")
    if result_bfs.failed:
        print(f"\n❌ Failed ({result_bfs.total_failed}):")
        for u in result_bfs.failed:
            print(f"   {u}")

    print()
    print("=" * 60)
    print(f"{'DFS':^60}")
    print("=" * 60)
    result_dfs = crawl(TARGET_URL, strategy="DFS", max_depth=1, max_pages=10)
    print(f"\n✅ Visited ({result_dfs.total_visited}):")
    for u in result_dfs.visited:
        print(f"   {u}")