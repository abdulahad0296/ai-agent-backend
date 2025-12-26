from django.shortcuts import render, redirect
from django.http import JsonResponse
from .tasks import run_ai_agent, AgentInteraction
from celery.result import AsyncResult
import uuid 

def index(request):
    # 1. FORCE SESSION CREATION AND SAVE
    if not request.session.session_key:
        request.session.create()
        request.session.save() 
    # 2. Get or Create a Conversation ID
    if request.method == 'GET' and 'conversation_id' not in request.GET:
        conversation_id = str(uuid.uuid4())[:8]
    else:
        conversation_id = request.GET.get('conversation_id')

    # 3. Only load messages for THIS conversation
    history = AgentInteraction.objects.filter(
        session_id=request.session.session_key,
        conversation_id=conversation_id
    ).order_by('created_at')

    return render(request, 'agents/index.html', {
        'history': history,
        'conversation_id': conversation_id
    })

def start_task(request):
    prompt = request.GET.get('prompt')
    
    # 4. Get IDs to pass to the worker
    session_id = request.session.session_key
    conversation_id = request.GET.get('conversation_id')

    if prompt and session_id and conversation_id:
        # Pass IDs to the worker
        task = run_ai_agent.delay(prompt, session_id, conversation_id)
        return JsonResponse({'task_id': task.id})
    return JsonResponse({'error': 'Missing data'}, status=400)

def get_status(request, task_id):
    
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
    return JsonResponse(result)