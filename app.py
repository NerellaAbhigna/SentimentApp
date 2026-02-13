import os
from flask import Flask, render_template, request, send_from_directory
from analyzer.pipeline import analyze_video
from analyzer.summary import summarize_comments
app = Flask(__name__)

@app.route("/download")
def download_file():
    return send_from_directory("data", "results.csv", as_attachment=True)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    sentiment_counts = {}
    error = None
    summary = None
    majority_sentiment = None
    wc_path = None

    if request.method == "POST":
        video_id = request.form.get("video_id")

        try:
            output = analyze_video(video_id)
            results = output.get("results", [])
            summary = output.get("summary")
            wc_path = output.get("wordcloud_path")

            if not results:
                error = "No comments found or comments are disabled."
            else:
                sentiment_counts = {
                    "Positive": sum(1 for r in results if r["sentiment"] == "Positive"),
                    "Neutral": sum(1 for r in results if r["sentiment"] == "Neutral"),
                    "Negative": sum(1 for r in results if r["sentiment"] == "Negative"),
                }
                majority_sentiment = max(sentiment_counts, key=sentiment_counts.get)
                

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        results=results,
        sentiment_counts=sentiment_counts,
        majority_sentiment=majority_sentiment,
        summary=summary,
        wc_path=wc_path,
        error=error
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    #app.run(debug=True)