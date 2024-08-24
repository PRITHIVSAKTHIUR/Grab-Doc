---
title: GRAB DOC
emoji: 👨🏻‍🚀
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.41.0
app_file: app.py
pinned: false
license: creativeml-openrail-m
short_description: pdf, docx, txt
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## Model Details

| Model Identifier              | Description                                     | Version |
|-------------------------------|-------------------------------------------------|---------|
| `mistralai/Mistral-7B-Instruct-v0.3` | A large language model fine-tuned for instruction-based tasks. | 0.3     |


![alt text](assets/AAD.png)

## HTTPS

    Make sure you have git-lfs installed (https://git-lfs.com)
    
    git lfs install
    
    git clone https://huggingface.co/spaces/prithivMLmods/GRAB-DOC
    
    If you want to clone without large files - just their pointers
    
    GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/spaces/prithivMLmods/GRAB

## SSH

    Make sure you have git-lfs installed (https://git-lfs.com)
    
    git lfs install
    
    git clone git@hf.co:spaces/prithivMLmods/GRAB-DOC
    
    If you want to clone without large files - just their pointers
    
    GIT_LFS_SKIP_SMUDGE=1 git clone git@hf.co:spaces/prithivMLmods/GRAB-DOC
    
## Inference-Client

```python
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3")

def format_prompt(message, history, system_prompt=None):
    prompt = "<s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    if system_prompt:
        prompt += f"[SYS] {system_prompt} [/SYS]"
    prompt += f"[INST] {message} [/INST]"
    return prompt
```

## DEMO GIF

![alt text](assets/GD.gif)

## Dependencies

| Package            | Version     | Description                                         |
|--------------------|-------------|-----------------------------------------------------|
| `gradio`           | Latest      | A library for building machine learning demos and applications. |
| `fpdf`             | Latest      | A Python class for generating PDF documents.       |
| `python-docx`      | Latest      | A library for creating and updating Microsoft Word (.docx) files. |
| `huggingface-hub`  | 0.24.6      | A library for interacting with the Hugging Face Hub to manage and share machine learning models and datasets. |

.

.

.@prithivmlmods

### **Try It Out!**
| Hugging Face | [prithivMLmods](https://huggingface.co/prithivMLmods) |
