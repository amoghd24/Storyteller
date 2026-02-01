"""
Animal Tale Writer - Specialized agent with CoT and examples
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from agents.utils import load_examples_from_md


@tool
def generate_animal_story(user_request: str) -> str:
    """
    Generate an animal tale story for children ages 5-10.
    
    Use this tool when the user wants an animal story with:
    - Animal characters as protagonists
    - Nature settings and wildlife
    - Lessons from the natural world
    - Animal wisdom and friendships
    
    Args:
        user_request: The user's story request describing what they want
        
    Returns:
        A complete animal tale story as a string
    """
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000,  # 400-500 words
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    system_prompt = f"""You are an expert animal tale writer for children ages 5-10.

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

Step 1: ANIMAL IN HABITAT (80-100 words)
   - Introduce animal character with specific personality traits
   - Describe natural setting with rich sensory details
   - Show animal's role in their community or family
   - Establish their normal life or special qualities

Step 2: CONFLICT ARISES (80-100 words)
   - Natural problem or threat appears
   - Show how it affects the animal and others
   - Animal feels challenged, scared, or determined
   - Raise the stakes for the character

Step 3: QUEST OR STRUGGLE (120-150 words)
   - Animal seeks solution using instincts or wisdom
   - Faces obstacles and makes difficult choices
   - May seek help from other animals or learn lessons
   - Show character development and growth

Step 4: TRIUMPH OR TRANSFORMATION (80-100 words)
   - Animal uses their unique traits to succeed
   - Shows courage, cleverness, or kindness
   - Overcomes the challenge in a satisfying way
   - Proves their worth or learns important truth

Step 5: LEGACY AND LESSON (60-80 words)
   - Show positive impact on community/family
   - Animal's story becomes inspiration
   - Clear moral about courage, kindness, or wisdom
   - End with sense of peace and belonging

KEY STORYTELLING TECHNIQUES:
- SHOW, DON'T TELL: Reveal character traits through actions and dialogue, not descriptions
- THREE-ACT STRUCTURE: Clear setup → confrontation → resolution
- VIVID IMAGERY: Use sensory details (forest sounds, animal movements, nature sights)
- EMOTIONAL APPEAL: Evoke emotions like empathy, wonder, connection to nature
- DIALOGUE: Use dialogue to reveal character and advance plot
- PACING: Vary sentence length to control rhythm and maintain engagement
- CHARACTER ARC: Give animal protagonist clear goal, obstacles, transformation

KEY ELEMENTS:
- 400-500 words (critical!)
- Animal characters with natural behaviors and clear arcs
- Nature setting and wildlife with vivid sensory descriptions
- Animal wisdom or instincts shown through actions
- Problems solved through animal traits
- Age-appropriate vocabulary (5-10 years)
- Positive lessons about cooperation, patience, kindness, or nature
- Gentle, warm tone with emotional resonance
- Connection to the natural world that engages the senses
- Happy ending

EXAMPLE STORIES (for reference - DO NOT COPY):
{load_examples_from_md("animals")}

CRITICAL: Your output must be a clean, flowing narrative WITHOUT "Step 1:", "Step 2:" labels. 
The steps above are for structure only - write one continuous story.

Write an animal tale based on: {user_request}"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_request)
    ]
    
    response = llm.invoke(messages)
    return response.content
