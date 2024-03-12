# ----------------------------------------------
# First edit `src/samples.txt` file so that very line
# is a dialogue before running `translate.py`
# ------------------------------------------------

import requests
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    samples_file = config["samples_file"]
    samples_translate_file = config["samples_translate_file"]

url = "https://demo-api.models.ai4bharat.org/inference/translation/v2"
payload = {
    "controlConfig": {"dataTracking": True},
    "input": [],
    "config": {
        "serviceId": "",
        "language": {"sourceLanguage": "en", "targetLanguage": "hi"},
    },
}


def eng2hin_api(inputs):
    inputs = [{"source": i} for i in inputs]
    payload["input"] = inputs

    while True:
        response = requests.post(url, json=payload)
        resp_data = response.json()
        if "output" in resp_data:
            break

    results = []
    for output in resp_data["output"]:
        results.append(output["target"])

    return results


if __name__ == "__main__":
    with open(samples_file, "r", encoding="utf8") as ifile:
        examples = ifile.readlines()
        print(f"Number of examples: {len(examples)}")
        translations = []
        ifile.close()

        batch_size = 8

        for idx in range(0, len(examples), batch_size):
            print(idx, idx + batch_size)
            samples = examples[idx : idx + batch_size]
            translations += eng2hin_api(samples)

        # create paired text
        with open(samples_translate_file, "w+", encoding="utf8") as ofile:
            for idx, translation_data in enumerate(
                zip(examples, translations), start=1
            ):
                sentence, translation = translation_data[0], translation_data[1]
                ofile.write(f"{sentence.strip()}\n{translation.strip()}")
                if idx != len(examples):
                    ofile.write("\n\n")
            ofile.close()
