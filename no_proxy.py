import requests
import time
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

auth_keys = []
with open("initdata.txt", "r") as file:
    auth_keys = [line.strip() for line in file.readlines()]

def fetch_points(account_number, auth_key):
    headers = {
        "Authorization": f"{auth_key}",
        "User-Agent": user_agent
    }

    while True:
        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                data = response.json()
                points = data.get("data", {}).get("rewardPoint", {}).get("points")
                if points is not None:
                    print(f"Аккаунт {account_number}: {points} pts")
                else:
                    print(f"Pts не найдено в ответе {account_number}...")
            else:
                print(f"Ошибка извлечения данных из аккаунта {account_number}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Ошибка запроза для аккаунта {account_number}: {e}")

        time.sleep(20)

with ThreadPoolExecutor(max_workers=len(auth_keys)) as executor:
    futures = [executor.submit(fetch_points, i + 1, key) for i, key in enumerate(auth_keys)]

    for future in futures:
        future.result()
