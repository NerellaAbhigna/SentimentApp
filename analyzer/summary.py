import re
import math
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import KMeans

def clean_comment(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Basic emoji/symbol removal using regex since emoji library might not be present
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def summarize_comments(raw_comments):
    if not raw_comments:
        return "No comments available to summarize."

    # Filter out empty or very short comments
    comments = [clean_comment(c) for c in raw_comments if len(str(c).strip()) > 3]
    
    if not comments:
        return "Not enough meaningful comments to summarize."

    try:
        # Load model - this might take a moment the first time
        embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        
        # Limit to first 100 comments for performance if needed, 
        # but let's try with what we have first.
        process_comments = comments[:200] 
        
        embeddings = embedder.encode(
            process_comments,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        
        num_comments = len(process_comments)
        # Aim for a reasonable number of clusters based on comment count
        num_clusters = min(5, max(1, math.ceil(num_comments / 10)))
        
        if num_comments < num_clusters:
            num_clusters = num_comments

        if num_clusters <= 1:
            # If only one cluster or very few comments, just return the most representative one
            centroid = embeddings.mean(dim=0, keepdim=True)
            sims = util.cos_sim(embeddings, centroid)
            best_idx = sims.argmax()
            return f"Common theme: {process_comments[best_idx]}"

        kmeans = KMeans(
            n_clusters=num_clusters,
            random_state=42,
            n_init=10
        )

        labels = kmeans.fit_predict(embeddings.cpu().numpy())
        clusters = defaultdict(list)
        for idx, label in enumerate(labels):
            clusters[label].append(idx)

        cluster_data = []
        for label, idxs in clusters.items():
            cluster_embeds = embeddings[idxs]
            centroid = cluster_embeds.mean(dim=0, keepdim=True)
            sims = util.cos_sim(cluster_embeds, centroid)
            best_idx = idxs[sims.argmax()]

            cluster_data.append({
                "count": len(idxs),
                "representative": process_comments[best_idx]
            })

        # Sort by most frequent themes
        cluster_data.sort(key=lambda x: x["count"], reverse=True)
        
        summary_lines = []
        total = sum(c["count"] for c in cluster_data)
        # Return top 3 themes
        for c in cluster_data[:3]:
            pct = round((c["count"] / total) * 100, 1)
            summary_lines.append(f"{pct}%: {c['representative']}")
        
        return " | ".join(summary_lines)

    except Exception as e:
        print(f"Error in summarization: {e}")
        return "Summary currently unavailable."
