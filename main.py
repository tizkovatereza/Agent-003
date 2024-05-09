# pip install -q -U google-generativeai
# pip install google-cloud-aiplatform
# pip install --upgrade google-cloud-aiplatform
# pip install python-dotenv

# Import necessary libraries
from typing import Optional
import textwrap
from dotenv import load_dotenv
import os
import pathlib
import requests

from IPython.display import Markdown

import google.generativeai as genai
import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Tool,
)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
E2B_API_KEY = os.getenv('E2B_API_KEY')

# Configuration for generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Vertex AI and Project configuration
PROJECT_ID = "[your-project-id]"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION) 

# Function declarations for the model
get_current_weather_func = FunctionDeclaration(
    name="get_current_weather",
    description="Get the current weather in a given location",
    parameters={
        "type": "object",
        "properties": {"location": {"type": "string", "description": "The city name of the location for which to get the weather."}},
    },
)

get_product_info = FunctionDeclaration(
    name="get_product_info",
    description="Get the stock amount and identifier for a given product",
    parameters={
        "type": "object",
        "properties": {
            "product_name": {"type": "string", "description": "Product name"}
        },
    },
)

get_store_location = FunctionDeclaration(
    name="get_store_location",
    description="Get the location of the closest store",
    parameters={
        "type": "object",
        "properties": {"location": {"type": "string", "description": "Location"}},
    },
)

place_order = FunctionDeclaration(
    name="place_order",
    description="Place an order",
    parameters={
        "type": "object",
        "properties": {
            "product": {"type": "string", "description": "Product name"},
            "address": {"type": "string", "description": "Shipping address"},
        },
    },
)

# Create generative model with tools
retail_tool = Tool(
    function_declarations=[
        get_product_info,
        get_store_location,
        place_order,
    ],
)

model = GenerativeModel(
    "gemini-1.0-pro-001",
    generation_config=GenerationConfig(temperature=0),
    tools=[retail_tool],
)

# Start chat session with the model
chat = model.start_chat()

# Function to convert text to Markdown (if needed)
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Send a message to the chat and print the response
response = chat.send_message('I have 57 cats, each owns 44 mittens, how many mittens is that in total? And how many degrees it is in San Francisco?')
print(response.text)
