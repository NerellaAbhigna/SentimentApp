**YouTube Comments Sentiment Analyzer**

**Overview**

The **YouTube Comments Sentiment Analyzer** is a machine learning-based application that analyzes user comments and classifies them into **Positive**, **Negative**, or **Neutral** sentiments.

This project is designed to help understand audience opinions by transforming unstructured text data into meaningful insights using **Natural Language Processing (NLP)** techniques.

**Objective**

* To analyze large volumes of YouTube comments efficiently
* To classify sentiments accurately using machine learning
* To provide insights into audience perception of content

**Key Features**

* ✔️ Text preprocessing and cleaning
* ✔️ Sentiment classification (Positive / Neutral / Negative)
* ✔️ Handles real-world noisy data (emojis, slang, mixed language)
* ✔️ Simple and modular code structure
* ✔️ Easy to extend for real-time applications

**Tech Stack**

* **Programming Language:** Python
* **Libraries:** Pandas, NumPy, Scikit-learn
* **NLP Techniques:** Text preprocessing, Tokenization, Vectorization (TF-IDF)
* **Model:** Machine Learning classification model

 **System Workflow**

1. **Data Collection**

   * Input comments (dataset or extracted from sources)

2. **Data Preprocessing**

   * Removing noise (punctuation, stopwords, special characters)
   * Text normalization

3. **Feature Extraction**

   * Converting text into numerical representation using TF-IDF

4. **Model Training**

   * Training a machine learning model on labeled data

5. **Prediction**

   * Classifying new comments into:

     * Positive 😊
     * Neutral 😐
     * Negative 😠

**Project Structure**

bash
SentimentApp/
│
├── data/                 # Dataset containing YouTube comments
├── model/                # Trained model files
├── src/                  # Core logic
│   ├── preprocessing.py
│   ├── training.py
│   ├── prediction.py
│
├── app.py                # Entry point of the application
├── requirements.txt      # Project dependencies
└── README.md             # Documentation

**Installation & Setup**

**Step 1:** Clone the Repository
bash
git clone https://github.com/NerellaAbhigna/SentimentApp.git
cd SentimentApp
**Step 2:** Install Dependencies
bash
pip install -r requirements.txt
**Step 3:** Run the Application
`bash
python app.py

**Sample Output**

| Comment                    | Predicted Sentiment |
| -------------------------- | ------------------- |
| "This video is amazing!"   | Positive            |
| "Not useful at all"        | Negative            |
| "It’s okay, nothing great" | Neutral             |

**Applications**
* Social media sentiment analysis
* Product and service feedback evaluation
* Content performance analysis
* Public opinion mining

**Future Scope**
* Integration with YouTube Data API for real-time comments
* Implementation of deep learning models (LSTM, BERT)
* Deployment as a web application
* Multi-language sentiment support
