"""
Evaluator Agent - Story Quality Assessment with Rubric
"""
import os
import warnings
from typing import Optional, Dict
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Suppress LangChain structured output warnings
warnings.filterwarnings("ignore", message=".*json_schema.*gpt-3.5-turbo.*")


class EvaluationScores(BaseModel):
    """Individual rubric scores"""
    age_appropriate: float = Field(description="Score 0-10 for age-appropriate content (5-10 years)")
    grounded: float = Field(description="Score 0-10 for coherent, logical story flow")
    conciseness: float = Field(description="Score 0-10 for appropriate length (400-500 words)")
    engagement: float = Field(description="Score 0-10 for how interesting and captivating")
    structure: float = Field(description="Score 0-10 for clear beginning, middle, end")


class EvaluationResponse(BaseModel):
    """Response schema for story evaluation"""
    scores: EvaluationScores
    overall_score: float = Field(description="Average of all scores (0-10)")
    approved: bool = Field(description="True if overall_score >= 7.0")
    feedback: str = Field(description="Detailed explanation of scores and decision")
    fixed_story: Optional[str] = Field(default=None, description="Improved story if score < 7")


def evaluate_story(story_text: str) -> EvaluationResponse:
    """
    Evaluate story quality using a comprehensive rubric with structured output.
    
    Rubric (each 0-10):
    1. Follows Guardrails - adheres to age-appropriate guidelines
    2. Grounded - coherent, logical story flow
    3. Conciseness - appropriate length (400-500 words)
    4. Engagement - interesting and captivating
    5. Structure - clear beginning, middle, end
    
    If score < 7: Generate fixes
    If score >= 7: Approve as-is
    """
    # Create LLM with structured output
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.1,  # Low temperature for consistent evaluation
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Bind Pydantic model for structured output
    structured_llm = llm.with_structured_output(EvaluationResponse)
    
    system_prompt = """You are a children's story quality evaluator and fixer using a strict rubric.

YOUR TASK:
1. Evaluate the story using the rubric below
2. If ANY individual score < 7.0, FIX the story by:
   - Improving each dimension that scored < 7.0
   - Maintaining the core narrative and charm
   - Keeping 400-500 words
   - Be specific about which areas you improved

EVALUATION RUBRIC (score each 0-10):

1. AGE APPROPRIATE (0-10)
   - Content suitable for 5-10 years
   - No mature themes or inappropriate language
   - Positive messages and tone
   - Kind characters and positive resolution
   - 10 = perfectly appropriate, 0 = inappropriate

2. GROUNDED (0-10)
   - Coherent, logical story flow
   - No plot holes or confusing elements
   - Consistent character behavior
   - 10 = perfectly coherent, 0 = confusing/illogical

3. CONCISENESS (0-10)
   - Appropriate length (400-500 words REQUIRED)
   - No unnecessary repetition
   - Efficient storytelling
   - 10 = 400-500 words perfect pacing, 0 = too long or too short

4. ENGAGEMENT (0-10)
   - Interesting and captivating for kids
   - Maintains attention throughout
   - Emotionally resonant
   - 10 = highly engaging, 0 = boring

5. STRUCTURE (0-10)
   - Clear beginning, middle, end
   - Good pacing and flow
   - Satisfying resolution
   - 10 = excellent structure, 0 = poor structure

DECISION LOGIC:
- Calculate overall_score = average of 5 scores
- If ALL scores >= 7.0: approved=true, fixed_story=null
- If ANY score < 7.0: approved=false, provide complete fixed_story

GUARDRAILS FOR YOUR RESPONSE:
1. You MUST provide age_appropriate score (0-10)
2. You MUST provide grounded score (0-10)
3. You MUST provide conciseness score (0-10)
4. You MUST provide engagement score (0-10)
5. You MUST provide structure score (0-10)
6. You MUST calculate overall_score (average of 5 scores)
7. You MUST set approved (true/false based on all scores >= 7)
8. You MUST provide feedback explaining the scores
9. If approved=false, you MUST provide the complete fixed_story (400-500 words)

Do not skip any fields. Every field is required."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Evaluate this story and fix if ANY score < 7:\n\n{story_text}")
    ]
    
    # Get structured response
    evaluation = structured_llm.invoke(messages)
    
    return evaluation
