import requests
from config import API_URL


def upload_pdfs_api(files):
    files_payload = [("files", (f.name, f.read(), "application/pdf")) for f in files]
    return requests.post(f"{API_URL}/upload_pdfs/", files=files_payload)


def ask_question(question, model_name=None, temperature=0.1):
    """Ask a question with optional model and temperature selection."""
    data = {"question": question, "temperature": temperature}
    if model_name:
        data["model_name"] = model_name
    return requests.post(f"{API_URL}/ask/", data=data)


def get_available_models():
    """Get available Gemini models from the server."""
    try:
        response = requests.get(f"{API_URL}/models")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching models: {e}")
        return None