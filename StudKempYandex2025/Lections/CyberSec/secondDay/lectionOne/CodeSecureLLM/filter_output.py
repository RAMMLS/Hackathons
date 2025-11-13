from transformers import pipline

toxicity_classifier = pipline("text-classification", model = "unitary/toxic-bert")

def filter_output(text: str) -> bool:
    result = toxicity_classifier(text)[0]

    return result["label"] == ["toxic"]

response = llm.generate("Ненавижу людей")
if filter_output(response):
    print("Ответ заблокирован из-за токсичности")
else:
    print(response)
