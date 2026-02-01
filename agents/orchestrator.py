"""
Orchestrator Agent - Modern LangChain Agent with Writer Tools
"""
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# Import writer tools
from agents.writers.princess import generate_princess_story
from agents.writers.christmas import generate_christmas_story
from agents.writers.animal import generate_animal_story


def generate_story(user_request: str, conversation_history: list = None) -> tuple:
    """
    Generate a story using modern LangChain agent with specialized writer tools.
    
    The agent will:
    1. Reason about which genre fits the request (or modification)
    2. Call the appropriate writer tool
    3. Return the generated story
    
    Args:
        user_request: Current user request (new story or modification)
        conversation_history: List of previous messages for multi-turn context
    
    Returns:
        tuple: (story_text, updated_messages) for state management
    """
    # Initialize model
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.1,  # Low temperature for consistent tool selection
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Define available tools
    tools = [
        generate_princess_story,
        generate_christmas_story,
        generate_animal_story
    ]
    
    # Create agent with tools and system prompt
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="""You are a story orchestrator for children's bedtime stories (ages 5-10).

You have access to three specialized story writer tools:
- generate_princess_story: Use for princess, royal, castle, magic, fairy tale themes
- generate_christmas_story: Use for Christmas, holiday, Santa, winter, giving themes  
- generate_animal_story: Use for animal characters, nature, wildlife, animal wisdom themes

MULTI-TURN CONVERSATION SUPPORT:
- For NEW story requests: Call the appropriate writer tool based on the request
- For MODIFICATIONS: Review the previous story from conversation history, understand the change request,
  then call the writer tool with a modified prompt that incorporates both the original intent AND the changes

CRITICAL GUARDRAILS FOR YOUR RESPONSE:
1. Call the MOST APPROPRIATE writer tool based on the user's request
2. After the tool returns the story, your Final Answer MUST be EXACTLY the story text from the tool
3. DO NOT add "Here is...", "Once upon a time I'll tell you...", titles, or any wrapper text
4. DO NOT summarize, shorten, or paraphrase the story
5. DO NOT add your own sentences before or after the story
6. Your entire response should be ONLY the story text - nothing else
7. Copy the tool output word-for-word as your Final Answer

Example:
Tool returns: "Princess Luna was brave..."
Your Final Answer: "Princess Luna was brave..." (exact same text, nothing added)

NOT: "Here is the story: Princess Luna was brave..."
NOT: "Let me tell you about Princess Luna..."
"""
    )
    
    # Build messages list with conversation history
    if conversation_history:
        messages = conversation_history.copy()
        messages.append({"role": "user", "content": user_request})
    else:
        messages = [{"role": "user", "content": f"Generate a bedtime story: {user_request}"}]
    
    # Invoke agent with full conversation context
    result = agent.invoke({"messages": messages})
    
    # Extract the final message content and return with full message history
    return result["messages"][-1].content, result["messages"]
