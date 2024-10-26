import os

from langchain_anthropic import ChatAnthropic


def claude_haiku():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key is not None:
        return ChatAnthropic(model="claude-3-haiku-20240307", api_key=api_key)


def claude_sonnet():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key is not None:
        return ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=api_key)
