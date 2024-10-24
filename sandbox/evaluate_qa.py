from langsmith import Client
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts.prompt import PromptTemplate
from langsmith.evaluation import LangChainStringEvaluator
from langchain_core.output_parsers import JsonOutputParser
from langsmith.schemas import Run, Example
from langsmith.evaluation import evaluate
import openai

# client = Client()

# Define dataset: these are your test cases
dataset_name = "QA Example Dataset v3"
# dataset = client.create_dataset(dataset_name)
# client.create_examples(
#     inputs=[
#         {"question": "What is LangChain?"},
#         {"question": "What is LangSmith?"},
#         {"question": "What is OpenAI?"},
#         {"question": "What is Google?"},
#         {"question": "What is Mistral?"},
#     ],
#     outputs=[
#         {"answer": "A framework for building LLM applications"},
#         {"answer": "A platform for observing and evaluating LLM applications"},
#         {"answer": "A company that creates Large Language Models"},
#         {"answer": "A technology company known for search"},
#         {"answer": "A company that creates Large Language Models"},
#     ],
#     dataset_id=dataset.id,
# )


_PROMPT_TEMPLATE = """You are an expert professor specialized in grading students' answers to questions.
You are grading the following question:
{query}
Here is the correct answer:
{answer}
You are grading the following predicted answer:
{result}
Respond with a grade between 0 and 10 based on accuracy. Do not provide any explanation.

Output JSON format:
  "grade": X
"""

PROMPT = PromptTemplate(
    input_variables=["query", "answer", "result"], template=_PROMPT_TEMPLATE
)
eval_llm = ChatVertexAI(model="gemini-1.5-flash", temperature=0.0)

chain = PROMPT | eval_llm | JsonOutputParser()


def evaluate_accuracy(run: Run, example: Example) -> dict:
    inputs = str(example.inputs.get("question"))
    prediction = run.outputs.get("output")
    required = example.outputs.get("answer")
    score = chain.invoke({"query": inputs, "answer": required, "result": prediction})
    return {"key": "pcc", "score": score["grade"]}


openai_client = openai.Client()


def my_app(question):
    return (
        openai_client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "Respond to the users question in a short, concise manner (one short sentence).",
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )
        .choices[0]
        .message.content
    )


def langsmith_app(inputs):
    output = my_app(inputs["question"])
    return {"output": output}


experiment_results = evaluate(
    langsmith_app,  # Your AI system
    data=dataset_name,  # The data to predict and grade over
    evaluators=[evaluate_accuracy],  # The evaluators to score the results
    experiment_prefix="openai-4o-mini",  # A prefix for your experiment names to easily identify them
)
