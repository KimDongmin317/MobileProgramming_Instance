import re
from flask import Flask, request
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
from PIL import Image

app = Flask(__name__)

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

device = "cuda" if torch.cuda.is_available() else "cpu"

model.to(device)

@app.route('/')
def hello():
    return 'Hi'

@app.route('/process_invoice', methods=['POST'])
def process_invoice():
    # Get the input image file from the request
    image = Image.open(request.files['invoice_photo'])
    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

    pixel_values = processor(image, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token

    # Create a JSON response
    response = processor.token2json(sequence)

    # Return the JSON response
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
