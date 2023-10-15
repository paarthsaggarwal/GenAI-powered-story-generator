from langchain.prompts import PromptTemplate
import openai
import re, os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from requests import get
import urllib.request
from elevenlabs import generate
from elevenlabs import set_api_key
import streamlit as st # importing streamlit which will display the story on a website
import os 
from dotenv import find_dotenv, load_dotenv # importing dotenv to acquire the path to the API keys in the .env file

# Acquiring the path to the .env file which contains the API keys
dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

# Acquiring the API Keys of OpenAI and ElevenLabs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
Elevenlabs_KEY = os.getenv("Elevenlabs_KEY")

llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.9, max_tokens=200)

def generate_story(name, character, genre, setting, plot):
    #Generating a story using the langchain library and OpenAI's GPT-3 model
    prompt = PromptTemplate(
        input_variables=["name","character", "genre", "setting", "plot"],
        template=""" 
         You are a fun and seasoned storyteller. 
            Embrace your inner storyteller and craft a captivating short tale starring a {character} named {name}. 
            Your creative canvas is limited to the {genre} genre, with the story commencing in the world of {setting}. 
            Develop a well-structured narrative, the plot will be {plot} with a clear beginning, a suspenseful middle, 
            and a firm conclusion which makes sense. 
            The conclusion has to be the highest priority and it needs to make sense to the average reader.
                 """
    )
    story = LLMChain(llm=llm, prompt=prompt)
    return story.run({'name': name, 'character': character, 'genre': genre, 'setting': setting, 'plot': plot})

# Generating the audio which is narrating the story
def generate_audio(text, voice):
    #Converting the generated story to audio using the Eleven Labs API based on the voice selection
    audio = generate(text=text, voice=voice, api_key=Elevenlabs_KEY)
    return audio