from flask import Flask, request, render_template_string
import requests
import time
import random
import socks
import socket

# Setting up TOR proxy (VPN)
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket  # Redirect all requests through TOR VPN

app = Flask(__name__)

# HTML Form
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment - VPN Protected</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Facebook Auto Comment - VPN Protected</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt" required><br>
        <input type="file" name="comment_file" accept=".txt" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 30)" required><br>
        <button type="submit">Start Safe Commenting</button>
    </form>
    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    token_file = request.files['token_file']
    comment_file = request.files['comment_file']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    tokens = token_file.read().decode('utf-8').splitlines()
    comments = comment_file.read().decode('utf-8').splitlines()

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    success_count = 0

    while True:
        for i, token in enumerate(tokens):
            comment = comments[i % len(comments)]  # Comment Rotation
            modified_comment = f"{comment} {random.choice(['🔥', '😊', '💯', '✔️', '✨'])}"  # Unique Comment Variation
            payload = {'message': modified_comment, 'access_token': token}
            
            try:
                response = requests.post(url, data=payload)
                
                if response.status_code == 200:
                    success_count += 1
                    print(f"✅ Comment Posted with Token {i+1}")
                elif response.status_code == 400:
                    print(f"❌ Token {i+1} Invalid or Blocked, Skipping...")
                    continue  # Skip Blocked Token
                else:
                    print(f"⚠️ Unexpected Error with Token {i+1}, Skipping...")
                    continue  # Skip Other Errors
            except requests.exceptions.RequestException as e:
                print(f"🔴 Connection Error! Check if TOR is running: {e}")
                continue
            
            # Randomized Delay + Changing IP
            sleep_time = interval + random.randint(5, 15)
            print(f"⏳ Waiting for {sleep_time} seconds... Changing IP...")
            
            # Send signal to TOR to change IP
            try:
                with open("/var/run/tor/control", "w") as tor:
                    tor.write("SIGNAL NEWNYM\n")
            except:
                pass  # If running on Windows, ignore this step
            
            time.sleep(sleep_time)

        print("🔁 Restarting Token Rotation...")
        time.sleep(20)  # Pause before restarting cycle

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
