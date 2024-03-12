# ----------------------------------------------
# First make necessory changes to  `src/samples-translated.txt`
# before running `create_dataset.py`
# ------------------------------------------------

import os
import zipfile
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    src_lang = config["src_lang"]
    tgt_lang = config["tgt_lang"]
    samples_translate_file = config["samples_translate_file"]
    dataset_dir = config["custom_dataset"]
    # create dataset folder
    os.makedirs(dataset_dir, exist_ok=True)


def zip_folder(folder_path):
    zip_file_path = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_file_path, mode="w") as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file), os.path.join(folder_path, "..")
                    ),
                )

    print(f"✅ Dataset created: {zip_file_path}")


def write_data_split(data, split):
    data_dir = f"{dataset_dir}/{split}/{src_lang}-{tgt_lang}"
    os.makedirs(data_dir, exist_ok=True)

    src_file_path = f"{data_dir}/{split}.{src_lang}"
    tgt_file_path = f"{data_dir}/{split}.{tgt_lang}"

    src_file = open(src_file_path, "w+", encoding="utf8")
    tgt_file = open(tgt_file_path, "w+", encoding="utf8")

    for idx, tr in enumerate(data, start=1):
        lines = tr.splitlines()
        if len(lines) > 1:
            lines = lines[-2:]
            orginal, translated = lines[0], lines[1]
            src_file.write(orginal.strip())
            tgt_file.write(translated.strip())
            if idx != len(data):
                src_file.write("\n")
                tgt_file.write("\n")

    src_file.close()
    tgt_file.close()


def seperate_data_files(src_file, dev_ratio=0.1):
    # read translated data
    content = open(src_file, encoding="utf8").read()
    translations = content.split("\n\n")

    # create data split
    split_index = int(len(translations) * (1.0 - dev_ratio))
    train_data, test_data = translations[:split_index], translations[split_index:]
    print("Train Examples:", len(train_data))
    print("Test Examples:", len(test_data))

    # write split
    write_data_split(train_data, "train")
    write_data_split(test_data, "dev")
    print("✅ Created Dataset Files.")

    # create zip of dataset
    zip_folder(dataset_dir)


if __name__ == "__main__":
    seperate_data_files(samples_translate_file)
