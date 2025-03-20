import base64
import vertexai
import re
from vertexai.generative_models import GenerativeModel, SafetySetting, Part


def multiturn_generate_content():
    vertexai.init(
        project="dealcheck",
        location="us-central1",
        api_endpoint="us-central1-aiplatform.googleapis.com"
    )
    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )
    chat = model.start_chat()
    output1 = chat.send_message([msg4_text1], generation_config=generation_config, safety_settings=safety_settings)
    print(output1)
    return output1

def get_text(model_output):
    candidates = model_output.candidates
    if candidates:
        print("First candidate:", candidates[0])
        candidate = candidates[0]

        if hasattr(candidate, 'content'):
            content = candidate.content
            print("Content:", content) 

            if hasattr(content, 'parts'):
                input_string = content.parts[0].text 
                code = re.search(r'```python\n(.*?)```', input_string, re.DOTALL)

                if code:
                    return code.group(1)
                else:
                    return "No code found."
            else:
                return "No parts in the content."
        else:
            return "No content attribute found in the candidate."
    else:
        return "No candidates found."


msg4_text1 = """Write a Python script to generate and save a depreciation curve using plt.savefig for the 2024 Toyota Corolla using Matplotlib. Choose logical X and Y values. Don't use plt.show() Example:

import numpy as np
import matplotlib.pyplot as plt

years = np.array([0, 1, 2, 3, 4, 5])
values = np.array([25988, 25988, 24680, 22709, 21240, 20000])

plt.figure(figsize=(8, 5))
plt.plot(years, values, marker='o', linestyle='-', color='b', label=\"Honda Civic Value\")
plt.xlabel(\"Years\")
plt.ylabel(\"Estimated Value ($)\")
plt.title(\"Depreciation Curve for 2024 Honda Civic\")
plt.grid(True)
plt.xticks(years)
plt.legend()
plt.savefig('test.png')"""

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

model_output = multiturn_generate_content()
program = get_text(model_output)
exec(program)