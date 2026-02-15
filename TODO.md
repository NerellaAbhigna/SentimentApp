# TODO: Handle video_id Error Cases

## Error Cases to Handle:
1. ✅ Empty video_id
2. ✅ Invalid video_id  
3. ✅ Input complete URL instead of video_id
4. ✅ API Quota exceeded
5. ✅ Video not found
6. ✅ Empty comments and videos with comments disabled

## Implementation Plan:

### Step 1: Create a video_id validator utility (analyzer/validators.py)
- Function to check if video_id is empty/None
- Function to extract video_id from various YouTube URL formats
- Function to validate video_id format (11 characters, alphanumeric)

### Step 2: Update app.py
- Add input validation before calling analyze_video
- Extract video_id from URL if user enters full URL
- Handle empty video_id with appropriate error message

### Step 3: Update analyzer/fetch_comments.py
- Handle Google API errors:
  - Quota exceeded (HttpError 403)
  - Video not found (HttpError 404)  
  - Comments disabled (HttpError 400 or empty response)
  - Invalid video_id (HttpError 400)
- Return meaningful error messages instead of crashing

### Step 4: Update analyzer/pipeline.py
- Catch specific exceptions from fetch_comments
- Return appropriate error messages

## Files to Edit:
1. `analyzer/validators.py` - NEW FILE - video_id validation utilities
2. `app.py` - Add input validation
3. `analyzer/fetch_comments.py` - Handle API errors
4. `analyzer/pipeline.py` - Handle errors from fetch_comments

## Followup Steps:
- Test each error case to ensure proper handling
- Verify error messages are user-friendly
