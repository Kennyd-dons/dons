import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

def main():
    # Initialize Groq client
    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),
    )
    
    # Enable instructor integration
    client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)
    
    print("Welcome to the Groq AI Chat! Type 'quit' to exit.")
    
    while True:
        # Get user input
        user_input = input("\nAsk me anything: ")
        
        # Check for quit command
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        try:
            # Make API call
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                response_model=Character,
            )
            
            # Print formatted response
            print("\nResponse:")
            print(response.model_dump_json(indent=2))
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
