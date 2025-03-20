import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]


def encode_img(path):
    with open(path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
    # print(base64_string)
    return base64_string

def decode_img(base64_string):
    with open("decoded_image.jpg", "wb") as out_file:
        out_file.write(base64.b64decode(base64_string))

def multiturn_generate_content(img):
    vertexai.init(
        project="dealcheck",
        location="us-central1",
        api_endpoint="us-central1-aiplatform.googleapis.com"
    )
    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )
    chat = model.start_chat()
    print(chat.send_message(
        [img, """What car is in the provided image?"""],
        generation_config=generation_config,
        safety_settings=safety_settings
    ))
    




def main():
    img = encode_img("./D4/car.jpg")
    msg1_image1 = Part.from_data(mime_type="image/jpeg", data=base64.b64decode(img))
    multiturn_generate_content(msg1_image1)
    
if __name__ == "__main__":
    main()