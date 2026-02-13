from unittest import result
from analyzer.fetch_comments import fetch_comments_all
from analyzer.sentiment import predict_sentiment
from analyzer.save_result import save_to_csv
from analyzer.summary import summarize_comments
from analyzer.wordcloud import generate_wordcloud
def analyze_video(video_id):
    """
    Full pipeline:
    video_id -> comments -> sentiment results
    """

    # 1. Fetch comments
    comments = fetch_comments_all(video_id)

    if not comments:
        return {
            "results": [],
            "summary": "No comments found.",
            "wordcloud_path": None
        }

    # 2. Predict sentiment
    results = predict_sentiment(comments)
    # 3. Get dominant sentiment
    
    summary = summarize_comments(comments)
    wc_path = "static/wordclouds/comments_wc.png"
    generate_wordcloud(comments, wc_path)

    save_to_csv(results)
    return {
    "results": results,
    "summary": summary,
    "wordcloud_path": wc_path,
    
}

