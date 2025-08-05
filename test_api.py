import requests
import json

url = "http://localhost:8000/api/v1/hackrx/run"
headers = {
    "Authorization": "Bearer f54ada5ff8aad823c950caee24b08bafd5d45da70027d16daef3f21f49af01e9",
    "Content-Type": "application/json"
}
payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": ["What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
                  "What is the waiting period for pre-existing diseases (PED) to be covered?"]
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response Text: {response.text}")
        try:
            error_json = response.json()
            print(f"Error JSON: {json.dumps(error_json, indent=2)}")
        except:
            print("Could not parse error response as JSON")
            
except requests.exceptions.ConnectionError:
    print("ERROR: Server is not running on localhost:8000")
    print("Make sure to start uvicorn with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
