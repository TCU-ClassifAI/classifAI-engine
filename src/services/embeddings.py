# import openai
# import numpy as np
# import re
# import os
# import pandas as pd

# # Load .env file if it exists
# from dotenv import load_dotenv

# load_dotenv()
# openai.api_key = os.environ["OPENAI_API_KEY"]

# # Load the text file
# file_path = "file.txt"

# sentences = []

# # Split the text into sentences (separated by a period, question mark, or exclamation point, etc.)

# with open(file_path, "r") as file:
#     # Read the entire content of the file into the string
#     file_content = file.read()
#     # Split the text into sentences (separated by a period, question mark, or exclamation point, etc.)
#     sentences = re.split(r"[.!?]+", file_content)
#     sentences = list(filter(None, sentences))


# df = pd.DataFrame(sentences, columns=["text"])

# print(df)
# from openai.embeddings_utils import get_embedding

# # embedding model parameters
# embedding_model = "text-embedding-ada-002"
# embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
# max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# import tiktoken

# # df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)

# encoding = tiktoken.get_encoding(embedding_encoding)
# df["embedding"] = df.combine.apply(lambda x: get_embedding(x, engine=embedding_model))

# print(df)
