import subprocess
import json

def get_friend_activity():
    process = subprocess.Popen(
        ["node", "fetch/fetch.js"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    stdout, stderr = process.communicate()
    
    return json.loads(stdout)

friend_activity = get_friend_activity()
print(friend_activity)