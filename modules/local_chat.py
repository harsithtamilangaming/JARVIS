from ctransformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "./models",
    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="mistral",
    max_new_tokens=256,
    threads=4
)

def get_local_response(user_input):
    prompt = f"<s>[INST] {user_input} [/INST]"
    result = model(prompt)
    if "[/INST]" in result:
        return result.split("[/INST]")[-1].strip()
    return result.strip()
