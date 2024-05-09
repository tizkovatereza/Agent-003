# pip install -q -U google-generativeai
# pip install google-cloud-aiplatform
# pip install --upgrade google-cloud-aiplatform
# pip install python-dotenv

# pip install e2b_code_interpreter


# Restart kernel after installs so that your environment can access the new packages
from typing import Optional
import IPython

'''
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
'''

# Import the necessary libraries
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


from dotenv import load_dotenv
import os
from google.oauth2 import service_account

load_dotenv()  # Load environment variables from .env

# Get the path to the service account file from the environment variable
service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Use the service account to authenticate
credentials = service_account.Credentials.from_service_account_file(service_account_path)

# You would use 'credentials' to initialize Google Cloud services as needed
# Example: Initializing AI Platform
from google.cloud import aiplatform

aiplatform.init(project='your-google-cloud-project-id', location='us-central1', credentials=credentials)

# Now you can use the environment variables as if they were set in the OS environment
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
E2B_API_KEY = os.getenv('E2B_API_KEY')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')




# Define a function to convert text to markdown
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

'''
try:
    # Used to securely store your API key
    from google.colab import userdata

    # Or use `os.getenv('API_KEY')` to fetch an environment variable.
    GOOGLE_API_KEY=userdata.get('API_KEY')
except ImportError:
    import os
    GOOGLE_API_KEY = os.environ['API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

E2B_API_KEY = "e2b_7dd15697d859d0e4e8c8aabdc7ee2e09a78fa12a"
'''

import sys

# Authenticate to GCP
if "google.colab" in sys.modules:
    from google.colab import auth

    auth.authenticate_user()


# If you need to use general credentials, import like this:
from google.auth import credentials  # Generic credentials interface



PROJECT_ID = "[your-project-id]"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION) 

import requests
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)


# FUNCTIONS DECLARATIONS

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

# GIVE MODEL TOOLS
retail_tool = Tool(
    function_declarations=[
        get_product_info,
        get_store_location,
        place_order,
    ],
)

# CREATE GENERATIVE MODEL
model = GenerativeModel(
    "gemini-1.0-pro-001",
    generation_config=GenerationConfig(temperature=0),
    tools=[retail_tool],
)
chat = model.start_chat()

#Import Optional from the typing Python module

from google.oauth2 import service_account

# Set the path to your service account key file
#service_account_path = '/Users/terezatizkova/Developer/Agent-003/chrome-lambda-422701-b7-0e7a8614a65e.json' # Use environment variable here if needed
#credentials = service_account.Credentials.from_service_account_file(service_account_path)

# Initialize AI Platform with credentials
from google.cloud import aiplatform
aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)


def init_sample(
    project: Optional[str] = None,
    location: Optional[str] = None,
    experiment: Optional[str] = None,
    staging_bucket: Optional[str] = None,
    #credentials: Optional[google.auth.credentials.Credentials] = None,
    encryption_spec_key_name: Optional[str] = None,
    service_account: Optional[str] = None,
):

    from google.cloud import aiplatform

    aiplatform.init(
        project=project,
        location=location,
        experiment=experiment,
        staging_bucket=staging_bucket,
        credentials=credentials,
        encryption_spec_key_name=encryption_spec_key_name,
        service_account=service_account,
    )


chat = model.start_chat()  #enable_automatic_function_calling=True

response = chat.send_message('I have 57 cats, each owns 44 mittens, how many mittens is that in total? And how many degrees it is in San Francisco?')
response.text
