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

import keras_ocr # started by installing keras_ocr on the local environment.
import cv2
import math
import numpy as np

import streamlit as st
import streamlit.components.v1 as components

#os.environ["OPENAI_API_KEY"] 
#os.environ["VISION_KEY"] 
#endpoint = os.environ["VISION_ENDPOINT"]

st.set_page_config(layout="wide") 

subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#Don't change the background path
BACKGROUND_PATH = os.path.join(BASE_DIR, "static/")




computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

# pipeline = keras_ocr.pipeline.Pipeline()

def inpaint_text(img_path, pipeline):
    # read image
    img = keras_ocr.tools.read(img_path)
    # generate (word, box) tuples 
    prediction_groups = pipeline.recognize([img])
    mask = np.zeros(img.shape[:2], dtype="uint8")
    for box in prediction_groups[0]:
        x0, y0 = box[1][0]
        x1, y1 = box[1][1] 
        x2, y2 = box[1][2]
        x3, y3 = box[1][3] 
        
        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mi1 = midpoint(x0, y0, x3, y3)
        
        thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
        
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,    
        thickness)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
                 
    return(img)

def text_less_image_freeze(img_path):

    pipeline = keras_ocr.pipeline.Pipeline()

    result_img = inpaint_text(img_path, pipeline)

    img_name = img_path.split("/")[-1].split(".")[0]

    img_name = "".join([c for c in img_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    img_name = img_name + ".jpg"
    #Image.fromarray(result_img).save("backend/background_images/background.jpg")

    Image.fromarray(result_img).save(os.path.join(BACKGROUND_PATH, img_name))
    
    #Image.fromarray(result_img).save(BACKGROUND_PATH + img_name)
    image = Image.fromarray(result_img)

    with open(BACKGROUND_PATH + img_name, 'wb') as f:
        f.write(image.getbuffer())
    
    return img_name

def text_less_image(img_path):

    pipeline = keras_ocr.pipeline.Pipeline()

    result_img = inpaint_text(img_path, pipeline)

    img_name = img_path.split("/")[-1].split(".")[0]
    img_name = "".join([c for c in img_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    img_name = img_name + ".jpg"

    # Sauvegardez l'image
    Image.fromarray(result_img).save(os.path.join(BACKGROUND_PATH, img_name))
    #Image.fromarray(result_img).save(f"static/{img_name}")

    return img_name

def text_recognition(img_url):

    print("===== Read File - remote =====")
    print(BASE_DIR)
    print(BACKGROUND_PATH)
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


# html_css_gen that implements the background in HTML code
def html_css_gen(layout, background_image):
   prompt = PromptTemplate(
            template="""
        This is a representation of a website design, which may come from a hand-drawn sketch or a design created using software like Figma or Adobe XD. 
        The design includes text elements, images, graphical elements, and their coordinates along with the coordinates of their four outer vertices.
        Construct a modern, sans-serif website using the HTML and Tailwind CSS framework that mirrors these design elements.
        For images and graphical elements, use appropriate HTML tags like <img> and <svg>, and ensure they are placed and sized according to the coordinates provided in the layout.
        Determine the appropriate HTML and Tailwind CSS classes to reflect their relative positions. 
        Utilize layout tags to represent their font size and relative placement based on the provided coordinates. 
        If elements appear to be part of a menu, employ <ul> and <li> tags. Intelligently use tags such as <button> and <input> based on the element names.
        Prioritize the design according to the given coordinates but also employ some creative freedom in the layout and CSS based on standard web design principles. 
        Refrain from using absolute coordinates in your HTML source code. 
        The output should be a combined HTML and Tailwind CSS source code without any descriptive commentary. 
        Generate only source code file, no description: {layout}.
        You receive a background image that you will integrate to the HTML and CSS code using the CSS \'background-image\' property. The background image is part of the layout as the background of the website : {background_image}.
        """
            ,
       input_variables=["layout", "background_image"]
   )
   llm = ChatOpenAI(model="gpt-4-0613",temperature=0)
   chain = LLMChain(prompt=prompt, llm=llm)
   output = chain.run(layout=layout, background_image = background_image)
   print(output)

   return output        
       


def image_run():
    html_code = ""
    layout = text_recognition(st.session_state.img)
    background_img_name = text_less_image(st.session_state.img)
    # background_image = f"http://localhost:8501/static/{background_img_name}"
    
    background_image = f"https://geniefront.streamlit.app/static/{background_img_name}"
    #background_image = f"app/static/{background_img_name}"
    if layout != []:
        html_code = html_css_gen(layout, background_image)

    st.session_state.html = html_code
    st.session_state.image = st.session_state.img

if "html" not in st.session_state:
    st.session_state.html = ""
if "image" not in st.session_state:
    st.session_state.image = ''    


# Front
st.title("GenieFront - Generative Vision for Front-End Development 🧞")



user_guide = """
**User Guide:**

---

**Step-by-Step Instructions for Using GenieFront on Streamlit:**

1. **Upload Your Design**:
   - Navigate to the "Image URL" input box.
   - Enter the URL of your design image. Ensure the image is publicly accessible.
   
2. **Process the Design**:
   - Click the "Run" button. GenieFront will analyze your design, extract design elements, and generate the corresponding HTML and CSS code.
   
3. **View the Results**:
   - On the right panel, you'll see the generated source code within the "See source code" expander. You can copy this code for your use.
   - Below the source code section, you'll find a real-time preview of how the design translates to a live website.

4. **Feedback & Iteration**:
   - If the resultant code doesn't align with your expectations, you can adjust your design and try again. Remember, clearer designs yield better results!
"""

with st.sidebar:
    "[View the source code](https://github.com/zlaabsi/geniefront/main/backend/app.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/zlaabsi/geniefront?quickstart=1)"
    st.markdown(user_guide)


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
