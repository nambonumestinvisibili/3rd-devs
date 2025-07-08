from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from openai import OpenAI
import os

# Import OpenAIService equivalent
from openai_service import OpenAIService  # You'll need to create this file

app = FastAPI()
openai_service = OpenAIService()
previous_summarization = ""

class Message(BaseModel):
    content: str

async def generate_summarization(user_message: Dict[str, str], assistant_response: Dict[str, str]) -> str:
    """Generate summarization based on the current turn and previous summarization."""
    global previous_summarization
    
    summarization_prompt = {
        "role": "system",
        "content": f"""Please summarize the following conversation in a concise manner, incorporating the previous summary if available:
<previous_summary>{previous_summarization or "No previous summary"}</previous_summary>
<current_turn> User: {user_message['content']}\nAssistant: {assistant_response['content']} </current_turn>
"""
    }

    response = await openai_service.completion(
        messages=[
            summarization_prompt,
            {"role": "user", "content": "Please create/update our conversation summary."}
        ],
        model="gpt-4o-mini",
        stream=False
    )
    
    return response.choices[0].message.content or "No conversation history"

def create_system_prompt(summarization: str) -> Dict[str, str]:
    """Create system prompt with conversation history."""
    content = "You are Alice, a helpful assistant who speaks using as few words as possible.\n\n"
    
    if summarization:
        content += f"""Here is a summary of the conversation so far:
<conversation_summary>
  {summarization}
</conversation_summary>"""
    
    content += "\nLet's chat!"
    
    return {
        "role": "system",
        "content": content
    }

@app.post("/api/chat")
async def chat(message: Message):
    """Handle chat endpoint."""
    global previous_summarization
    
    try:
        system_prompt = create_system_prompt(previous_summarization)
        
        assistant_response = await openai_service.completion(
            messages=[system_prompt, {"role": "user", "content": message.content}],
            model="gpt-4o",
            stream=False
        )
        
        # Generate new summarization
        previous_summarization = await generate_summarization(
            {"role": "user", "content": message.content},
            assistant_response.choices[0].message
        )
        
        return assistant_response
        
    except Exception as error:
        print(f"Error in OpenAI completion: {str(error)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")

@app.post("/api/demo")
async def demo():
    """Handle demo endpoint."""
    global previous_summarization
    
    demo_messages = [
        {"content": "Hi! I'm Adam", "role": "user"},
        {"content": "How are you?", "role": "user"},
        {"content": "Do you know my name?", "role": "user"}
    ]
    
    assistant_response = None
    
    for message in demo_messages:
        print("--- NEXT TURN ---")
        print(f"Adam: {message['content']}")
        
        try:
            system_prompt = create_system_prompt(previous_summarization)
            
            assistant_response = await openai_service.completion(
                messages=[system_prompt, message],
                model="gpt-4o",
                stream=False
            )
            
            print(f"Alice: {assistant_response.choices[0].message.content}")
            
            # Generate new summarization
            previous_summarization = await generate_summarization(
                message,
                assistant_response.choices[0].message
            )
            
        except Exception as error:
            print(f"Error in OpenAI completion: {str(error)}")
            raise HTTPException(status_code=500, detail="An error occurred while processing your request")
    
    return assistant_response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000) 