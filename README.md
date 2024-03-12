# Dataset Creation and Fine-Tuning Notebook for IndicTrans2 Models

## Introduction

This repository contains resources for creating a dataset required for fine-tuning **AI4Bharat**'s [IndicTrans2](https://ai4bharat.iitm.ac.in/indic-trans2/), an existing open-source translation model. Additionally, it includes a notebook for fine-tuning the model using Google Colab.

While the model is already impressive at translating English text to Hindi, it lacks attention to fine details, especially when it comes to conversational inputs. It is noticeable that the model predominantly produces output from a male perspective.

The goal is to fine-tune the model to capture more information from conversational inputs and generate appropriate output.

> As a Hindi and English speaker, this repository is centered around Hindi but should also work for other Indic languages that model supports.

## Dataset Creation

To create the dataset for fine-tuning, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/saurabhv749/indictrans2-finetune
   cd indictrans2-finetune
   ```

2. **Configuration**: We will use the `Anyscale` API for text generation. Obtain your API key by visiting the [Credentials Page](https://app.endpoints.anyscale.com/credentials) and paste it into `dataset/config.yaml`. If your target language is other than Hindi, please change `tgt_lang` accordingly. I'm using `Mixtral-8x7B-Instruct-v0.1`, but you can use any model listed [here](https://docs.endpoints.anyscale.com/).

3. **Generate Data**: We will use a LLM to generate some conversational data for us to start with. First, add topics to `dataset/src/topics` to generate conversations around those topics.

   Generate conversation data by running:

   ```
   python generate.py
   ```

4. **Preprocessing**: The generated conversations will be in the file `dataset/src/samples.txt`. Clean it so that **every line contains a dialogue**. Also, take special care of **quotation marks**.

5. **Translate**: Once you're done with formatting `dataset/src/samples.txt`, run

   ```
   python translate.py
   ```

   to create translated text along with the original sentences.

6. **Fix Translations**: Yes, more manual work. Correct translations, but don't mess with the **spacing/new lines**.

7. **Create Dataset**: Finally, run

   ```
   python create_dataset.py
   ```

   to create a zip file with data in the required folder structure.

## Fine-Tuning Notebook

The `indictrans2-finetune.ipynb` contains a Google Colab notebook for fine-tuning the translation model using the created `en-indic-exp.zip`. Follow the instructions within the notebook to:

- Open the notebook in Colab.
- Upload `en-indic-exp.zip`.
- Extract the zip file.
- Fine-tune the model.

## Pre-trained LoRA

[sam749/IndicTrans2-Conv](https://huggingface.co/sam749/IndicTrans2-Conv)
