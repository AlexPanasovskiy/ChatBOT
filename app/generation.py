import torch
import collectiondocs as cd
from transformers import AutoTokenizer, AutoModelForCausalLM


model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, 
                                             torch_dtype=torch.float16, 
                                             device_map="auto")


async def generate_answer(question):
    results = cd.collection.query(
        query_texts = [question],
        n_results = 2)
    context = "\n".join(results["documents"][0])

    prompt = f"""<s>[INST] <<SYS>>
            Ты эксперт по AnyLogic. Отвечай ТОЛЬКО на вопрос, используя предоставленный контекст.
            Отвечай кратко и по делу. Не объясняй свои действия.
            Если ответа нет в контексте, скажи: "Информация не найдена в документации".
            Контекст: {context}
            <</SYS>>

            Вопрос: {question} [/INST]"""

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens = 150,
        temperature = 0.3,
        do_sample = False,
        pad_token_id = tokenizer.eos_token_id)

    input_length = inputs.input_ids.shape[1]
    generated_ids = outputs[:, input_length:]
    
    clean_response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    clean_response = clean_response.strip()
    
    return clean_response