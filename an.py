from flask import Flask, request, render_template_string, jsonify
import requests
import time

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Created by Raghu ACC Rullx Boy</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial; }
        input, textarea { width: 80%; padding: 10px; margin: 10px; border-radius: 5px; border: none; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px; }
        button:hover { background-color: darkgreen; }
    </style>
</head>
<body>
    <h1>Created by Raghu ACC Rullx Boy</h1>
    <form method="POST" action="/submit">
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <textarea name="comment" placeholder="Enter Your Comment" required></textarea><br>
        <input type="text" name="cookies" placeholder="Enter Cookies" required><br>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 5)" required><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    post_url = request.form['post_url']
    comment = request.form['comment']
    cookies = request.form['cookies']
    interval = int(request.form['interval'])

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Cookie': cookies
    }
    
    try:
        post_id = post_url.split('posts/')[1].split('/')[0]
        comment_url = f"https://graph.facebook.com/v17.0/{post_id}/comments"

        while True:
            response = requests.post(comment_url, headers=headers, data={'message': comment})
            
            if response.status_code == 200:
                return jsonify({'status': 'Success', 'message': 'Comment posted successfully!'})
            elif response.status_code == 400:
                return jsonify({'status': 'Error', 'message': 'Invalid Cookies or Post URL!'})
            else:
                return jsonify({'status': 'Error', 'message': f'Error: {response.text}'})
            
            time.sleep(interval)

    except Exception as e:
        return jsonify({'status': 'Error', 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
