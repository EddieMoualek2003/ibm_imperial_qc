from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

# Paths
base_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
adapter_path = "./quantum-llm-output/checkpoint-750"  # Or checkpoint-final if saved that way

# Load tokenizer and base model
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", torch_dtype=torch.float16)

# Load LoRA adapter on top
model = PeftModel.from_pretrained(model, adapter_path)

# Run test prompt
prompt = "### Instruction:\nExplain the Quantum Zeno Effect in quantum computing.\n\n### Response:"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

# Generate response
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=200)

# Decode and print
print("\n🧠 Model Output:\n" + tokenizer.decode(outputs[0], skip_special_tokens=True))
