from flask import Blueprint, make_response, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()


client = OpenAI()


# async def main() -> None:
#     chat_completion = await client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Say this is a test",
#             }
#         ],
#         model="gpt-3.5-turbo",
#     )


# asyncio.run(main())


categorize = Blueprint("categorize", __name__)


@categorize.route("/healthcheck")
def healthcheck():
    return make_response("OK", 200)


# @categorize.route("/categorize", methods=["POST"])


def categorize_endpoint(data):
    """
    Categorize the question type and Costa's level of reasoning of a question given the context, using GPT-4.

    Args:
        summary (str): Summary of the question.
        previous_sentence (str): Previous sentence in the context.
        previous_speaker (str): Speaker of the previous sentence.
        question (str): Question to categorize.
        question_speaker (str): Speaker of the question.
        next_sentence (str): Next sentence in the context.
        next_speaker (str): Speaker of the next sentence.

    Returns:
        dict: A dictionary containing the question type and Costa's level of reasoning.
    """

    # data = request.json

    # Basic input validation
    required_fields = [
        "summary",
        "previous_sentence",
        "previous_speaker",
        "question",
        "question_speaker",
        "next_sentence",
        "next_speaker",
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Construct the messages to send to the language model

    system_role = """
    Given the following context and question from the speaker, determine the question type and Costa's level of reasoning.
    The question type should be categorized as Knowledge, Analyze, Apply, Create, Evaluate, Understand, Rhetorical, or Unknown.
    Costa's levels of reasoning should be categorized as 1 (gathering), 2 (processing), 3 (applying), or 0 (n/a).
    Provide the analysis in JSON format as specified.
    --- BEGIN USER MESSAGE ---
        Context: "$SUMMARY"
        Previous Sentence: "$PREVIOUS_SENTENCE"
        Speaker of Previous Sentence: "$PREVIOUS_SPEAKER"
        Question: "$QUESTION"
        Speaker of Question: "$QUESTION_SPEAKER"
        Next Sentence: "$NEXT_SENTENCE"
        Speaker of Next Sentence: "$NEXT_SPEAKER"
    --- END USER MESSAGE ---
    Analyze the question and output the results in the following JSON format,
    where QUESTION_TYPE is a str and QUESTION_LEVEL is an int (1, 2, 3, or 0):

    ---BEGIN FORMAT---
    {
        "question_type":"$QUESTION_TYPE",
        "question_level":"$QUESTION_LEVEL"
    }
    ---END FORMAT---
    """

    user_message = f"""
    Context: {data['summary']}
    Previous Sentence: {data['previous_sentence']}
    Speaker of Previous Sentence: {data['previous_speaker']}
    Question: {data['question']}
    Speaker of Question: {data['question_speaker']}
    Next Sentence: {data['next_sentence']}
    Speaker of Next Sentence: {data['next_speaker']}
    """

    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": user_message},
    ]

    # Call the OpenAI API with the prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=messages,
        temperature=0,
    )

    print(str(response.choices[0].message.content))

    # Extract the response and format it as JSON
    output = str(response.choices[0].message.content)

    # Parse the output JSON
    try:
        output_json = json.loads(output)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid response format from language model"}), 500

    return jsonify(output_json)


# Define your sample input data
sample_data = {
    "summary": "Context summary",
    "previous_sentence": "Previous sentence",
    "previous_speaker": "Speaker A",
    "question": "What is the capital of France?",
    "question_speaker": "Speaker B",
    "next_sentence": "Next sentence",
    "next_speaker": "Speaker C",
}

# Call the function with the sample data
result = categorize_endpoint(sample_data)

# Print the result
print(jsonify(result).data)
