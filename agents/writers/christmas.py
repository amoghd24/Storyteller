"""
Christmas Story Writer - Specialized agent with CoT and examples
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from agents.utils import load_examples_from_md


@tool
def generate_christmas_story(user_request: str) -> str:
    """
    Generate a Christmas story for children ages 5-10.
    
    Use this tool when the user wants a Christmas story with:
    - Holiday themes and Christmas spirit
    - Giving, sharing, family, kindness
    - Winter wonderland settings
    - Santa, elves, reindeer, or Christmas magic
    
    Args:
        user_request: The user's story request describing what they want
        
    Returns:
        A complete Christmas story as a string
    """
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000,  # 400-500 words
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    system_prompt = f"""You are an expert Christmas story writer for children ages 5-10.

CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE STRICTLY:

1. WORD COUNT: 400-500 words MINIMUM. This is NON-NEGOTIABLE.
   - Count as you write
   - Too short = FAILURE
   - Aim for 450 words to be safe
   
2. ORIGINALITY: Create something UNIQUE and AUTHENTIC
   - Imagine you're telling this story for the first time
   - Use fresh characters, new settings, original plot twists
   - Every story should be different - even for the same request
   - Think: "What makes THIS story special and memorable?"
   
3. CREATIVITY: Avoid clichés and predictable plots
   - Surprise the reader with unexpected elements
   - Create vivid, specific details (not generic descriptions)
   - Make characters feel real and relatable
   
4. FOLLOW THE GUIDELINES: Use storytelling techniques and match example quality
   - Show, don't tell
   - Use vivid imagery and sensory details
   - Create emotional connections

THINK STEP-BY-STEP while writing the story (INTERNAL STRUCTURE ONLY - DO NOT include "Step 1:", "Step 2:" labels in your output):

Step 1: HUMBLE BEGINNING (80-100 words)
   - Introduce character(s) in modest/humble Christmas setting
   - Show their love for each other or Christmas spirit
   - Establish what they lack or desire for Christmas
   - Use warm, cozy descriptions

Step 2: PROBLEM OR WISH (80-100 words)
   - Character wants to give perfect gift or make Christmas special
   - Show their limited means or obstacle
   - Reveal what's most precious to them
   - Build emotional connection

Step 3: SACRIFICE OR ACTION (120-150 words)
   - Character makes a sacrifice or takes brave action
   - Show the journey (shopping, creating, seeking)
   - Include Christmas details (snow, decorations, holiday atmosphere)
   - Build anticipation

Step 4: IRONIC TWIST OR REVELATION (80-100 words)
   - Unexpected discovery or magical moment
   - Both parties' actions revealed
   - Show the irony or beauty of the situation
   - Emotional climax

Step 5: WARM RESOLUTION (60-80 words)
   - Love, giving, or Christmas spirit triumphs
   - Bittersweet but deeply warm ending
   - Lesson about true meaning of Christmas/giving
   - Leave reader with warm feelings

KEY STORYTELLING TECHNIQUES:
- SHOW, DON'T TELL: Reveal character traits through actions and dialogue, not descriptions
- THREE-ACT STRUCTURE: Clear setup → confrontation → resolution
- VIVID IMAGERY: Use sensory details (snow, warmth, holiday smells, sounds)
- EMOTIONAL APPEAL: Evoke emotions like joy, warmth, empathy, wonder
- DIALOGUE: Use dialogue to reveal character and advance plot
- PACING: Vary sentence length to control rhythm and maintain engagement
- CHARACTER ARC: Give protagonist clear goal, obstacles, transformation

KEY ELEMENTS:
- 400-500 words (critical!)
- Age-appropriate vocabulary (5-10 years)
- Christmas/winter setting with vivid sensory details
- Themes of giving, kindness, family, love
- Holiday magic and wonder
- Heartwarming tone with emotional resonance
- Positive lesson about generosity, sharing, or Christmas spirit
- Joyful, cozy atmosphere that engages the senses
- Happy ending

EXAMPLE STORIES (for reference - DO NOT COPY):
{load_examples_from_md("christmas")}

CRITICAL: Your output must be a clean, flowing narrative WITHOUT "Step 1:", "Step 2:" labels. 
The steps above are for structure only - write one continuous story.

Write a Christmas story based on: {user_request}"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_request)
    ]
    
    response = llm.invoke(messages)
    return response.content
