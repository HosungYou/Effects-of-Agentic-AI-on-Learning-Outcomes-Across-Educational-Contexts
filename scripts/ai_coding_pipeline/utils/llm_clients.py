#!/usr/bin/env python3
"""
LLM client wrappers for Claude, GPT-4o, and Groq.
Provides unified interface with retry logic, rate limiting, and cost tracking.
"""

import os
import time
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    """Base class for LLM clients."""

    def __init__(self, model: str, cost_tracker=None):
        self.model = model
        self.cost_tracker = cost_tracker

    @abstractmethod
    def send_prompt(self, system: str, user: str, temperature: float = 0.0,
                   max_tokens: int = 4096) -> Dict[str, Any]:
        """Send a prompt and return response."""
        pass

    def retry_with_backoff(self, func, max_retries: int = 3, initial_delay: float = 1.0):
        """
        Retry a function with exponential backoff.

        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds

        Returns:
            Function result
        """
        delay = initial_delay

        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise

                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2

        raise RuntimeError(f"Failed after {max_retries} attempts")


class ClaudeClient(BaseLLMClient):
    """Client for Anthropic Claude API."""

    def __init__(self, model: str = "claude-sonnet-4-5-20250929", cost_tracker=None):
        super().__init__(model, cost_tracker)

        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package required. Install with: pip install anthropic")

        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=api_key)

        # Pricing per million tokens (input/output)
        self.pricing = {
            'claude-sonnet-4-5-20250929': (3.00, 15.00),
            'claude-sonnet-3-5-20241022': (3.00, 15.00),
            'claude-opus-4-6': (15.00, 75.00)
        }

    def send_prompt(self, system: str, user: str, temperature: float = 0.0,
                   max_tokens: int = 4096) -> Dict[str, Any]:
        """
        Send prompt to Claude.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Response dictionary with content and token counts
        """
        def _call():
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[
                    {"role": "user", "content": user}
                ]
            )
            return response

        response = self.retry_with_backoff(_call)

        content = response.content[0].text if response.content else ""
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        if self.cost_tracker:
            self.cost_tracker.track(
                model=self.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )

        return {
            'content': content,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'model': self.model
        }


class GPT4oClient(BaseLLMClient):
    """Client for OpenAI GPT-4o API."""

    def __init__(self, model: str = "gpt-4o", cost_tracker=None):
        super().__init__(model, cost_tracker)

        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)

        self.pricing = {
            'gpt-4o': (2.50, 10.00),
            'gpt-4o-2024-11-20': (2.50, 10.00),
            'gpt-4-turbo': (10.00, 30.00)
        }

    def send_prompt(self, system: str, user: str, temperature: float = 0.0,
                   max_tokens: int = 4096) -> Dict[str, Any]:
        """
        Send prompt to GPT-4o.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Response dictionary with content and token counts
        """
        def _call():
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ]
            )
            return response

        response = self.retry_with_backoff(_call)

        content = response.choices[0].message.content if response.choices else ""
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        if self.cost_tracker:
            self.cost_tracker.track(
                model=self.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )

        return {
            'content': content,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'model': self.model
        }


class GroqClient(BaseLLMClient):
    """Client for Groq API."""

    def __init__(self, model: str = "llama-3.3-70b-versatile", cost_tracker=None):
        super().__init__(model, cost_tracker)

        try:
            from groq import Groq
        except ImportError:
            raise ImportError("groq package required. Install with: pip install groq")

        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")

        self.client = Groq(api_key=api_key)

        self.pricing = {
            'llama-3.3-70b-versatile': (0.59, 0.79),
            'llama-3.1-70b-versatile': (0.59, 0.79),
            'mixtral-8x7b-32768': (0.24, 0.24)
        }

    def send_prompt(self, system: str, user: str, temperature: float = 0.0,
                   max_tokens: int = 4096) -> Dict[str, Any]:
        """
        Send prompt to Groq.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Response dictionary with content and token counts
        """
        def _call():
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ]
            )
            return response

        response = self.retry_with_backoff(_call)

        content = response.choices[0].message.content if response.choices else ""
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        if self.cost_tracker:
            self.cost_tracker.track(
                model=self.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )

        return {
            'content': content,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'model': self.model
        }


def test_clients():
    """Test all clients with a simple prompt."""
    system = "You are a helpful meta-analysis assistant."
    user = "Say 'Hello, World!' and nothing else."

    print("Testing Claude...")
    try:
        claude = ClaudeClient()
        response = claude.send_prompt(system, user)
        print(f"Claude response: {response['content'][:100]}")
        print(f"Tokens: {response['input_tokens']} in, {response['output_tokens']} out")
    except Exception as e:
        print(f"Claude failed: {e}")

    print("\nTesting GPT-4o...")
    try:
        gpt4o = GPT4oClient()
        response = gpt4o.send_prompt(system, user)
        print(f"GPT-4o response: {response['content'][:100]}")
        print(f"Tokens: {response['input_tokens']} in, {response['output_tokens']} out")
    except Exception as e:
        print(f"GPT-4o failed: {e}")

    print("\nTesting Groq...")
    try:
        groq = GroqClient()
        response = groq.send_prompt(system, user)
        print(f"Groq response: {response['content'][:100]}")
        print(f"Tokens: {response['input_tokens']} in, {response['output_tokens']} out")
    except Exception as e:
        print(f"Groq failed: {e}")


if __name__ == "__main__":
    test_clients()
