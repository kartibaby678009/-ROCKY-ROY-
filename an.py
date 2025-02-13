from flask import Flask, request
import requests
import time

app = Flask(__name__)

# Facebook Graph API URL (अपना Post ID यहाँ डालें)
FB_POST_URL = "https://graph.facebook.com/v19.0/YOUR_POST_ID/comments"

# Function to Post Comment
def post_comment(cookies, user_agent, comment):
    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "message": comment
    }

    response = requests.post(FB_POST_URL, headers=headers, cookies=cookies, data=data)

    if response.status_code == 200:
        return "✅ Comment Sent Successfully!"
    else:
        return f"❌ Failed to Comment! Error: {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    html_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Auto Comment Tool</title>
    </head>
    <body>
        <h2>Facebook Auto Comment Tool</h2>
        <form method="POST">
            <label>Enter Facebook Cookies (One per line):</label><br>
            <textarea name="cookies" required></textarea><br><br>

            <label>Enter User-Agent:</label><br>
            <input type="text" name="user_agent" value="Mozilla/5.0 (Windows NT 10.0; Win64; x64)" required><br><br>

            <label>Enter Comments (One per line):</label><br>
            <textarea name="comments" required></textarea><br><br>

            <label>Enter Time Interval (Seconds):</label><br>
            <input type="number" name="time_interval" value="400" required><br><br>

            <button type="submit">Submit</button>
        </form>
    """

    if request.method == "POST":
        cookies_text = request.form["cookies"]
        comments_text = request.form["comments"]
        user_agent = request.form["user_agent"]
        time_interval = int(request.form["time_interval"])

        # Cookies और Comments को Process करें
        cookies_list = [cookie.strip() for cookie in cookies_text.split("\n") if cookie.strip()]
        comments_list = [comment.strip() for comment in comments_text.split("\n") if comment.strip()]

        if not cookies_list or not comments_list:
            return html_form + "<h3>❌ Error: Cookies और Comments खाली नहीं होने चाहिए!</h3></body></html>"

        result_logs = ""
        for i, comment in enumerate(comments_list):
            cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies_list[i % len(cookies_list)].split("; ")}
            result = post_comment(cookies, user_agent, comment)

            print(f"[INFO] {result}")  # Render Logs में दिखाने के लिए
            result_logs += f"<p>{result}</p>"
            time.sleep(time_interval)

        return html_form + f"<h3>✅ सभी Comments भेज दिए गए!</h3>{result_logs}</body></html>"

    return html_form + "</body></html>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
