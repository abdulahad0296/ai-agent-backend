from django.shortcuts import render
from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import run_ai_agent
from .models import AgentInteraction

def trigger_agent(request):
    # Get the 'prompt' from the URL, or use a default if missing
    user_prompt = request.GET.get('prompt', 'Default instruction')

    # Pass this prompt to the Celery task
    task = run_ai_agent.delay(user_prompt)   
    

    return JsonResponse({
        "status": "success", 
        "message": "Agent started working.", 
        "task_id": task.id,
        "input_received": user_prompt
    })

def get_task_status(request, task_id):
    # Ask Celery about this specific ID
    result = AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": result.status, 
        "result": result.result if result.ready() else None
    }
    
    return JsonResponse(response)

def index(request):
    # This is to fetch last 5 chats in newest first order
    history = AgentInteraction.objects.all().order_by('created_at') 
    return render(request, 'agents/index.html', {'history': history})