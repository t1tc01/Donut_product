"""
Test raw model pretrained
"""

from datasets import load_dataset
from transformers import DonutProcessor, VisionEncoderDecoderModel
import re 
import torch
import time

dataset = load_dataset("hf-internal-testing/example-documents", split="test")
image = dataset[2]["image"]
print("Load sample done!")

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
print("Load model done!")

device = 'cpu'
model.to(device)

task_prompt = "<s_cord-v2>"
decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
pixel_values = processor(image, return_tensors="pt").pixel_values

start_time = time.time()
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
end_time = time.time()
print("Time execute: ", end_time - start_time)

sequence = processor.batch_decode(outputs.sequences)[0]
sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
print(processor.token2json(sequence))