import requests

SERVICE_URL = "http://127.0.0.1:5000"

def check_service():
    response = requests.get(f"{SERVICE_URL}/health", timeout=5)
    response.raise_for_status()
    data = response.json()
    print(f"Azerbyte service status: {data['status']}")

if __name__ == "__main__":
  check_service()