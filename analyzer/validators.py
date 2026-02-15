import re

def extract_video_id(input_string):
    """
    Extract video ID from various YouTube URL formats or validate a direct video ID.
    
    Supported URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID&feature=...
    
    Args:
        input_string (str): YouTube URL or video ID
        
    Returns:
        str: YouTube video ID if valid, None otherwise
    """
    if not input_string:
        return None
    
    input_string = input_string.strip()
    
    # If it's already a valid 11-character video ID (alphanumeric)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', input_string):
        return input_string
    
    # Pattern to extract video ID from various YouTube URL formats
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_string)
        if match:
            return match.group(1)
    
    return None


def is_valid_video_id(video_id):
    """
    Validate if the given string is a valid YouTube video ID.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not video_id:
        return False
    
    # YouTube video IDs are exactly 11 characters, containing letters, numbers, underscores, and hyphens
    return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))


def validate_input(video_id):
    """
    Validate and process video_id input from user.
    
    Args:
        video_id (str): User input (could be video ID or URL)
        
    Returns:
        tuple: (is_valid, video_id_or_error_message)
    """
    # Check if empty or None
    if not video_id or not video_id.strip():
        return (False, "Please enter a YouTube Video ID or URL.")
    
    # Try to extract video ID from URL or validate direct video ID
    extracted_id = extract_video_id(video_id)
    
    if extracted_id is None:
        return (False, "Invalid YouTube URL or Video ID. Please enter a valid YouTube video URL or 11-character video ID.")
    
    return (True, extracted_id)
