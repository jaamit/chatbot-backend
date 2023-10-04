from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import faiss
import numpy as np

# Load GPT-2 model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Assume we have a function to fetch the FAQ embeddings from the vector DB
# Mocking a random embedding
# Assuming the embeddings are of size 768
def get_faq_embedding(question):
    return torch.rand(1, 768)  

# Create a vector database for storing user question embeddings
user_question_db = faiss.IndexFlatIP(768) 

# Function to add a user question embedding to the vector database
def add_user_question_embedding(embedding):

    embedding_np = embedding.cpu().numpy()
    embedding_2d = embedding_np.reshape(1, -1)

    # Pad the embedding if needed
    if embedding_2d.shape[1] < 768:
        padded_embedding = np.zeros((1, 768))
        padded_embedding[:, :embedding_2d.shape[1]] = embedding_2d
        embedding_2d = padded_embedding

    # Check if the dimensions match
    if user_question_db.d == -1:
        # If the index is empty, set the dimension based on the embedding
        user_question_db.d = embedding_2d.shape[1]
    else:
        assert embedding_2d.shape[1] == user_question_db.d, f"Dimensions mismatch: Expected {user_question_db.d}, got {embedding_2d.shape[1]}"
    user_question_db.add(embedding_2d)

# Function to generate output using GPT-2 based on a prompt
def generate_gpt2_output(prompt, max_length=100, temperature=0.7):
    # Tokenize the prompt using GPT-2 tokenizer and ensure it fits within max_length
    input_ids = tokenizer.encode(prompt, max_length=max_length, return_tensors="pt", truncation=True)
    
    # Generate text based on the input prompt
    output = model.generate(input_ids,
                                max_length=max_length,
                                temperature=temperature,
                                num_return_sequences=1,
                                pad_token_id=tokenizer.eos_token_id,
                                do_sample=True)
    
    # Decode the generated output into text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Function to generate a combined prompt given a user question
def generate_combined_prompt(question, max_length=1000):
    faq_embedding = get_faq_embedding(question)
    
    # Convert FAQ embedding and question to text
    faq_text = " ".join([str(val) for val in faq_embedding.flatten().tolist()])
    question_text = question
    
    # Combine FAQ and question into a prompt
    combined_prompt = f"Given this FAQ: {faq_text}, and a question: '{question_text}', what's the answer?"
    
    combined_prompt = combined_prompt[:max_length]
    return combined_prompt

def generate_bot_response(text: str):
    print(text)
    print("Generating response")
    # sample_question = "How do I update my password?"

    # Generate the combined prompt
    combined_prompt = generate_combined_prompt(text)

    # Generate the output using GPT-2
    generated_output = generate_gpt2_output(combined_prompt, max_length=1000, temperature=0.7)

    return generated_output
