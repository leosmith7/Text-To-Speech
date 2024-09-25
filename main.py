import tkinter as tk
from tkinter import filedialog
import requests
import PyPDF2
import os

API_KEY = os.getenv('API_KEY')

class PDFToSpeechApp:
    def __init__(self, window):
        self.window = window
        window.title("PDF to Speech Converter")
        window.minsize(width=300, height=200)
        self.select_button = tk.Button(window, text="Select PDF", command=self.select_pdf)
        self.select_button.pack(expand=True)

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            text = self.extract_text_from_pdf(file_path)
            audio_data = self.text_to_speech(text)
            if audio_data:
                self.save_audio(audio_data)

    def extract_text_from_pdf(self, file_path):
        combined_text = ''
        if file_path:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    combined_text += page.extract_text() + ' '
        return combined_text

    def text_to_speech(self, text):
        response = requests.get(f'https://api.voicerss.org/?key={API_KEY}&src={text}&hl=en-us&c=WAV')
        if response.status_code == 200 and response.content:
            print(response.content)
            return response.content

        else:
            print("Error:", response.status_code)
            return None

    def save_audio(self, audio_data):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if file_path:
            with open(file_path, 'wb') as audio_file:
                audio_file.write(audio_data)
            print(f"Audio saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToSpeechApp(root)
    root.mainloop()
