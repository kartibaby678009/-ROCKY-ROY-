from flask import Flask, request, render_template_string
import requests
import time
import random

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment - Created by Raghu ACC Rullx</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Created by Raghu ACC Rullx Boy</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <label>Upload Tokens:</label><br>
        <input type="file" name="tokens" accept=".txt" required><br>

        <label>Upload Comments:</label><br>
        <input type="file" name="comments" accept=".txt" required><br>

        <label>Post URL:</label><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>

        <label>Time Interval (in seconds):</label><br>
        <input type="number" name="interval" value="400" required><br>

        <button type="submit">Submit Your Details</button>
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
    tokens_file = request.files['tokens']
    comments_file = request.files['comments']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    tokens = tokens_file.read().decode().splitlines()
    comments = comments_file.read().decode().splitlines()

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    for token in tokens:
        for comment in comments:
            url = f"https://graph.facebook.com/{post_id}/comments"
            payload = {'message': comment, 'access_token': token}

            response = requests.post(url, data=payload)

            if response.status_code == 200:
                print(f"✅ Comment Successful: {comment}")
                time.sleep(interval + random.randint(10, 30))  # Random Delay for Anti-Block
            elif response.status_code == 400:
                return render_template_string(HTML_FORM, message="❌ Invalid Token or Permissions Error!")
            else:
                return render_template_string(HTML_FORM, message="⚠️ Something Went Wrong!")

    return render_template_string(HTML_FORM, message="✅ All Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
