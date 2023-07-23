import torch
import gradio as gr
import tiktoken
import boto3


MODEL_PATH = 's3://emlo3/model_gpt.script.pt'

# tokenizer
cl100k_base = tiktoken.get_encoding("cl100k_base")

# In production, load the arguments directly instead of accessing private attributes
# See openai_public.py for examples of arguments for specific encodings
tokenizer = tiktoken.Encoding(
    # If you're changing the set of special tokens, make sure to use a different name
    # It should be clear from the name what behaviour to expect.
    name="cl100k_im",
    pat_str=cl100k_base._pat_str,
    mergeable_ranks=cl100k_base._mergeable_ranks,
    special_tokens={
        **cl100k_base._special_tokens,
        "<|im_start|>": 100264,
        "<|im_end|>": 100265,
    }
)


def split_s3_path(s3_path):
    path_parts=s3_path.replace("s3://","").split("/")
    bucket=path_parts.pop(0)
    key="/".join(path_parts)
    return bucket, key


s3_client = boto3.client('s3', region_name='us-west-2')
model_bucket, model_key = split_s3_path(MODEL_PATH)
s3_client.download_file(model_bucket,model_key,'model_gpt.script.pt')


loaded_model = torch.jit.load('model_gpt.script.pt')

def predict(text: str, max_new_tokens: int = 32) -> str:
    input_enc = torch.tensor(tokenizer.encode(text))
    with torch.no_grad():
        out_gen = loaded_model.model.generate(input_enc.unsqueeze(0).long(), max_new_tokens=max_new_tokens)
    decoded = tokenizer.decode(out_gen[0].cpu().numpy().tolist())
    return decoded
    
    
grdemo = gr.Interface(
    fn=predict,
    inputs=[gr.Textbox(lines=5, placeholder="Enter text here..."), gr.Slider(32, 512, value=10, step=32, label="Max number of tokens:")],
    outputs="text",
)

if __name__ == "__main__":
    grdemo.launch(server_port=80, server_name='0.0.0.0')
