from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
#API_KEY = os.environ.get("API_KEY_VALUE")
API_KEY= "AIzaSyAGs3__UuQ8xtxKSLU0-buqxzK4aJ2i760"

class VideoError(Exception):
    """Custom exception for video-related errors"""
    pass

class QuotaExceededError(VideoError):
    """Raised when API quota is exceeded"""
    pass

class VideoNotFoundError(VideoError):
    """Raised when video is not found"""
    pass

class CommentsDisabledError(VideoError):
    """Raised when comments are disabled for a video"""
    pass

class InvalidVideoIDError(VideoError):
    """Raised when video ID is invalid"""
    pass


def fetch_comments_all(video_id):
    """
    Fetch ALL top-level comments from a YouTube video.

    Args:
        video_id (str): YouTube video ID

    Returns:
        list: List of comment texts
        
    Raises:
        QuotaExceededError: When API quota is exceeded
        VideoNotFoundError: When video doesn't exist
        CommentsDisabledError: When comments are disabled
        InvalidVideoIDError: When video ID is invalid
    """

    youtube = build(
        "youtube",
        "v3",
        developerKey=API_KEY
    )

    comments = []
    next_page_token = None

    try:
        # First, verify the video exists and get its details
        video_request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        video_response = video_request.execute()
        
        # Check if video exists
        if not video_response.get("items"):
            raise VideoNotFoundError("Video not found. The video may have been deleted or the ID is incorrect.")
        
        video_info = video_response["items"][0]
        
        # Check if comments are disabled
        # YouTube returns commentCount=0 when comments are disabled
        statistics = video_info.get("statistics", {})
        comment_count = int(statistics.get("commentCount", 0))
        
        if comment_count == 0:
            # Comments might be disabled, let's try to fetch anyway to confirm
            pass
        
    except HttpError as e:
        error_details = e.error_details if hasattr(e, 'error_details') else str(e)
        error_code = e.resp.status
        
        if error_code == 404:
            raise VideoNotFoundError("Video not found. The video may have been deleted or the ID is incorrect.")
        elif error_code == 403:
            # Check if it's quota exceeded or comment disabled
            if "quotaExceeded" in str(error_details).lower() or "quota" in str(error_details).lower():
                raise QuotaExceededError("API quota exceeded. Please try again later.")
            else:
                raise CommentsDisabledError("Comments are disabled for this video.")
        elif error_code == 400:
            raise InvalidVideoIDError("Invalid video ID. Please check the video ID and try again.")
        else:
            raise VideoError(f"YouTube API error: {error_details}")

    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )

            response = request.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            # Move to next page
            next_page_token = response.get("nextPageToken")

            # No more pages → stop
            if not next_page_token:
                break

    except HttpError as e:
        error_code = e.resp.status
        error_details = e.error_details if hasattr(e, 'error_details') else str(e)
        
        if error_code == 403:
            if "quotaExceeded" in str(error_details).lower() or "quota" in str(error_details).lower():
                raise QuotaExceededError("API quota exceeded. Please try again later.")
            else:
                raise CommentsDisabledError("Comments are disabled for this video. Cannot retrieve comments.")
        elif error_code == 404:
            raise VideoNotFoundError("Video not found. The video may have been deleted.")
        elif error_code == 400:
            raise InvalidVideoIDError("Invalid video ID format.")
        else:
            raise VideoError(f"Error fetching comments: {error_details}")
    
    return comments
