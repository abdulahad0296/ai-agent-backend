from duckduckgo_search import DDGS

print("Attempting to search...")

try:
    # Try the 'html' backend first (usually most reliable)
    results = DDGS().text("current bitcoin price", max_results=3, backend="html")
    
    if results:
        print("\n✅ SUCCESS! Found results:")
        for r in results:
            print(f"- {r['title']}")
            print(f"  Body: {r['body'][:100]}...") # Show first 100 chars
    else:
        print("\n❌ Backend 'html' returned nothing.")

except Exception as e:
    print(f"\n💥 Error: {e}")