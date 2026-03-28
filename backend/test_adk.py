import asyncio, httpx, json
async def test():
    app_name = "generate_suggestions"
    user_id_str = "1"
    ADK_SERVER_URL = "http://127.0.0.1:8001"
    async with httpx.AsyncClient(timeout=60.0) as client:
        session_url = f"{ADK_SERVER_URL}/apps/{app_name}/users/{user_id_str}/sessions"
        session_response = await client.post(session_url, json={})
        assigned_session_id = session_response.json().get("id")
        adk_payload = {
            "appName": app_name,
            "userId": user_id_str,
            "sessionId": assigned_session_id,
            "newMessage": {"role": "user", "parts": [{"text": "Hello, write me a post about GrowthOdds"}]},
            "streaming": False
        }
        run_url = f"{ADK_SERVER_URL}/run"
        print("Waiting for response...")
        response = await client.post(run_url, json=adk_payload)
        with open("adk_resp.json", "w") as f:
            f.write(response.text)
        print("Done. Saved adk_resp.json.")

asyncio.run(test())
