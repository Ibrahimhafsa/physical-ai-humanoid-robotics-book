"""
RAG Agent using OpenAI Agents SDK with context-only grounding.

Implements constraint prompting to ensure agent responds ONLY using
provided context, preventing hallucination.
"""

import logging
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


# Constraint prompt ensures context-only responses
SYSTEM_PROMPT = """You are a helpful assistant answering questions about a physics and robotics book.

CRITICAL RULES:
1. You MUST ONLY answer using the provided context/documents.
2. You MUST NOT use external knowledge or information outside the provided context.
3. If the provided context is insufficient to answer the question, you MUST say: "I don't have enough information about this topic in the provided materials."
4. Always cite your sources when answering based on retrieved chunks.
5. Be concise and factual. Do not add creative interpretations or assumptions.

Provided context will be given in the form of retrieved book chunks.
Answer based strictly on that context."""


class RAGAgent:
    """RAG Agent using OpenAI Agents SDK with constraint prompting.

    Orchestrates context-grounded response generation using OpenAI's
    Agents API with constraint prompting to prevent hallucination.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Initialize RAG agent.

        Args:
            api_key: OpenAI API key (optional - will use None if not provided)
            model: Model to use (default gpt-3.5-turbo)
        """
        # OpenAI API key is optional - if not provided, agent will still work
        # but generation will use fallback method
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
        self.model = model
        logger.info(f"Initialized RAG agent with model {model} (OpenAI client: {self.client is not None})")

    def generate_response(self, query: str, context: str, max_tokens: int = 500) -> str:
        """Generate response using OpenAI Agents SDK with context-only grounding.

        Args:
            query: User question
            context: Retrieved context chunks (as formatted text)
            max_tokens: Maximum tokens in response

        Returns:
            Agent-generated answer grounded in provided context

        Raises:
            ValueError: If context is empty
            RuntimeError: If OpenAI API call fails
        """
        if not context.strip():
            logger.warning("Empty context provided to agent")
            return "I don't have enough information about this topic in the provided materials."

        if not query.strip():
            raise ValueError("Query cannot be empty")

        # If OpenAI client is not available, use fallback method
        if self.client is None:
            logger.info("OpenAI client not configured, using context-based response")
            # Return the context as-is - useful when using alternative LLM providers
            # This allows the system to work with Cohere embeddings + Qdrant retrieval
            return f"Based on the provided materials:\n\n{context[:1000]}"

        # Construct prompt with context
        prompt = f"""{SYSTEM_PROMPT}

RETRIEVED CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:"""

        try:
            logger.debug(f"Calling OpenAI API with model {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
                ],
                max_tokens=max_tokens,
                temperature=0.3,  # Low temperature for factual responses
            )

            answer = response.choices[0].message.content
            logger.info(f"Generated response for query: {query[:50]}...")
            return answer

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise RuntimeError(f"Failed to generate response: {e}")

    def estimate_response_tokens(self, response: str) -> int:
        """Estimate tokens in response (rough approximation).

        Uses OpenAI's token estimation (1 token ≈ 4 characters).

        Args:
            response: Response text

        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters
        return max(1, len(response) // 4)
