# ... (previous content remains the same)

def custom_model_response(self, message):
    try:
        input_ids = self.custom_tokenizer.encode(message, return_tensors="pt")
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

        with torch.no_grad():
            output = self.custom_model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_length=100,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                temperature=0.7,
                top_p=0.95
            )

        response = self.custom_tokenizer.decode(
            output[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
        return response
    except Exception as e:
        return f"Error in custom model response: {str(e)}"


def get_chat_history(self):
    return self.history