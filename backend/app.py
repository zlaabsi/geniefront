# streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

import streamlit as st
import streamlit.components.v1 as components

os.environ["OPENAI_API_KEY"] = ""
os.environ["VISION_KEY"] = ""
endpoint = os.environ["VISION_ENDPOINT"] = ""
st.set_page_config(layout="wide") 

subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def text_recognition(img_url):

    print("===== Read File - remote =====")
    read_response = computervision_client.read(img_url,  raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    layout = []
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                layout.append({line.text:line.bounding_box})
    print(layout)
    print("End of Computer Vision.")
    return layout

def html_gen(layout):
    prompt = PromptTemplate(
        template="""This is a layout of a handwriting website design, including text and their coordinates of four outer vertices. 
        Make an HTML modern sans-serif website that reflects these elements and decide which 
        CSS can be used to match their relative positions, try to use proper layout tags to match
         their font size and relative placement based on their coordinates. 
         Use <ul> and <li> if the elements look like as menu list. 
         Smartly use function tags like <button> <input> if their names look like that.
         Your design should be prior to the coordinates, 
         then you should also use some imagination for the layout and CSS from common web design principle.
         Remember, don't use absolute coordinates in your HTML source code. 
         Generate only source code file, no description: {layout}.\n""",
        input_variables=["layout"]
    )
    llm = ChatOpenAI(model="gpt-4-0613",temperature=0)
    chain = LLMChain(prompt=prompt, llm=llm)
    output = chain.run(layout=layout)
    print(output)

    return output

def html_css_gen(layout):
    prompt = PromptTemplate(
        template = """
        This is a representation of a website design, which may come from a hand-drawn sketch or a design created using software like Figma or Adobe XD. 
        The design includes text elements, images, graphical elements, and their coordinates along with the coordinates of their four outer vertices.
        Construct a modern, sans-serif website using the HTMLand Tailwind CSS that mirrors these design elements.
        For images and graphical elements, use appropriate HTML tags like <img> and <svg>, and ensure they are placed and sized according to the coordinates provided in the layout.
        Determine the appropriate HTML and Tailwind CSS classes to reflect their relative positions. 
        Utilize layout tags to represent their font size and relative placement based on the provided coordinates. 
        If elements appear to be part of a menu, employ <ul> and <li> tags. Intelligently use tags such as <button> and <input> based on the element names.
        Prioritize the design according to the given coordinates but also employ some creative freedom in the layout and CSS based on standard web design principles. 
        Refrain from using absolute coordinates in your HTML source code. 
        The output should be a combined HTML and Tailwind CSS source code without any descriptive commentary.
        Don't include ```html at the beginning of the code source and ``` at the end of the source code.
        Generate only source code file, no description: {layout}.""",
        input_variables=["layout"]
    )
    llm = ChatOpenAI(model="gpt-4-0613",temperature=0)
    chain = LLMChain(prompt=prompt, llm=llm)
    output = chain.run(layout=layout)
    print(output)

    return output        
       


def image_run():
    html_code = ""
    layout = text_recognition(st.session_state.img)
    if layout != []:
        html_code = html_css_gen(layout)

    st.session_state.html = html_code
    st.session_state.image = st.session_state.img

if "html" not in st.session_state:
    st.session_state.html = ""
if "image" not in st.session_state:
    st.session_state.image = ''    


st.title("Jincraft - Generative Vision")
col1, col2 = st.columns([0.5, 0.5], gap='medium')
with col1:
    st.text_input("Image URL:", value="", key='img')
    st.button("Run", on_click=image_run)
    if st.session_state.image != '':
        st.image(st.session_state.image)
with col2:
    with st.expander("See source code"):
        st.code(st.session_state.html)
    with st.container():
        components.html(st.session_state.html, height=600, scrolling=True)




