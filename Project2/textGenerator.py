import requests
import gradio as gr
ollama_url="http://localhost:11434/api/generate"

def textGenerator(prompt,word_limit=100,language="English"):
    payload={
        "model":"deepseek-r1:1.5b",
        "prompt":f"Generate the response within {word_limit} word limit for the prompt {prompt} on the language{language}",
        "stream":False,
    }
    response=requests.post(ollama_url,json=payload)
    if response.status_code==200:
        return response.json().get("response","No output generated")
    else:
        return f"Error {response.text}"
    

#Using Gradios for web interface
    
interface=gr.Interface(
    fn=textGenerator,
    inputs=[
        gr.Textbox(lines=3,placeholder="Enter the prompt here"),
        gr.Slider(50,500,step=50,label="Word Limit"),
        gr.Dropdown(
            choices = ["English", "Hindi", "Tamil", "Telugu", "Malayalam", "Kannada", "Bengali", "Marathi", "Gujarati", "Punjabi"],
            value="English",
            label="Choose a language"
        )
    ],
    outputs=gr.Textbox(label="Generated Content"),
    title="AI Powered Text Generator",
    description="Enter the prompt to generate the content of your desired topic."
)

interface.launch()
