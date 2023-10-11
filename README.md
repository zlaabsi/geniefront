# GenieFront [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://geniefront.streamlit.app/)


![GenieFront Presentation Hackathon](https://github.com/zlaabsi/geniefront/assets/52045850/f812c181-beaa-4bfc-ab18-e4b0417d9282)

---

## Introduction

GenieFront stands at the crossroads of design and development, offering a state-of-the-art solution to transform visual web designs into interactive front-end code. By leveraging advanced technologies, GenieFront automates the process of generating HTML and CSS code from a visual design, be it a digital mock-up, a photo, or even a hand-drawn sketch.

---

## Demo 



https://github.com/zlaabsi/geniefront/assets/52045850/4489cf22-3ab2-4573-96bc-f4b91da61a49



---

## Technologies Used

- **Streamlit**: Provides a user-friendly web interface, making it easy for users to input design images and view the generated source code.
- **Azure Computer Vision**: Employs Optical Character Recognition (OCR) capabilities to detect and extract textual elements from the input design.
- **Keras-OCR**: A tool used for OCR, particularly effective at isolating text from other visual elements.
- **GPT-4 by OpenAI**: A generative language model responsible for interpreting the design layout and crafting the corresponding HTML and CSS code.
- **Python Libraries**: Essential libraries such as `os`, `sys`, `PIL`, `numpy`, and `cv2` are utilized to facilitate image processing and other functionalities.

---
## GenieFront Workflow Diagram
![GenieFront Workflow Diagram](https://github.com/zlaabsi/geniefront/assets/52045850/f23f04d7-b326-421c-adcf-55c9addc0faa)


---

## Key Functionalities

1. **Text Recognition with Azure**: The system extracts textual elements from the input image using Azure's OCR capabilities. This is essential to ensure the generated code includes all textual content as intended by the design.

2. **Image Processing with Keras-OCR**: The `inpaint_text` function employs Keras-OCR to remove text from the design image. This process, termed "inpainting", ensures that only the design components remain, paving the way for precise code generation.

3. **Code Generation using GPT-4**: The extracted layout from the processed image is input to a GPT-4 model. This model interprets the design and generates corresponding HTML and CSS code, ensuring an accurate representation of the visual design.

4. **Tailored Code Generation**: An additional function, `html_css_gen`, can integrate a background image into the final output. This is crucial for designs where the background plays a pivotal role in the overall aesthetics.

5. **User Interface with Streamlit**: A minimalist yet effective user interface allows users to input their design images and view the generated code. Additionally, there's an option to visualize the transformed website directly within the application.

---

## In-Depth Function Breakdown with Code Examples

### Azure Computer Vision Integration

The `ComputerVisionClient` from Azure's SDK is employed to tap into their OCR capabilities. Here's a code snippet showcasing its usage:

```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
```

### Keras-OCR for Image Processing

The `inpaint_text` function uses `keras_ocr` for text detection and removal:

```python
import keras_ocr

def inpaint_text(img_path, pipeline):
    img = keras_ocr.tools.read(img_path)
    prediction_groups = pipeline.recognize([img])
    mask = np.zeros(img.shape[:2], dtype="uint8")
    for box in prediction_groups[0]:
        # ... code to process the bounding box and create a mask ...
    img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
    return img
```

### GPT-4 for Code Generation

The cleaned design is fed to GPT-4 for code generation. While the actual communication with GPT-4 might be abstracted behind APIs, the idea is to send the recognized layout to the model and retrieve the generated code.


### Streamlit for User Interaction

Streamlit offers a simple way to create web interfaces. Here's a basic example from the script:

```python
import streamlit as st

st.title("GenieFront - Generative Vision for Front-End Development")
user_input = st.text_input("Image URL:", value="", key='img')
```

### Supporting Functions

1. **midpoint**: Assists in finding the midpoint between two coordinates.

```python
def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)
```

2. **text_recognition**: Uses Azure's Computer Vision to recognize and extract text from the design.

```python
def text_recognition(img_url):
    read_response = computervision_client.read(img_url,  raw=True)
    # ... processing to get the text ...
    return layout
```

3. **text_less_image**: Processes the design to isolate the design elements.

```python
def text_less_image(img_path):
    pipeline = keras_ocr.pipeline.Pipeline()
    result_img = inpaint_text(img_path, pipeline)
    # ... further processing ...
    return img_name
```

4. **html_css_gen**: Generates the final HTML and CSS code, integrating the background image.

```python
def html_css_gen(layout, background_image):
    prompt = PromptTemplate( ... )  # Template for GPT-4
    output = chain.run(layout=layout, background_image=background_image)
    return output
```

These functions form the backbone of the GenieFront solution, ensuring a smooth transition from design to code.

---

## Running GenieFront

To run GenieFront locally:

1. Clone the repository to your local machine.
2. Ensure you have all required libraries installed. You can install them using `pip install -r requirements.txt`.
3. Set the necessary environment variables, particularly the API keys for Azure and OpenAI.
4. Navigate to the project directory in your terminal and run the command:
    ```
    streamlit run app.py
    ```
5. Open the provided local URL in your web browser to interact with GenieFront.

---

## Conclusion

GenieFront is not just a tool; it's a testament to what's possible when design meets technology. As web development continues to evolve, tools like GenieFront will be instrumental in bridging the gap between designers and developers, making the
