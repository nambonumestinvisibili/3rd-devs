from typing import List, Dict, Any, Union
from openai import OpenAI
import os

class OpenAIService:
    def __init__(self):
        """Initialize OpenAI client with API key from environment."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = False
    ) -> Union[Any, AsyncGenerator[Any, None]]:
        """
        Send a completion request to OpenAI API.
        
        Args:
            messages: List of message dictionaries with role and content
            model: The model to use for completion
            stream: Whether to stream the response
            
        Returns:
            OpenAI completion response or stream
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream
            )
            return response
            
        except Exception as e:
            print(f"Error in OpenAI completion: {str(e)}")
            raise 