import os
from dotenv import load_dotenv


# LangSmith tracing is automatically enabled if LANGCHAIN_TRACING_V2=true in .env
# View traces at: https://smith.langchain.com/

# Import agents
from agents.orchestrator import generate_story
from agents.evaluator import evaluate_story

load_dotenv()


"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

IMMEDIATE IMPROVEMENTS (2 hours):
1. Expand genre coverage - CurAdd 5+ specialized writers (adventure, science, friendship, mythology, historical) with 
   curated few-shot examples for each
2. Evaluation dashboard - Persist stories with rubric scores to PostgreSQL, analyze patterns to identify weak dimensions
   and continuously improve prompts


NEXT PHASE (Additional time): 
3. Store User Feedback: Create a pipeline to injest user feedback into the system to improve the story generation process.
4. RAG-enhanced generation - Build vector store of high-quality stories, retrieve similar examples dynamically based
   on user request for better contextual generation
5. Build Continous Evaluation Pipeline: Create a pipeline to sample conversations at random and continuously evaluate the story generation process and improve the system schedueld via async workers.

"""


def generate_story_pipeline(user_request: str, conversation_history: list = None):
    """
    Complete story generation pipeline using ReAct agent orchestration.
    
    Flow:
    1. ReAct agent reasons and calls appropriate writer tool (with conversation context)
    2. Evaluate with rubric and fix if needed
    3. Return final story with scores and updated conversation history
    
    Args:
        user_request: Current user request (new story or modification)
        conversation_history: List of previous messages for multi-turn context
    
    Returns:
        dict: Contains story, evaluation, and updated conversation history
    """
    # ReAct agent will reason and call the right tool with conversation context
    story_text, updated_messages = generate_story(user_request, conversation_history)
    word_count = len(story_text.split())
    print(f"✅ Story generated ({word_count} words)")
    
    # Evaluate and fix if needed
    print("📊 Evaluating quality...")
    evaluation = evaluate_story(story_text)
    
    # Show summary
    print(f"Overall Score: {evaluation.overall_score:.1f}/10 - {'✅ Approved' if evaluation.approved else '⚠️ Needs improvement'}")
    
    if not evaluation.approved:
        # Identify which dimensions were below threshold
        scores_dict = evaluation.scores.model_dump()
        low_scores = [dim for dim, score in scores_dict.items() if score < 7.0]
        if low_scores:
            print(f"🔧 Improved: {', '.join(low_scores)}")
    
    # Always return result - evaluator will fix issues if needed
    return {
        "story": story_text,
        "word_count": word_count,
        "evaluation": evaluation,
        "conversation_history": updated_messages
    }


def main():
    print("=" * 70)
    print("🌟 AmoghxHippocraticAI Storyteller 🌟")
    print("=" * 70)
    print("\nThe StoryTeller agent has access to three specialized writers:")
    print("  👑 Princess Writer - Royal tales with magic and enchantment")
    print("  🎄 Christmas Writer - Holiday stories about giving and joy")
    print("  🦁 Animal Writer - Wise animals and nature lessons")
    print("\nStories are 400-500 words, evaluated and improved automatically!")
    print("💬 Multi-turn support: Request changes after your story is generated!")
    print("=" * 70)
    
    # Initialize conversation state (empty list to maintain message history)
    conversation_history = []
    
    # Initial story request
    user_input = input("\n📖 What kind of story do you want to hear?\n> ")
    
    # Multi-turn conversation loop
    while True:
        print("\n" + "=" * 70)
        print("🔮 Generating your personalized story...")
        print("=" * 70)
        
        # Generate story with conversation context
        result = generate_story_pipeline(user_input, conversation_history)
        
        if result:
            # Update conversation history with full agent messages (user + assistant + tool calls)
            conversation_history = result['conversation_history']
            
            # Use fixed story if available, otherwise original
            final_story = result['evaluation'].fixed_story if result['evaluation'].fixed_story else result['story']
            final_word_count = len(final_story.split())
            
            # Display the story
            print("\n" + "=" * 70)
            print("📚 YOUR STORY")
            print("=" * 70)
            print(f"\n{final_story}\n")
            print("=" * 70)
            print(f"\n✨ Story Complete! ({final_word_count} words)")
            print(f"Quality Score: {result['evaluation'].overall_score:.1f}/10")
            if result['evaluation'].fixed_story:
                print("🔧 Story was improved by evaluator to meet all quality standards")
            print("=" * 70)
            
            # Ask user for next action
            print("\n💬 What would you like to do next?")
            print("  - Type 'end' to finish")
            print("  - Or describe any changes you'd like (e.g., 'make the princess braver', 'add a dragon')")
            
            next_action = input("\n> ").strip().lower()
            
            if next_action == 'end':
                print("\n" + "=" * 70)
                print("🌙 Thank you for using the Storyteller! Sweet dreams!")
                print("=" * 70)
                break
            else:
                # User wants to make changes - set up for next iteration
                user_input = f"Modify the story: {next_action}"
                print(f"\n🔄 Applying your changes: '{next_action}'")


if __name__ == "__main__":
    main()