from fetch_token import fetch_token
import requests as req

next_action = fetch_token()

def login(email):
    
    url = "https://login.unity.com/en/sign-in"

    headers = {
        "Next-Action": next_action,
        "Content-Type": "text/plain; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://login.unity.com",
    "Referer": "https://login.unity.com/en/sign-in"
    }
    raw_data = f'["{email}"]'

    response = req.post(url, headers=headers, data=raw_data)
    res = response.text
    print(f"status_code: {response.status_code}\nresponse_text: {res}")
    if(res[-6:-1] == "false"):
        print("Login Successful")
        return True
    elif(res[-5:-1] == "true"):
        print("Login Failed")
        return False
    else:
        print("Error: Fetching Next-Action token failed")
        return False
    
    
