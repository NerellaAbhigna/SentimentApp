import os
from flask import Flask, render_template, request, send_from_directory
from analyzer.pipeline import analyze_video
from analyzer.summary import summarize_comments
from analyzer.validators import validate_input

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
        video_id_input = request.form.get("video_id")

        # 1. Validate input (empty, invalid format, or extract video_id from URL)
        is_valid, video_id_or_error = validate_input(video_id_input)
        
        if not is_valid:
            error = video_id_or_error
        else:
            video_id = video_id_or_error
            try:
                output = analyze_video(video_id)
                results = output.get("results", [])
                summary = output.get("summary")
                wc_path = output.get("wordcloud_path")
                
                # Check for error returned from pipeline
                pipeline_error = output.get("error")
                
                if pipeline_error:
                    error = pipeline_error
                elif not results:
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
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)
    app.run(debug=True)
