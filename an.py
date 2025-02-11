from flask import Flask, request, render_template_string, jsonify
import requests
import time

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Auto Comment Tool - Created by Raghu ACC Rullx</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial; }
        form { background: #222; padding: 20px; margin: auto; width: 300px; border-radius: 10px; }
        input, textarea { width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
        button { background: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: lime; }
    </style>
</head>
<body>
    <h1>Auto Comment Tool</h1>
    <form method="POST">
        <input type="text" name="cookie" placeholder="Enter Facebook Cookies" required><br>
        <input type="text" name="post_url" placeholder="Enter Post URL" required><br>
        <textarea name="comment" placeholder="Enter Your Comment" required></textarea><br>
        <input type="number" name="interval" placeholder="Time Interval (in seconds)" required><br>
        <button type="submit">Submit</button>
    </form>
    <p>Created by Raghu ACC Rullx</p>
</body>
</html>
"""

# Function to post comments
def post_comment(cookie, post_url, comment):
    try:
        post_id = post_url.split('/')[-1].split('?')[0]
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0"
        }
        data = {
            "message": comment
        }
        response = requests.post(f"https://graph.facebook.com/{post_id}/comments", headers=headers, data=data)
        if response.status_code == 200:
            return "✅ Comment Successful!"
        else:
            return f"❌ Error: {response.json().get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        post_url = request.form.get('post_url')
        comment = request.form.get('comment')
        interval = request.form.get('interval')

        if not all([cookie, post_url, comment, interval]):
            return jsonify({"error": "⚠️ All fields are required!"})

        try:
            interval = int(interval)
            result = post_comment(cookie, post_url, comment)
            time.sleep(interval)
            return jsonify({"result": result})
        except ValueError:
            return jsonify({"error": "⏱️ Interval must be a number!"})
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
