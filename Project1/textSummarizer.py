import requests
import gradio as gr
import docx
import PyPDF2

ollama_URL="http://localhost:11434/api/generate"

def extract_text_of_file(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".docx"):
        doc=docx.Document(file)
        text=[]
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
    elif file.name.endswith(".pdf"):
        reader=PyPDF2.PdfReader(file)
        text=[]
        for page in reader.pages:
            page_text=page.extract_text()
            if page_text:
                text.append(page_text)
        return " ".join(text)

    else:
        return "Unsupported File Type"

    
def text_summarizer(text,summaryType,file):

    #Handle the text if file is uploaded
    if file is not None:
        text=extract_text_of_file(file)
    if not text.strip():
        return "Please enter the text or upload a file to generate a summary."
    
    #Handle the summary type
    if summaryType == "One Line Summary":
        prompt = f"Summarize the following text in one line: {text}"
    elif summaryType == "Three Line Summary":
        prompt = f"Summarize the following text in three lines: {text}"
    elif summaryType == "Summary in Bullet Points":
        prompt = f"Summarize the following text as bullet points: {text}"
    elif summaryType == "General Summary in Paragraph":
        prompt = f"Summarize the following text in a paragraph: {text}"
    else:
        prompt = f"Summarize the following text: {text}"


    payload= {
        "model":"deepseek-r1:1.5b",
        "prompt":f"Summarize the following text given below: {text}",
        "stream":False
    }

    response=requests.post(ollama_URL,json=payload)

    if(response.status_code==200):
        return response.json().get("response","No output generated")
    else:
        return f"Error: {response.text}"

interface=gr.Interface(
    fn=text_summarizer,
    inputs=[
        gr.Textbox(lines=10,placeholder="Enter the text to summarize"),
        gr.Dropdown(
            choices=["One Line Summary","Three Line Summary","Summary in Bullet Points","General Summary in Paragraph"],
            value="General Summary in Paragraph",
            label="Select Summary Type"
        ),
        gr.File(
            label="Upload File (Optional)",
            file_types=[".txt",".pdf",".docx"]
        )
        ],
    outputs=gr.Textbox(label="Summary"),
    title="AI Powered Summarizer",
    description="Enter the text that you want a summary on, then Deepseek will help you summarize."
)

if __name__ == "__main__":
    interface.launch()
#Testing the function

#text="Artificial Intelligence (AI) is a branch of computer science that focuses on building systems capable of performing tasks that usually require human intelligence.These tasks include learning, reasoning, problem-solving, and understanding natural language."
#print(text_summarizer(text))
