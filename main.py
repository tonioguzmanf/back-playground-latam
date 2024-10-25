from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import fitz

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate(prompt_list, system_instructions, model, region, max_output_tokens, temperature):
    vertexai.init(project="your_project_id", location=region)
    model = GenerativeModel(
        model,
        system_instruction=[system_instructions]
    )

    generation_config = {
        "max_output_tokens": max_output_tokens,
        "temperature": temperature,
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

    responses = model.generate_content(
        prompt_list,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    result = ""
    for response in responses:
        result += response.text
    return result

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Define the route for the HTTP POST request
@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        # Get the JSON data from the request
        #data = request.get_json()
        data = request.form
        prompt = f"""{data.get('prompt')}"""
        system_instructions = f"""{data.get('system_instructions')}"""
        model = data.get('model')
        region = data.get('region')
        max_output_tokens = int(data.get('max_output_tokens'))
        temperature = float(data.get('temperature'))
        #file = data.get('file')
        #safety_level = int(data.get('safety_settings'))

        # Validate input
        if not prompt or not system_instructions:
            return jsonify({"error": "Both 'prompt' and 'system_instructions' are required."}), 400

        prompt_list = [prompt]
        #print("primer prompt")
        #print(prompt_list)

        pdf_files = request.files.getlist('file')
        if pdf_files:
            for file in pdf_files:
            # Extract text from the PDF file
                pdf_text = extract_text_from_pdf(file)
                pdf_text = f"""{pdf_text}"""
                prompt_list.append(pdf_text)

        #print("segundo prompts")
        #print(prompt_list)

        # Call the generate function and get the result
        result = generate(prompt_list, system_instructions, model, region, max_output_tokens, temperature)
        # Return the result as a JSON response
        print("respuesta exitosa")
        print(result)
        return jsonify({"result": result}), 200
    except Exception as e:
        # Handle any errors that occur and return an error response
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
