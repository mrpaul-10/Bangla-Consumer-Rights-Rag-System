"""
Handles LLM prompt construction and answer generation (Google Gemini).
"""

import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """তুমি একজন সহায়ক আইনি সহকারী, যে শুধুমাত্র প্রদত্ত ভোক্তা অধিকার সংরক্ষণ আইন, ২০০৯ এর তথ্যের ভিত্তিতে উত্তর দাও।

নিয়ম:
1. শুধুমাত্র নিচে দেওয়া প্রাসঙ্গিক অংশ (context) ব্যবহার করে উত্তর দাও।
2. উত্তরের শেষে কোন ধারা থেকে তথ্য নেওয়া হয়েছে তা উল্লেখ করো।
3. যদি প্রদত্ত তথ্যে উত্তর না থাকে, স্পষ্টভাবে বলো "দুঃখিত, এই তথ্য আইনের প্রদত্ত অংশে পাওয়া যায়নি। এটি সম্ভবত এই আইনের আওতার বাইরের একটি বিষয়।"
4. এটি আইনি পরামর্শ নয় — জটিল বিষয়ে আইনজীবীর পরামর্শ নেওয়ার কথা মনে করিয়ে দাও।
"""

# The model name for Google Gemini-2.5 Flash is defined here.
MODEL_NAME = "gemini-3.1-flash-lite"


def _build_prompt(query: str, context_chunks: list[dict]) -> str:
    context_text = "\n\n".join(
        f"[{c['section']}]\n{c['content']}" for c in context_chunks
    )
    return f"{SYSTEM_PROMPT}\n\nপ্রাসঙ্গিক তথ্য:\n{context_text}\n\nপ্রশ্ন: {query}\n\nউত্তর:"


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    import time
    from google import genai
    from google.genai.errors import ServerError

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = _build_prompt(query, context_chunks)

    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            return response.text
        except ServerError as e:
            if attempt == max_retries:
                raise
            wait_time = 10 * attempt  # 10s, 20s, 30s, 40s, 50s
            print(f"  [Server busy, retry {attempt}/{max_retries} in {wait_time}s...]")
            time.sleep(wait_time)

# print("API Key loaded:", os.getenv("GOOGLE_API_KEY")[:10] + "..." if os.getenv("GOOGLE_API_KEY") else "NOT FOUND")
if __name__ == "__main__":
    sample_chunks = [
        {"section": "ধারা ৬০", "content": "কোন ব্যক্তি, কারণ উদ্ভব হইবার ৩০ দিনের মধ্যে এই আইনের অধীন ভোক্তা-অধিকার বিরোধী কার্য সম্পর্কে মহাপরিচালক কিংবা অধিদপ্তরের ক্ষমতাপ্রাপ্ত কর্মকর্তার নিকট লিখিতভাবে অভিযোগ দায়ের করিতে পারিবেন।"},
    ]
    answer = generate_answer("অভিযোগ কীভাবে দায়ের করতে হয়?", sample_chunks)
    print(answer)