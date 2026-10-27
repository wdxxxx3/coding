# 每张图在文本里放 1 个 <image> 占位符；vision 输出每张图 N=256 个 token
emb = llm.embed(input_ids)                                    # [B, T, D]
img_tokens = projector(vision(pixels))                        # [num_images, N, D]
emb[input_ids == IMAGE_ID] = img_tokens.flatten(0, 1)
labels = input_ids.clone()
labels[attention_mask == 0] = -100
