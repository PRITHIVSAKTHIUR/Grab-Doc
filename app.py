from huggingface_hub import InferenceClient
import gradio as gr
from fpdf import FPDF
import docx

css = '''
.gradio-container{max-width: 1000px !important}
h1{text-align:center}
footer {
    visibility: hidden
}
'''

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

# Generate text
def generate(
    prompt, history, system_prompt=None, temperature=0.2, max_new_tokens=1024, top_p=0.95, repetition_penalty=1.0,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt, history, system_prompt)

    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
    output = ""

    for response in stream:
        output += response.token.text
        # Clean up </s> tags from the generated output
        output = output.replace("</s>", "")
        yield output
    return output

# Save the generated content to a file
def save_file(content, filename, file_format):
    if file_format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in content.split("\n"):
            pdf.multi_cell(0, 10, line)
        pdf.output(f"{filename}.pdf")
        return f"{filename}.pdf"
    elif file_format == "docx":
        doc = docx.Document()
        doc.add_paragraph(content)
        doc.save(f"{filename}.docx")
        return f"{filename}.docx"
    elif file_format == "txt":
        with open(f"{filename}.txt", "w") as f:
            f.write(content)
        return f"{filename}.txt"
    else:
        raise ValueError("Unsupported file format")

# Combine generate and save file functions
def generate_and_save(prompt, history, filename="output", file_format="pdf", system_prompt=None, temperature=0.2, max_new_tokens=1024, top_p=0.95, repetition_penalty=1.0):
    generated_text = ""
    for output in generate(prompt, history, system_prompt, temperature, max_new_tokens, top_p, repetition_penalty):
        generated_text = output
    # Ensure </s> tags are removed from the final output
    generated_text = generated_text.replace("</s>", "")
    saved_file = save_file(generated_text, filename, file_format)
    return generated_text, history + [(prompt, generated_text)], saved_file

# Create Gradio interface
demo = gr.Interface(
    fn=generate_and_save,
    inputs=[
        gr.Textbox(placeholder="Type your message here...", label="Chatbot", lines=5),
        gr.State(value=[]),  
        gr.Textbox(placeholder="Filename (default: output)", label="Filename", value="output"),
        gr.Radio(["pdf", "docx", "txt"], label="File Format", value="pdf"),
    ],
    outputs=[
        gr.Textbox(label="Generated Text", lines=5),
        gr.State(value=[]), 
        gr.File(label="Download File")
    ],
    css=css,
    title="GRAB DOC👨🏻‍🚀",
    theme="bethecloud/storj_theme"
)

demo.queue().launch(show_api=False)