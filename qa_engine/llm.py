import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-large"

print("Loading Flan-T5 generative model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.eval()
print("Flan-T5 loaded! ✅")


def clean_context(text):
    text = re.sub(r'[◦▪•●▸▹►◆▷]', ' ', text)
    text = re.sub(r'(POST|GET|PUT|DELETE)\s+/api/\S+', '', text)
    text = re.sub(r'Page No\.\s*\S+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'CCET\s+IPS', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b[ivxlcdm]+\b\.?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\d+\.?\s*$', '', text, flags=re.MULTILINE)
    lines = text.split('\n')
    clean = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line.split()) < 4:
            continue
        if re.match(r'^[\d\s\.\-]+$', line):
            continue
        clean.append(line)
    text = ' '.join(clean)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def generate_answer_with_model(question, context):
    try:
        context = clean_context(context)
        if not context or not question:
            return None

        words = context.split()
        if len(words) > 600:
            context = ' '.join(words[:600])

        # Slightly more directive prompt
        prompt = f"""Question: {question}

Context:
{context}

Provide a clear and concise answer based only on the context. If the context contains a list or bullet points, include them in your answer.
Answer:"""

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=2,
                length_penalty=1.5,          # Encourage longer answers
                repetition_penalty=1.1,      # Discourage repeating tokens
            )

        answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        print(f"Context preview: {context[:200]}...")
        print(f"Flan-T5 answer: {answer[:120]}")

        if not answer or len(answer.split()) < 1:
            return None

        return answer

    except Exception as e:
        print(f"Flan-T5 error: {e}")
        return None