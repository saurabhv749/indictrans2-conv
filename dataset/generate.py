import requests
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    api_base = config["api_base"]
    model = config["model"]
    token = config["anyscale_api_credential"]
    topics_file = config["topics_file"]
    samples_file = config["samples_file"]
    # Get yours from here: https://app.endpoints.anyscale.com/credentials

s = requests.Session()
url = f"{api_base}/chat/completions"
temperature = 0.7


def create_examples(topic):
    prompt = """You will be provided with a word, and your task will be to generate sentences using that word. The following is the template for the response:
    
    - a paragraph using the word
    - a male's dialogue using the word
    - a female's dialogue using the word
    - {MALE_NAME} talking to {MALE_NAME} dialogue using the word
    - {MALE_NAME} talking to {FEMALE_NAME} dialogue using the word
    - {FEMALE_NAME} talking to {MALE_NAME}  dialogue using the word
    - {FEMALE_NAME} talking to {FEMALE_NAME} dialogue using the word

    """
    prompt += f"let's start with '{topic}'."

    body = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an award winning expert in script writing.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }

    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        response = resp.json()
        message = response["choices"][0]["message"]
        return message["content"]


if __name__ == "__main__":
    topics = open(topics_file, "r", encoding="utf8").read().split("\n")

    # Opening samples.txt as 'append' so that we only need to update the list of 'topics'
    with open(samples_file, "a") as file:
        for idx, topic in enumerate(topics, start=1):
            print(f" {topic} - {idx} /  {len(topics)}")
            sample = create_examples(topic)
            file.write(sample)
            file.write("\n\n")
        print(f"✅ Generation done!")
