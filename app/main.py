from http import HTTPStatus
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from json import JSONDecodeError
import uvicorn


import numpy as np 
from datasets import load_dataset
from transformers import DonutProcessor, VisionEncoderDecoderModel
import re 
import torch
import time

from PIL import Image

origins = ["http://localhost:8080"]


app = FastAPI(
    title="Document Parsing Invoice using Donut",
    description=""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def load_model():
    global processor 
    global model
    global decoder_input_ids

    task_prompt = "<s_cord-v2>"
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
    


@app.get("/", tags=['General'])
def ref_root():
    """
        Health check.
    """
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response

@app.get("/predict_test/", tags=["Test"])
def test_predict():
    dataset = load_dataset("hf-internal-testing/example-documents", split="test")
    image = dataset[2]["image"]
    pixel_values = processor(image, return_tensors="pt").pixel_values

    #Run predict
    outputs = model.generate(
        pixel_values.to('cpu'),
        decoder_input_ids=decoder_input_ids.to('cpu'),
        max_length=model.decoder.config.max_position_embeddings,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    #Post-processing
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip() 
    result_json = processor.token2json(sequence)

    #Return result in JSON format
    return result_json



@app.post("/predict", tags=["Prediction"])
async def predict(file: UploadFile = File(...)):

    # #Read and pre-process image
    image = Image.open(file.file)
    pixel_values = processor(image, return_tensors="pt").pixel_values

    #Run predict
    outputs = model.generate(
        pixel_values.to('cpu'),
        decoder_input_ids=decoder_input_ids.to('cpu'),
        max_length=model.decoder.config.max_position_embeddings,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    #Post-processing
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip() 
    result_json = processor.token2json(sequence)

    #Return result in JSON format
    return result_json


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8008)

