# import torch
# from speechbox import ASRDiarizationPipeline, PunctuationRestorer
# from datasets import load_dataset

# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# pipeline = ASRDiarizationPipeline.from_pretrained("openai/whisper-large-v3", device=device)

# # load dataset of concatenated LibriSpeech samples
# concatenated_librispeech = load_dataset("sanchit-gandhi/concatenated_librispeech", split="train", streaming=True)
# # get first sample
# sample = next(iter(concatenated_librispeech))

# out = pipeline(sample["audio"])
# print(out)

# it prints out fine, but when using large-v3, it doesnt include punctuation and capitalization. 

# Restore the punctuation and capitalization of the transcribed text



from speechbox import PunctuationRestorer
from datasets import load_dataset

streamed_dataset = load_dataset("librispeech_asr", "clean", split="validation", streaming=True)

# get first sample
sample = next(iter(streamed_dataset))

# print out normalized transcript
print(sample["text"])
# => "HE WAS IN A FEVERED STATE OF MIND OWING TO THE BLIGHT HIS WIFE'S ACTION THREATENED TO CAST UPON HIS ENTIRE FUTURE"

# load the restoring class
restorer = PunctuationRestorer.from_pretrained("openai/whisper-medium")
restorer.to("cuda")

restored_text, log_probs = restorer(sample["audio"]["array"], sample["text"], sampling_rate=sample["audio"]["sampling_rate"], num_beams=1)

print("Restored text:\n", restored_text)