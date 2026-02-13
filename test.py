from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

MODEL_PATH = "./model/mt5"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH, local_files_only=True)

summarizer = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

text = """
summarize: India is a diverse country with many languages, cultures,
and traditions. It has a rapidly growing tech industry.
"""

output = summarizer(text, max_length=60, do_sample=False)
print(output[0]["generated_text"])
