import requests
import json
import re
import html
import time

API_ENDPOINT = "https://api.stackexchange.com/2.3/questions"

def clean_html(text):
    modified_text = re.sub(r"<pre.*?</pre>", " ", text, flags=re.DOTALL)
    modified_text = re.sub(r"<[^>]+>", " ", modified_text)
    modified_text = html.unescape(modified_text)

    return modified_text

def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_documents_to_file(documents, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(documents, f,  indent=2)

def document_builder(indexed_doc):
    document = []
    for doc_id, question in indexed_doc:
        doc = {
            "id": doc_id,
            "title": clean_html(question["title"]),
            "text": clean_html(question["body"]),
            "source_id": question["question_id"],
            "link": question["link"]
        }
        document.append(doc)

    return document

def fetch_questions(max_pages):
    all_items = []
    questions_id_set = set()
    for page in range(1, max_pages+1):
        params = {
            "page": page,
            "pagesize": 100,
            "order": "desc",
            "sort": "votes",
            "filter": "withbody",
            "site": "stackoverflow"
        }
        response = requests.get(API_ENDPOINT, params= params, timeout=10)
        questions = response.json()
        if "error_id" in questions:
            print(response.status_code)
            print(questions.get("error_name"), questions.get("error_message"))
            break

        for question in questions["items"]:
            q_id = question.get("question_id")
            if q_id not in questions_id_set:
                questions_id_set.add(q_id)
                all_items.append(question)

        if "backoff" in questions:
            time.sleep(questions["backoff"])

        if not questions["has_more"]:
            return all_items

    return all_items


if __name__ == "__main__":
    all_items = fetch_questions(10)

    filtered_questions = [item for item in all_items if "closed_reason" not in item]
    documents = document_builder(enumerate(filtered_questions, start=1))

    write_documents_to_file(documents, "data_stackoverflow.json")
    print(f"Saved {len(documents)} documents to data_stackoverflow.json.")
