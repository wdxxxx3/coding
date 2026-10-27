# SFT 损失。input_ids = prompt + response + pad，pad_id == eos_id
logits = model(input_ids).logits                     # [B, T, V]
labels = input_ids.clone()
labels[input_ids == pad_id] = -100
loss = F.cross_entropy(logits.view(-1, V), labels.view(-1), ignore_index=-100)
