"""Text chunking into semantic units."""

import hashlib
import re
from typing import List

from src.models import Chunk


class TextChunker:
    """Split text into semantic chunks with metadata."""

    MAX_CHUNK_SIZE = 8192  # Max characters per chunk
    MAX_TOKENS = 512  # Max tokens per chunk (conservative estimate)
    TOKENS_PER_WORD = 1.3  # OpenAI tokenization estimate

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate token count for text."""
        word_count = len(text.split())
        return int(word_count * TextChunker.TOKENS_PER_WORD)

    @staticmethod
    def compute_chunk_id(text: str) -> str:
        """Compute SHA256 hash of normalized text for deduplication."""
        normalized = re.sub(r"\s+", " ", text.lower().strip())
        return hashlib.sha256(normalized.encode()).hexdigest()

    @classmethod
    def chunk_text(
        cls, text: str, url: str, section_title: str = None
    ) -> List[Chunk]:
        """Split text into semantic chunks.

        Args:
            text: Clean extracted text
            url: Source page URL
            section_title: Optional section/heading title

        Returns:
            List of Chunk objects with metadata
        """
        chunks = []

        # Remove empty text
        text = text.strip()
        if not text:
            return chunks

        # Split by paragraphs (double newline) first
        paragraphs = re.split(r"\n\n+", text)

        chunk_index = 0
        current_chunk_text = ""
        current_chunk_section = section_title

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # If adding this paragraph would exceed max size, save current chunk
            potential_text = (
                f"{current_chunk_text}\n\n{paragraph}"
                if current_chunk_text
                else paragraph
            )

            if len(potential_text) > cls.MAX_CHUNK_SIZE:
                # Save current chunk if not empty
                if current_chunk_text:
                    token_count = cls.estimate_tokens(current_chunk_text)
                    # Only create chunk if text is not empty/whitespace and within token limit
                    if token_count > 0 and token_count <= cls.MAX_TOKENS:
                        chunk_id = cls.compute_chunk_id(current_chunk_text)
                        chunks.append(
                            Chunk(
                                chunk_id=chunk_id,
                                url=url,
                                text=current_chunk_text,
                                section_title=current_chunk_section,
                                chunk_index=chunk_index,
                                token_count=token_count,
                                extraction_method="semantic_paragraph",
                            )
                        )
                        chunk_index += 1

                # Start new chunk with paragraph (split if still too large)
                if len(paragraph) > cls.MAX_CHUNK_SIZE:
                    # Split large paragraph by sentences
                    sentences = re.split(r"(?<=[.!?])\s+", paragraph)
                    current_chunk_text = ""

                    for sentence in sentences:
                        if len(current_chunk_text) + len(sentence) > cls.MAX_CHUNK_SIZE:
                            if current_chunk_text:
                                token_count = cls.estimate_tokens(current_chunk_text)
                                if token_count > 0 and token_count <= cls.MAX_TOKENS:
                                    chunk_id = cls.compute_chunk_id(current_chunk_text)
                                    chunks.append(
                                        Chunk(
                                            chunk_id=chunk_id,
                                            url=url,
                                            text=current_chunk_text,
                                            section_title=current_chunk_section,
                                            chunk_index=chunk_index,
                                            token_count=token_count,
                                            extraction_method="semantic_paragraph",
                                        )
                                    )
                                    chunk_index += 1
                            current_chunk_text = sentence
                        else:
                            current_chunk_text = (
                                f"{current_chunk_text} {sentence}"
                                if current_chunk_text
                                else sentence
                            )

                    if current_chunk_text:
                        token_count = cls.estimate_tokens(current_chunk_text)
                        if token_count > 0 and token_count <= cls.MAX_TOKENS:
                            chunk_id = cls.compute_chunk_id(current_chunk_text)
                            chunks.append(
                                Chunk(
                                    chunk_id=chunk_id,
                                    url=url,
                                    text=current_chunk_text,
                                    section_title=current_chunk_section,
                                    chunk_index=chunk_index,
                                    token_count=token_count,
                                    extraction_method="semantic_paragraph",
                                )
                            )
                            chunk_index += 1
                        current_chunk_text = ""
                else:
                    current_chunk_text = paragraph
            else:
                current_chunk_text = potential_text

        # Save final chunk
        if current_chunk_text:
            token_count = cls.estimate_tokens(current_chunk_text)
            if token_count > 0 and token_count <= cls.MAX_TOKENS:
                chunk_id = cls.compute_chunk_id(current_chunk_text)
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        url=url,
                        text=current_chunk_text,
                        section_title=current_chunk_section,
                        chunk_index=chunk_index,
                        token_count=token_count,
                        extraction_method="semantic_paragraph",
                    )
                )

        return chunks
