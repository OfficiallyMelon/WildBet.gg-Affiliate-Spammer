import tkinter as tk
from tkinter import messagebox
import json
import random
import requests
import string
import time
from faker import Faker
import threading

def generate_temp_email():
    """Generate a temporary email address."""
    faker = Faker()
    email_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    email_domain = faker.domain_name()
    return f"{email_prefix}@{email_domain}"

def sign_up_redeem():
    num_accounts = int(entry_num_accounts.get())
    password = entry_password.get()
    promo_code = entry_promo_code.get()
    
    for _ in range(num_accounts):
        email = generate_temp_email()

        try:
            username, password = register_user(email, password)
            auth_token = login_user(username, password)
            resp = redeem_promo_code(auth_token, promo_code)
            log(f"Registration successful! Email: {email}, Password: {password}")
            log("Login successful!")
            log(f"Auth Token: {auth_token}")
            log(f"Response: {resp}")
            log("Waiting 25 Seconds due to api limits")
            time.sleep(25)
        except requests.exceptions.RequestException as e:
            log(f"An error occurred: {e}")

def sign_up_redeem_thread():
    threading.Thread(target=sign_up_redeem).start()

def load_proxies_from_json(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

def register_user(temp_email, password):
    url = "https://wildbet.gg/api/auth/local/register"
    
    payload = {
        "email": temp_email,
        "username": temp_email,
        "password": password,
        "confirmPassword": password
    }
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Content-Type": "application/json",
        "Origin": "https://wildbet.gg",
        "Referer": "https://wildbet.gg/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return temp_email, password
    else:
        return None, None

def login_user(email, password):
    url = "https://wildbet.gg/api/auth/local/login"
    
    payload = {
        "email": email,
        "username": email,
        "password": password,
        "confirmPassword": "password"
    }
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, zstd",
        "Accept-Language": "en-US,en;q=0.9,en-AU;q=0.8",
        "Content-Type": "application/json",
        "Origin": "https://wildbet.gg",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            auth_token = data.get('authToken')
            return auth_token
        except ValueError:
            return None
    else:
        return None

def redeem_promo_code(auth_token, promo_code):
    url = "https://wildbet.gg/api/affiliates/redeem-code"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": auth_token,
        "Content-Type": "application/json",
        "Referer": "",
        "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    
    payload = {
        "code": promo_code
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    return response.json()

def log(message):
    text_logs.insert(tk.END, message + "\n")
    text_logs.see(tk.END)

# GUI setup
root = tk.Tk()
root.title("WildBet.gg Affiliate Spammer")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_num_accounts = tk.Label(frame, text="Number of Accounts:")
label_num_accounts.grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry_num_accounts = tk.Entry(frame)
entry_num_accounts.grid(row=0, column=1, padx=5, pady=5)

label_password = tk.Label(frame, text="Password:")
label_password.grid(row=1, column=0, padx=5, pady=5, sticky="w")

entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

label_promo_code = tk.Label(frame, text="Promo Code:")
label_promo_code.grid(row=2, column=0, padx=5, pady=5, sticky="w")

entry_promo_code = tk.Entry(frame)
entry_promo_code.grid(row=2, column=1, padx=5, pady=5)

button_submit = tk.Button(frame, text="Submit", command=sign_up_redeem_thread)
button_submit.grid(row=3, columnspan=2, pady=10)

text_logs = tk.Text(frame, height=15, width=50)
text_logs.grid(row=0, column=2, rowspan=4, padx=10, pady=10)

root.mainloop()