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
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Created by Raghu ACC Rullx Boy</h1>
    <form method="POST" action="/submit">
        <input type="text" name="cookies" placeholder="Enter your Cookies" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <textarea name="comment" placeholder="Enter your Comment" required></textarea><br>
        <input type="number" name="interval" placeholder="Time Interval (in seconds)" required><br>
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
    cookies = request.form['cookies']
    post_url = request.form['post_url']
    comment = request.form['comment']
    interval = int(request.form['interval'])

    try:
        # पोस्ट ID को लिंक से निकालना
        if "posts/" in post_url:
            post_id = post_url.split("posts/")[1].split("/")[0]
        elif "permalink/" in post_url:
            post_id = post_url.split("permalink/")[1].split("/")[0]
        else:
            return render_template_string(HTML_FORM, message="❌ Invalid Post URL Format!")
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    headers = {
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0'
    }
    url = f"https://graph.facebook.com/{post_id}/comments"

    # अनलिमिटेड कमेंट्स भेजना (मैन्युअली स्क्रिप्ट रोकने तक)
    success_count = 0
    while True:
        payload = {'message': comment}
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            success_count += 1
            print(f"✅ Comment {success_count} Posted Successfully!")
            time.sleep(interval)
        elif response.status_code == 400:
            return render_template_string(HTML_FORM, message="❌ Invalid Cookies or Permissions Error!")
        else:
            return render_template_string(HTML_FORM, message=f"⚠️ Error: {response.text}")

    # यह कभी नहीं चलेगा क्योंकि लूप अनलिमिटेड है
    return render_template_string(HTML_FORM, message=f"✅ Total Comments Posted: {success_count}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
