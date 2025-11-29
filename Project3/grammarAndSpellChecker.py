import requests
import gradio as gr

# Ollama local server URL
ollama_url = "http://localhost:11434/api/generate"

def correct_grammer_and_spell(text):
    # Prompt given to the model (instruction only)
    prompt =  f"Correct the grammar and spelling in the following text and provide explanations:\n{text}"

    # Data sent to the Ollama model
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "thinking": False   # Disable the AI thinking output
        }
    }

    # Sending request to the Ollama API
    response = requests.post(ollama_url, json=payload)

    # If request was successful, return model output
    if response.status_code == 200:
        return response.json().get("response", "No output generated")
    else:
        return f"Error {response.text}"


# Creating the Gradio UI
interface = gr.Interface(
    fn=correct_grammer_and_spell,  # Function to run
    inputs=gr.Textbox(lines=5, placeholder="Enter the text to correct grammar and spelling mistakes"),
    outputs=gr.Textbox(lines=10,label="Corrected Text"),
    title="AI Powered Grammar and Spell Checker",
    description="Enter the text with grammatical and spelling errors and Deepseek AI will correct them!"
)

# Start the Gradio app
interface.launch()
