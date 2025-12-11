"""HTML to clean text extraction."""

import re
from typing import Optional

from bs4 import BeautifulSoup


class TextExtractor:
    """Extract clean text from HTML pages."""

    # Tags to completely remove
    REMOVE_TAGS = {
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "meta",
        "noscript",
        "iframe",
        "svg",
    }

    # Content container selectors to prefer
    CONTENT_SELECTORS = [
        ".docusaurus-page",
        ".markdown",
        "article",
        "main",
        ".content",
        ".post-content",
    ]

    @staticmethod
    def _clean_text(text: str) -> str:
        """Normalize whitespace in text."""
        # Replace multiple spaces/newlines with single space
        text = re.sub(r"\s+", " ", text)
        # Remove control characters except newlines in code blocks
        text = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", text)
        return text.strip()

    @staticmethod
    def _extract_text_from_element(element) -> str:
        """Recursively extract text from an HTML element."""
        text_parts = []

        for child in element.children:
            if isinstance(child, str):
                text_parts.append(child)
            else:
                # Skip removed tags
                if child.name in TextExtractor.REMOVE_TAGS:
                    continue

                # Handle code blocks specially (preserve formatting)
                if child.name in ["code", "pre"]:
                    text_parts.append(child.get_text())
                # Handle headers
                elif child.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                    text_parts.append(f"\n{child.get_text()}\n")
                # Handle lists
                elif child.name in ["ul", "ol"]:
                    for li in child.find_all("li", recursive=False):
                        text_parts.append(f"- {li.get_text()}\n")
                # Handle paragraphs
                elif child.name == "p":
                    text_parts.append(f"{child.get_text()}\n")
                else:
                    # Recursively process
                    text_parts.append(TextExtractor._extract_text_from_element(child))

        return "".join(text_parts)

    @classmethod
    def extract_text(cls, html: str) -> tuple[str, str]:
        """Extract clean text from HTML.

        Returns:
            Tuple of (clean_text, extraction_method)
        """
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Remove unwanted tags
            for tag in soup.find_all(cls.REMOVE_TAGS):
                tag.decompose()

            # Try to find content container
            content = None
            for selector in cls.CONTENT_SELECTORS:
                content = soup.select_one(selector)
                if content:
                    break

            # Fallback to body or entire document
            if not content:
                content = soup.find("body")
            if not content:
                content = soup

            # Extract text
            text = cls._extract_text_from_element(content)

            # Clean up whitespace
            text = cls._clean_text(text)

            return text, "semantic_extraction"

        except Exception as e:
            # Fallback to raw text
            try:
                soup = BeautifulSoup(html, "html.parser")
                # Remove script and style
                for script in soup(["script", "style"]):
                    script.decompose()

                text = soup.get_text()
                text = cls._clean_text(text)
                return text, "fallback_html"
            except Exception:
                # Last resort: regex-based cleaning
                text = re.sub("<[^<]+?>", "", html)
                text = cls._clean_text(text)
                return text, "fallback_raw"
