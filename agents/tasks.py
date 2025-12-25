from celery import shared_task
import os
from groq import Groq
from .models import AgentInteraction
from duckduckgo_search import DDGS
from datetime import datetime

@shared_task
def run_ai_agent(user_prompt, session_id, conversation_id):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key: return "Error: API Key missing!"

    today = datetime.now().strftime("%B %Y")

    # --- 1. SEARCH WEB (Context for the NEW prompt) ---
    print(f"--- [SEARCHING] Web for: {user_prompt} ---")
    try:
        results = DDGS().text(user_prompt, max_results=5, backend="html")
        web_context = ""
        if results:
            for result in results:
                web_context += f"- {result['title']}: {result['body']}\n"
        else:
            web_context = "No search results found."
    except Exception as e:
        web_context = f"Search Error: {str(e)}"
    
    try:
        client = Groq(api_key=api_key)
        

        # 2. MEMORY UPDATE: Only fetch history for THIS specific conversation
        recent_chats = AgentInteraction.objects.filter(
            session_id=session_id,
            conversation_id=conversation_id
        ).order_by('-created_at')[:5]    

        # Reverse them to be Oldest -> Newest (Chronological order)
        history_messages = []
        for chat in reversed(recent_chats):
            history_messages.append({"role": "user", "content": chat.prompt})
            if chat.response:
                history_messages.append({"role": "assistant", "content": chat.response})
        
        # ----------------------------------------------------

        # 3. Construct the System Prompt
        system_prompt = f"""
        You are a helpful AI assistant.
        TODAY'S DATE: {today}
        
        CONTEXT FROM WEB SEARCH (Use this if relevant to the user's latest message):
        {web_context}
        
        INSTRUCTIONS:
        1. Answer the user's latest question.
        2. use the conversation history to understand context (e.g., if user says "he", look at previous messages to know who "he" is).
        3. If the answer is not in the search results or memory, use your own knowledge.
        """

        # 4. Assemble the Full Message Chain
        final_messages = [{"role": "system", "content": system_prompt}]
        final_messages.extend(history_messages) # Add the memory
        final_messages.append({"role": "user", "content": user_prompt}) # Add the new prompt

        # 5. Send to Groq
        chat_completion = client.chat.completions.create(
            messages=final_messages,
            model="llama-3.1-8b-instant", 
        )

        ai_response = chat_completion.choices[0].message.content
        # 3. SAVE with the new IDs
        AgentInteraction.objects.create(
            prompt=user_prompt, 
            response=ai_response,
            session_id=session_id,
            conversation_id=conversation_id
        )
        return ai_response

    except Exception as e:
        return f"Error: {str(e)}"