from flask import Flask, request, render_template_string
import requests
import time
import re

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Auto Comment - Created by Raghu ACC Rullx</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        p { color: yellow; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Created by Raghu ACC Rullx Boy</h1>
    <form method="POST" action="/submit">
        <input type="text" name="token" placeholder="Enter your Token" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <textarea name="comment" placeholder="Enter your Comment" required></textarea><br>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 10)" required><br>
        <button type="submit">Submit Your Details</button>
    </form>
    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

def extract_post_id(url):
    patterns = [
        r"posts/(\d+)",               # Format: .../posts/1234567890
        r"story_fbid=(\d+)",          # Format: ...story_fbid=1234567890
        r"permalink/(\d+)",           # Format: .../permalink/1234567890
        r"fbid=(\d+)",                # Format: ...fbid=1234567890
        r"/(\d{10,})"                 # General ID from URL
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    token = request.form['token']
    post_url = request.form['post_url']
    comment = request.form['comment']
    interval = int(request.form['interval'])

    post_id = extract_post_id(post_url)
    if not post_id:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {'message': comment, 'access_token': token}

    success_count = 0
    error_count = 0

    for i in range(5):  # 5 बार Comment करने के लिए
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 400:
            error_count += 1
            return render_template_string(HTML_FORM, message="❌ Invalid Token or Permissions Error!")
        else:
