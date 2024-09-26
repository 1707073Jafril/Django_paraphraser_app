# paraphrase/some_paraphrase_library.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Use GPU if available, else CPU
model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws").to(device)

def paraphrase_function(input_paragraph):
    # Prepare the input text
    text = "paraphrase: " + input_paragraph + " </s>"
    
    # Tokenize the input
    encoding = tokenizer.encode_plus(
        text,
        pad_to_max_length=True,
        return_tensors="pt"
    )
    
    # Move input tensors to the correct device (CPU or GPU)
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)
    
    # Generate paraphrases
    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=256,
        do_sample=True,
        top_k=120,
        top_p=0.95,
        early_stopping=True,
        num_return_sequences=5
    )
    
    # Decode the outputs
    paraphrased_sentences = []
    for output in outputs:
        line = tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        paraphrased_sentences.append(line)

    return paraphrased_sentences
