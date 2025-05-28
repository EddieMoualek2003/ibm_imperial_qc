from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Step 1: Load base model and tokenizer
base_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
adapter_path = "./quantum-llm-output/checkpoint-750"  # Or change if needed

print("🔁 Loading base model...")
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("🔗 Loading LoRA adapter...")
model = PeftModel.from_pretrained(model, adapter_path)
print("🧬 Merging LoRA with base...")
model = model.merge_and_unload()

print("💾 Saving merged model...")
output_dir = "./quantum-llm-merged"
model.save_pretrained(output_dir)
tokenizer = AutoTokenizer.from_pretrained(base_model)
tokenizer.save_pretrained(output_dir)

print("✅ Merged model saved to:", output_dir)
