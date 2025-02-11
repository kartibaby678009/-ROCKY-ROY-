from flask import Flask, request, render_template_string
import requests
import time

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
        button:hover { background-color: darkgreen; }
    </style>
</head>
<body>
    <h1>Created by Raghu ACC Rullx Boy</h1>
    <form method="POST" action="/submit">
        <input type="text" name="token" placeholder="Enter your Token" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <textarea name="comment" placeholder="Enter your Comment" required></textarea><br>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 5)" required><br>
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
    token = request.form['token']
    post_url = request.form['post_url']
    comment = request.form['comment']
    interval = int(request.form['interval'])

    # Post ID Extract करने का तरीका अपडेट किया गया
    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {'message': comment, 'access_token': token}

    success_count = 0
    for i in range(5):  # 5 बार Comment करने के लिए (आवश्यकतानुसार बदल सकते हो)
        try:
            response = requests.post(url, data=payload)

            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 400:
                return render_template_string(HTML_FORM, message="❌ Invalid Token or Permissions Error!")
            else:
                return render_template_string(HTML_FORM, message="⚠️ Something Went Wrong!")

            time.sleep(interval)  # Slow Commenting के लिए

        except requests.exceptions.RequestException:
            return render_template_string(HTML_FORM, message="⚠️ Network Error Occurred!")

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
