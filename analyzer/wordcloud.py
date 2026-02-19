from wordcloud import WordCloud, STOPWORDS
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import os
import re

def generate_wordcloud(comments, output_path):
    """
    Generate and save a WordCloud from a list of comments.
    
    comments: list[str]
    output_path: path to save PNG
    """

    # Combine all comments
    text = " ".join(comments)

    # Clean text
    text = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Handle empty text
    if not text.strip():
        text = "NoWordsFound"

    stopwords = set(STOPWORDS)
    stopwords.update([
        "video","youtube","channel","bro","sir","is","the","a","i","it","to","and","in",
        "that","of","for","on","with","was","this","as","are","subscribe","subscribed",
        "like","likes","liked","share","comment","comments","bhai","anna","akka","madam",
        "guys","friends","first","second","third","reply","replies","watch","watching",
        "watched","content","creator","youtuber","youtubers","love","loved","loving"
    ])

    # Generate wordcloud
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=stopwords,
        min_font_size=10
    ).generate(text)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save WordCloud as image
    wc.to_file(output_path)  # ✅ Use to_file instead of plt to avoid matplotlib issues

    return output_path
