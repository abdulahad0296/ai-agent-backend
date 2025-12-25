import requests
import time
import csv
import sys

# 1. The "Golden Dataset"
# These are the questions we ALWAYS want the AI to get right.
TEST_CASES = [
    "What is the capital of France?",
    "Who won the Cricket World Cup 2023?",
    "Explain Quantum Computing in one sentence.",
    "What is the current price of Bitcoin?",  # Tests Search
    "Who is the CEO of Tesla?",
    "How old is he?", # Tests Memory (relies on previous question)
]

BASE_URL = "http://127.0.0.1:8000/agents"

def run_evaluation():
    print(f"🚀 Starting Evaluation on {len(TEST_CASES)} test cases...\n")
    
    results = []

    for i, prompt in enumerate(TEST_CASES):
        print(f"[{i+1}/{len(TEST_CASES)}] Testing: '{prompt}'")
        
        start_time = time.time()
        
        try:
            # A. Trigger the Agent
            start_resp = requests.get(f"{BASE_URL}/start/?prompt={prompt}")
            if start_resp.status_code != 200:
                print(f"   ❌ Failed to start task: {start_resp.text}")
                continue
                
            task_id = start_resp.json()['task_id']
            
            # B. Poll for Result (Wait for AI to think)
            while True:
                status_resp = requests.get(f"{BASE_URL}/status/{task_id}/")
                status_data = status_resp.json()
                
                if status_data['status'] == 'SUCCESS':
                    latency = round(time.time() - start_time, 2)
                    response_text = status_data['result']
                    print(f"   ✅ Done in {latency}s")
                    
                    results.append({
                        "prompt": prompt,
                        "response": response_text,
                        "latency_seconds": latency
                    })
                    break
                
                elif status_data['status'] == 'FAILURE':
                    print("   ❌ Task Failed")
                    break
                
                time.sleep(1) # Wait 1s before checking again

        except Exception as e:
            print(f"   💥 Error: {e}")

    # C. Save Report
    save_report(results)

def save_report(results):
    filename = f"eval_report_{int(time.time())}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["prompt", "response", "latency_seconds"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n📝 Report saved to: {filename}")
    print("Check this file to verify the AI's accuracy!")

if __name__ == "__main__":
    run_evaluation()