from urllib.parse import urlparse, urljoin, urldefrag
from typing import Set, List
from bs4 import BeautifulSoup


def get_domain(url: str) -> str:
    """Trả về domain (scheme + netloc) của URL."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def is_same_domain(url: str, base_domain: str) -> bool:
    """Kiểm tra url có cùng domain với base_domain không."""
    return get_domain(url) == base_domain


def normalize_url(url: str) -> str:
    """
    Chuẩn hoá URL:
    - Bỏ fragment (#section)
    - Bỏ trailing slash cuối (trừ root)
    """
    url, _ = urldefrag(url)         # bỏ #fragment
    if url.endswith("/") and urlparse(url).path != "/":
        url = url.rstrip("/")
    return url


def extract_links(html: str, base_url: str) -> List[str]:
    """
    Parse HTML và trả về danh sách URL tuyệt đối
    từ tất cả thẻ <a href="...">.
    """
    soup = BeautifulSoup(html, "html.parser")
    links: List[str] = []

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()

        if href.startswith(("javascript:", "mailto:", "tel:", "#")):
            continue

        absolute = urljoin(base_url, href)
        normalized = normalize_url(absolute)

        if urlparse(normalized).scheme in ("http", "https"):
            links.append(normalized)

    return links


def is_valid_url(url: str) -> bool:
    """Kiểm tra URL có hợp lệ (có scheme và netloc) không."""
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)