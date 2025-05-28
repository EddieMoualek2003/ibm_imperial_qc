from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
from transformers import BitsAndBytesConfig
import torch

# Load dataset
dataset = load_dataset("json", data_files="./data/quantum_llm_dataset_v1_expanded.json")

# Tokenizer and model
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# QLoRA config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Tokenization function
def tokenize(example):
    prompt = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
    result = tokenizer(prompt, padding="max_length", truncation=True, max_length=512)
    result["labels"] = result["input_ids"].copy()
    return result

tokenized_dataset = dataset["train"].map(tokenize)

# Training arguments
training_args = TrainingArguments(
    output_dir="./quantum-llm-output",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_dir="./logs",
    fp16=True,
    save_total_limit=2,
    report_to="none",
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

# Train!
trainer.train()
