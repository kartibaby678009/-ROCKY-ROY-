from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rocky Roy CARTER SERVER</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial; }
        input, button { padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; border: none; }
    </style>
</head>
<body>
    <h1>Rocky Roy CARTER SERVER</h1>
    <form method="POST" enctype="multipart/form-data">
        <label>Upload Tokens:</label><br>
        <input type="file" name="tokens" multiple><br>
        
        <label>Upload Messages:</label><br>
        <input type="file" name="messages" multiple><br>
        
        <label>Recipient ID (User/Page ID):</label><br>
        <input type="text" name="recipient_id" required><br>
        
        <label>Time Interval (in seconds):</label><br>
        <input type="number" name="interval" value="400" required><br><br>
        
        <button type="submit">Submit Your Details</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tokens = request.files.getlist('tokens')
        messages = request.files.getlist('messages')
        recipient_id = request.form['recipient_id']
        interval = int(request.form['interval'])

        token_list = [token.read().decode().strip() for token in tokens]
        message_list = [msg.read().decode().strip() for msg in messages]

        for token in token_list:
            for message in message_list:
                send_message(token, recipient_id, message)
                time.sleep(interval)

        return "✅ Messages Sent Successfully!"

    return render_template_string(HTML_PAGE)

def send_message(token, recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/{recipient_id}/messages"
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message},
        'access_token': token
    }
    response = requests.post(url, json=payload)
    print(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
