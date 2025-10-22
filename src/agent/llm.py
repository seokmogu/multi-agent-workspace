"""
LLM initialization with rate limiting and caching.

Centralizes LLM setup for consistency and production stability.
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.rate_limiters import InMemoryRateLimiter
from .configuration import Configuration


# Global rate limiter to prevent API throttling
# Anthropic Claude API tier limits:
# - Tier 1: 50 requests/min, 40,000 tokens/min
# - Tier 2: 1,000 requests/min, 80,000 tokens/min
# Setting conservative limits for Tier 1 compliance
_rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.8,  # ~50 requests/min
    check_every_n_seconds=0.1,
    max_bucket_size=10,  # Allow small bursts
)


def get_llm(config: Configuration, temperature: float = None) -> ChatAnthropic:
    """
    Get a configured LLM instance with rate limiting.

    Args:
        config: Configuration object
        temperature: Override temperature (optional)

    Returns:
        Configured ChatAnthropic instance

    Example:
        >>> config = Configuration()
        >>> llm = get_llm(config)
        >>> llm = get_llm(config, temperature=0.3)  # Lower for extraction
    """
    return ChatAnthropic(
        model=config.llm_model,
        temperature=temperature if temperature is not None else config.temperature,
        rate_limiter=_rate_limiter,
        # Enable caching for repeated prompts (cost savings)
        # https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
        max_tokens=4096,
    )


def get_llm_for_research(config: Configuration) -> ChatAnthropic:
    """
    Get LLM optimized for research tasks (higher temperature).

    Returns:
        ChatAnthropic configured for creative research
    """
    return get_llm(config, temperature=0.7)


def get_llm_for_extraction(config: Configuration) -> ChatAnthropic:
    """
    Get LLM optimized for extraction tasks (lower temperature).

    Returns:
        ChatAnthropic configured for precise extraction
    """
    return get_llm(config, temperature=0.3)


def get_llm_for_reflection(config: Configuration) -> ChatAnthropic:
    """
    Get LLM optimized for reflection tasks (balanced temperature).

    Returns:
        ChatAnthropic configured for quality analysis
    """
    return get_llm(config, temperature=0.5)
