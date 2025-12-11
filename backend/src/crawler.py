"""URL discovery and page crawling for Docosaurus books."""

import asyncio
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree as ET

import httpx
from bs4 import BeautifulSoup

from src.models import Page


class DocosaurusCrawler:
    """Crawl Docosaurus book URLs and fetch page content."""

    def __init__(self, root_url: str, timeout: int = 30):
        """Initialize crawler."""
        self.root_url = root_url.rstrip("/")
        self.timeout = timeout
        self.session: Optional[httpx.Client] = None
        self.discovered_urls: Set[str] = set()

    async def _fetch_sitemap(self) -> Optional[str]:
        """Fetch sitemap.xml from the Docosaurus site."""
        sitemap_url = f"{self.root_url}/sitemap.xml"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(sitemap_url)
                if response.status_code == 200:
                    return response.text
        except Exception:
            pass
        return None

    def _parse_sitemap(self, sitemap_xml: str) -> List[str]:
        """Parse sitemap.xml and extract URLs."""
        urls = []
        try:
            root = ET.fromstring(sitemap_xml)
            namespace = {
                "ns": "http://www.sitemaps.org/schemas/sitemap/0.9"
            }

            for loc in root.findall(".//ns:loc", namespace):
                if loc.text:
                    url = loc.text.strip()
                    # Filter out asset URLs (CSS, JS, images)
                    if not any(
                        ext in url.lower()
                        for ext in [".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".ico"]
                    ):
                        urls.append(url)

            return urls
        except Exception:
            return []

    async def _discover_urls_from_html(self, html: str) -> List[str]:
        """Fallback: discover URLs from HTML by parsing links."""
        urls = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if href.startswith("/"):
                    url = urljoin(self.root_url, href)
                elif href.startswith(self.root_url):
                    url = href
                else:
                    continue

                # Filter out asset URLs and anchors
                if any(
                    ext in url.lower()
                    for ext in [".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".ico", "#"]
                ):
                    continue

                url = url.split("#")[0]  # Remove anchors
                if url not in self.discovered_urls:
                    urls.append(url)
                    self.discovered_urls.add(url)

        except Exception:
            pass

        return urls

    async def discover_urls(self, max_pages: Optional[int] = None) -> List[str]:
        """Discover all pages URLs from the book."""
        # Try sitemap first
        sitemap_xml = await self._fetch_sitemap()
        if sitemap_xml:
            urls = self._parse_sitemap(sitemap_xml)
            self.discovered_urls.update(urls)
        else:
            # Fallback: crawl root page and extract links
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(self.root_url)
                    if response.status_code == 200:
                        root_urls = await self._discover_urls_from_html(
                            response.text
                        )
                        self.discovered_urls.update(root_urls)
            except Exception:
                pass

        urls = sorted(list(self.discovered_urls))
        if max_pages:
            urls = urls[:max_pages]

        return urls

    async def fetch_page(self, url: str) -> Page:
        """Fetch and parse a single page."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)

                # Extract title
                title = url.split("/")[-1].replace("-", " ").title()
                try:
                    soup = BeautifulSoup(response.text, "html.parser")
                    title_tag = soup.find("title")
                    if title_tag and title_tag.string:
                        title = title_tag.string.strip()
                except Exception:
                    pass

                return Page(
                    url=url,
                    title=title,
                    html_content=response.text,
                    status_code=response.status_code,
                )

        except httpx.TimeoutException:
            return Page(
                url=url,
                title="Unknown",
                html_content="",
                status_code=408,
                fetch_error="Request timeout",
            )
        except httpx.RequestError as e:
            return Page(
                url=url,
                title="Unknown",
                html_content="",
                status_code=0,
                fetch_error=f"Request failed: {str(e)}",
            )
        except Exception as e:
            return Page(
                url=url,
                title="Unknown",
                html_content="",
                status_code=0,
                fetch_error=f"Unexpected error: {str(e)}",
            )

    async def fetch_pages(self, urls: List[str]) -> List[Page]:
        """Fetch multiple pages concurrently."""
        tasks = [self.fetch_page(url) for url in urls]
        pages = await asyncio.gather(*tasks)
        return pages
