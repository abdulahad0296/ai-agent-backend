from celery import shared_task
import os
from groq import Groq
from .models import AgentInteraction
from duckduckgo_search import DDGS
from datetime import datetime # <--- 1. Import this

@shared_task
def run_ai_agent(user_prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key: return "Error: API Key missing!"

    # 2. Get Today's Date
    today = datetime.now().strftime("%B %Y") # e.g., "December 2025"

    print(f"--- [SEARCHING] Web for: {user_prompt} ---")
    try:
        # 3. Search (We append the year to the query to force recent results)
        # If user asks "Who won the world cup", we search "Who won the world cup 2025" etc.
        search_query = f"{user_prompt}" 
        results = DDGS().text(search_query, max_results=5, backend="html")
        
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
        
        # 4. Prompt with TIME CONTEXT
        system_prompt = f"""
        You are a helpful AI assistant.
        TODAY'S DATE: {today}
        
        CONTEXT FROM WEB SEARCH:
        {web_context}
        
        INSTRUCTIONS:
        1. Answer the user's question using the search results.
        2. Pay attention to dates! Do not report events from 2022 as "current" if they are old.
        3. If the user asks about the "Cricket World Cup", distinguish between T20 (2022, 2024) and ODI (2023).
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant", 
        )

        ai_response = chat_completion.choices[0].message.content

        AgentInteraction.objects.create(prompt=user_prompt, response=ai_response)
        return ai_response

    except Exception as e:
        return f"Error: {str(e)}"