from unittest import result
from analyzer.fetch_comments import fetch_comments_all
from analyzer.fetch_comments import (
    VideoError, 
    QuotaExceededError, 
    VideoNotFoundError, 
    CommentsDisabledError,
    InvalidVideoIDError
)
from analyzer.sentiment import predict_sentiment
from analyzer.save_result import save_to_csv
from analyzer.summary import summarize_comments
from analyzer.wordcloud import generate_wordcloud


def analyze_video(video_id):
    """
    Full pipeline:
    video_id -> comments -> sentiment results
    
    Returns:
        dict: Results dictionary with sentiment analysis data
              OR error information if something goes wrong
    """

    # 1. Fetch comments - with proper error handling
    try:
        comments = fetch_comments_all(video_id)
    except QuotaExceededError as e:
        return {
            "results": [],
            "summary": None,
            "wordcloud_path": None,
            "error": str(e),
            "error_type": "quota_exceeded"
        }
    except VideoNotFoundError as e:
        return {
            "results": [],
            "summary": None,
            "wordcloud_path": None,
            "error": str(e),
            "error_type": "video_not_found"
        }
    except CommentsDisabledError as e:
        return {
            "results": [],
            "summary": None,
            "wordcloud_path": None,
            "error": str(e),
            "error_type": "comments_disabled"
        }
    except InvalidVideoIDError as e:
        return {
            "results": [],
            "summary": None,
            "wordcloud_path": None,
            "error": str(e),
            "error_type": "invalid_video_id"
        }
    except VideoError as e:
        return {
            "results": [],
            "summary": None,
            "wordcloud_path": None,
            "error": str(e),
            "error_type": "video_error"
        }
    except Exception as e:
        return {
            "results": [],
            "summary": None,
            "wordcloud_path": None,
            "error": f"An unexpected error occurred: {str(e)}",
            "error_type": "unexpected_error"
        }

    # Check if comments list is empty
    if not comments:
        return {
            "results": [],
            "summary": "No comments found. The video may have no comments or comments are disabled.",
            "wordcloud_path": None,
            "error": "No comments found or comments are disabled.",
            "error_type": "no_comments"
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
        "error": None,
        "error_type": None
    }
