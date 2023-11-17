import re

MAX_TOKENS = 8000


def split_text_into_chunks(text, max_tokens):
    # Split text into chunks with a maximum number of tokens
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_tokens:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def summarize_content(content, max_tokens):
    # Implement your summarization function here
    # This could be your GPT-4 summarization model or any other summarization approach
    # For simplicity, let's just return the first sentence of each chunk here
    return [chunk.split(".")[0] for chunk in content]


def summarize_content_long(transcript: str, max_tokens: int = 8000) -> str:
    """Summarize the transcript into a short summary. Uses Chunking and GPT-4 for long transcripts.

    Args:
        transcript (str): The transcript to summarize.
        max_tokens (int, optional): The maximum number of tokens to use for the summary. Defaults to 8000.

    Returns:
        str: The summary of the transcript.
    """

    chunks = split_text_into_chunks(transcript, max_tokens=MAX_TOKENS)

    if len(chunks) == 1:
        # If there is only one chunk, use its summary directly
        return summarize_content(chunks[0], MAX_TOKENS)
    else:
        # Summarize each chunk
        chunk_summaries = [summarize_content(chunk, MAX_TOKENS) for chunk in chunks]

        # Combine chunk summaries and summarize the combined content
        combined_summary = summarize_content(
            " ".join([" ".join(chunk_summary) for chunk_summary in chunk_summaries]),
            MAX_TOKENS,
        )

    # Print the final summary
    print(" ".join(combined_summary))
