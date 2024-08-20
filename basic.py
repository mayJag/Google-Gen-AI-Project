import google.generativeai as genai
import os
import textwrap
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '*')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Retrieve API key from environment variable
GOOGLE_API_KEY = 'AIzaSyAhd6hBehgK4QRMrnGgukT1VZKSoDqNETk'

genai.configure(api_key=GOOGLE_API_KEY)

# List available models for user selection
print("Available models:")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

# Get user's model choice
while True:
  model_name = input("Enter the name of the model you'd like to use: ")
  try:
    model = genai.GenerativeModel(model_name)
    break  # Exit loop if the model is found
  except ValueError:
    print("Model not found. Please choose from the available models.")

# Get user's prompt
user_prompt = input("Enter your prompt: ")

# Generate and display response
try:
  response = model.generate_content(user_prompt)
  print(response.text)
  display(to_markdown(response.text))
except Exception as e:
  print(f"An error occurred: {e}")
