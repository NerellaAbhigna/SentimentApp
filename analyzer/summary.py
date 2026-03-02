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
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def is_meaningful(text):
    """
    Keep only comments that contain at least one alphabet.
    Removes number-only or symbol-only comments like '2026', '100', etc.
    """
    return bool(re.search(r"[a-zA-Z]", text))


def summarize_comments(raw_comments):
    if not raw_comments:
        return "No comments available to summarize."

    # Clean + filter comments properly
    comments = []
    for c in raw_comments:
        cleaned = clean_comment(c)
        if len(cleaned) > 3 and is_meaningful(cleaned):
            comments.append(cleaned)

    if not comments:
        return "Not enough meaningful comments to summarize."

    try:
        embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        # Limit comments for performance
        process_comments = comments[:200]

        embeddings = embedder.encode(
            process_comments,
            convert_to_tensor=True,
            show_progress_bar=False
        )

        num_comments = len(process_comments)
        num_clusters = min(5, max(1, math.ceil(num_comments / 10)))

        if num_comments < num_clusters:
            num_clusters = num_comments

        # Single theme case
        if num_clusters <= 1:
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

        for idxs in clusters.values():
            cluster_embeds = embeddings[idxs]
            centroid = cluster_embeds.mean(dim=0, keepdim=True)
            sims = util.cos_sim(cluster_embeds, centroid)
            best_local_idx = sims.argmax().item()
            best_idx = idxs[best_local_idx]

            representative = process_comments[best_idx].strip()
            if not representative:
                continue  # safety: skip empty representatives

            cluster_data.append({
                "count": len(idxs),
                "representative": representative
            })

        if not cluster_data:
            return "Not enough meaningful opinion clusters found."

        # Sort by frequency
        cluster_data.sort(key=lambda x: x["count"], reverse=True)

        total = sum(c["count"] for c in cluster_data)
        summary_lines = []

        for c in cluster_data[:3]:
            pct = round((c["count"] / total) * 100, 1)
            rep = c["representative"]
            if len(rep) > 100:
                rep = rep[:97] + "..."
            summary_lines.append(f"{pct}%: {rep}")

        return " | ".join(summary_lines)

    except Exception as e:
        print(f"Error in summarization: {e}")
        return "Summary currently unavailable."