from wordcloud import WordCloud, STOPWORDS
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import os
import re

def generate_wordcloud(comments, output_path):
    """
    comments: list[str]
    output_path: path to save PNG
    """

    # Combine all comments
    text = " ".join(comments)

    # Extra cleaning (important for messy YouTube data)
    text = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    if not text.strip():
        # Create a dummy wordcloud if no text is available
        text = "NoWordsFound"

    stopwords = set(STOPWORDS)
    stopwords.update(["video", "youtube", "channel", "bro", "sir","is","the","a","i","it","to","and","in","that","of","for","on","with","was","this","as","are","video","videos","channel","subscribe","subscribed",
    "like","likes","liked","share","comment","comments",
    "bro","bhai","anna","akka","sir","madam","guys","friends",
    "first","second","third","reply","replies",
    "watch","watching","watched",
    "content","creator","youtuber","youtubers",
    "love","loved","loving",])

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=stopwords,
        min_font_size=10
    ).generate(text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path
