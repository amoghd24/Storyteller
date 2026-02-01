"""
Princess Story Writer - Specialized agent with CoT and examples
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from agents.utils import load_examples_from_md


@tool
def generate_princess_story(user_request: str) -> str:
    """
    Generate a princess story for children ages 5-10.
    
    Use this tool when the user wants a princess story with:
    - Royal characters (princesses, princes, kings, queens)
    - Magic and fairy tales
    - Castles, kingdoms, enchantments
    - Classic princess themes and adventures
    
    Args:
        user_request: The user's story request describing what they want
        
    Returns:
        A complete princess story as a string
    """
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,  # Higher for creativity
        max_tokens=1000,  # 400-500 words
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    system_prompt = f"""You are an expert princess story writer for children ages 5-10.

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

Step 1: CHARACTER IN SITUATION (80-100 words)
   - Introduce princess in her current life (trapped, oppressed, or longing)
   - Show her kind heart despite difficulties
   - Establish what she dreams of or desires
   - Use dialogue and internal thoughts

Step 2: OPPORTUNITY OR MAGICAL HELPER (80-100 words)
   - Introduce a magical element (fairy godmother, prince, enchanted object)
   - Show moment of hope or possibility
   - Create anticipation and wonder

Step 3: TRANSFORMATION/JOURNEY (120-150 words)
   - Magical transformation or escape plan
   - Princess takes action with courage
   - Include magical details and helpers
   - Build tension with obstacles

Step 4: CRISIS AND CLIMAX (80-100 words)
   - Time limit, discovery, or major obstacle
   - Princess must make choice or face challenge
   - Show her true character (brave, kind, clever)
   - Turning point of the story

Step 5: REUNION AND RESOLUTION (60-80 words)
   - Quest completed or reunion happens
   - Happy ending with lesson learned
   - Forgiveness, love, or magic prevails
   - "Happily ever after" tone

KEY STORYTELLING TECHNIQUES:
- SHOW, DON'T TELL: Reveal character traits through actions and dialogue, not descriptions
- THREE-ACT STRUCTURE: Clear setup → confrontation → resolution
- VIVID IMAGERY: Use sensory details (sights, sounds) to create immersive experience
- EMOTIONAL APPEAL: Evoke emotions like empathy, joy, wonder
- DIALOGUE: Use dialogue to reveal character and advance plot
- PACING: Vary sentence length to control rhythm and maintain engagement
- CHARACTER ARC: Give protagonist clear goal, obstacles, transformation

KEY ELEMENTS:
- 400-500 words (critical!)
- Age-appropriate vocabulary (5-10 years)
- Royal/magical setting with vivid descriptions
- Kind, brave protagonist with clear character arc
- Enchanting elements (fairy godmother, magic, etc.)
- Clear problem and resolution
- Positive lesson about kindness, courage, or believing in yourself
- Happy ending with emotional resonance
- Beautiful, descriptive language that engages the senses

EXAMPLE STORIES (for reference - DO NOT COPY):
{load_examples_from_md("princess")}

CRITICAL: Your output must be a clean, flowing narrative WITHOUT "Step 1:", "Step 2:" labels. 
The steps above are for structure only - write one continuous story.

Write a princess story based on: {user_request}"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_request)
    ]
    
    response = llm.invoke(messages)
    return response.content
