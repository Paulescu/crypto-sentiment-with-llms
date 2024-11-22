from typing import Optional, Literal
import json
from pydantic import BaseModel, Field

from llama_index.llms.anthropic import Anthropic
from llama_index.core.prompts import PromptTemplate

from .config import AnthropicConfig


def pprint(model: BaseModel):
    print(json.dumps(model.model_dump(), indent=2))

class NewsMarketSignal(BaseModel):
    """
    Market signal of a news article about the crypto market
    """
    signal: Literal["bullish", "bearish", "neutral"] = Field(description="""
        The market signal of the news article about the crypto market.
        Set it as neutral if the text is not related to crypto market, or not enough
        information to determine the signal.
    """)

    reasoning: str = Field(description="""
        The reasoning for the market signal.
        Set it as non-relevant if the text is not related to crypto market
        Set it as non-enough-info if there is not enough information to determine the signal
    """)


class ClaudeMarketSignalExtractor:
    """
    A class to extract market signal from text using Claude's API
    """
    def __init__(self):
        """
        Initialize the ClaudeMarketSignalExtractor.
        """
        config = AnthropicConfig()
        
        self.llm = Anthropic(
            model=config.model_name,
            max_tokens=config.max_tokens,
            api_key=config.api_key,
        )

        self.prompt = PromptTemplate(
            """
            You are an expert at analyzing news articles related to cryptocurrencies and
            extracting market signal from the text in a structured format.

            Here is the news article:
            {text}
            """
        )

    def get_signal(self, text: str) -> NewsMarketSignal:
        """
        Extract the market signal from the text.

        Args:
            text (str): The text to extract the sentiment from.

        Returns:
            SentimentScore: The sentiment score.
        """
        response = self.llm.structured_predict(
            NewsMarketSignal, self.prompt, text=text
        )

        return response

if __name__ == "__main__":
    
    # initialize the sentiment extractor
    llm = ClaudeMarketSignalExtractor()
    
    # example 1 -> positive signal
    text = "Trump Said appoints Crypto Lawyer Teresa Goody Guillén to Lead SEC"
    response = llm.get_signal(text)
    print(text)
    pprint(response)

    # example 2 -> negative signal
    text = "FED to increase interest rates"
    response = llm.get_signal(text)
    print(text)
    pprint(response)

    # example 3 -> non-relevant text
    text = "City Holder Daily Combo and Daily Quiz November 22, 2024"
    response = llm.get_signal(text)
    print(text)
    pprint(response)

    # example 4 -> non-relevant text
    text = "The grass is green"
    response = llm.get_signal(text)
    print(text)
    pprint(response)
