# GenieFront [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://geniefront.streamlit.app/)


![GenieFront Presentation Hackathon](https://github.com/zlaabsi/geniefront/assets/52045850/f812c181-beaa-4bfc-ab18-e4b0417d9282)

---

## Introduction

GenieFront stands at the crossroads of design and development, offering a state-of-the-art solution to transform visual web designs into interactive front-end code. By leveraging advanced technologies, GenieFront automates the process of generating HTML and CSS code from a visual design, be it a digital mock-up, a photo, or even a hand-drawn sketch.

---

## Technologies Used

- **Streamlit**: Provides a user-friendly web interface, making it easy for users to input design images and view the generated source code.
- **Azure Computer Vision**: Employs Optical Character Recognition (OCR) capabilities to detect and extract textual elements from the input design.
- **Keras-OCR**: A tool used for OCR, particularly effective at isolating text from other visual elements.
- **GPT-4 by OpenAI**: A generative language model responsible for interpreting the design layout and crafting the corresponding HTML and CSS code.
- **Python Libraries**: Essential libraries such as `os`, `sys`, `PIL`, `numpy`, and `cv2` are utilized to facilitate image processing and other functionalities.

---

## Key Functionalities

1. **Text Recognition with Azure**: The system extracts textual elements from the input image using Azure's OCR capabilities. This is essential to ensure the generated code includes all textual content as intended by the design.

2. **Image Processing with Keras-OCR**: The `inpaint_text` function employs Keras-OCR to remove text from the design image. This process, termed "inpainting", ensures that only the design components remain, paving the way for precise code generation.

3. **Code Generation using GPT-4**: The extracted layout from the processed image is input to a GPT-4 model. This model interprets the design and generates corresponding HTML and CSS code, ensuring an accurate representation of the visual design.

4. **Tailored Code Generation**: An additional function, `html_css_gen`, can integrate a background image into the final output. This is crucial for designs where the background plays a pivotal role in the overall aesthetics.

5. **User Interface with Streamlit**: A minimalist yet effective user interface allows users to input their design images and view the generated code. Additionally, there's an option to visualize the transformed website directly within the application.

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
