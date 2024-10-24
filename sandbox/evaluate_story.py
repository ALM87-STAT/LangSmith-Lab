from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langsmith.schemas import Run, Example
from langsmith.evaluation import evaluate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())

EVALUATION_PROMPT = """You are an expert professor specialized in grading students' answers to questions.
 
# Evaluation Criteria (Additive Score, 0-5):
1. Context: Award 1 point if the answer uses only information provided in the correct answer, without introducing external or fabricated details.
2. Completeness: Add 1 point if the answer addresses all key elements of the question based on the available correct answer, without omissions.
3. Conciseness: Add a final point if the answer uses the fewest words possible to address the question and avoids redundancy.
 
# Evaluation Steps:
1. Read provided the correct answer, question and answer carefully.
2. Go through each evaluation criterion one by one and assess whether the answer meets the criteria.
3. Compose your reasoning for each critera, explaining why you did or did not award a point. You can only award full points. 
4. Calculate the total score by summing the points awarded.
5. Format your evaluation response according to the specified Output format, ensuring proper JSON syntax with a "reasoning" field for your step-by-step explanation and a "total_score" field for the calculated total. Review your formatted response. It needs to be valid JSON.
 
# Output format:
"reasoning": "Your step-by-step explanation for the Evaluation Criteria, why you awarded a point or not.",
"total_score": sum of criteria scores

Now, grade the following question:
 
You are grading the following question:
{question}
Here is the correct answer:
{correct_answer}
You are grading the following predicted answer:
{answer}"""


evaluation_prompt_template = PromptTemplate(
    input_variables=["question", "correct_answer", "answer"],
    template=EVALUATION_PROMPT,
)

eval_llm = ChatVertexAI(model="gemini-1.5-flash", temperature=0.0)

llm_judges = evaluation_prompt_template | eval_llm | JsonOutputParser()


def evaluate_accuracy(run: Run, example: Example) -> dict:
    inputs = str(example.inputs.get("question"))
    prediction = run.outputs.get("output")
    required = example.outputs.get("answer")
    score = llm_judges.invoke(
        {"question": inputs, "correct_answer": required, "answer": prediction}
    )
    return {"key": "acc", "score": score["total_score"]}


APP_SYSTEM_PROMPT = """"Respond to the users question in a short, concise manner (one short sentence)."""

APP_USER_PROMPT = """{question}"""

# Target task definition
app_prompt_template = ChatPromptTemplate.from_messages(
    [("system", APP_SYSTEM_PROMPT), ("user", APP_USER_PROMPT)]
)

chat_model = ChatOpenAI(model="gpt-4-turbo")
output_parser = StrOutputParser()

chain = app_prompt_template | chat_model | output_parser

# The name or UUID of the LangSmith dataset to evaluate on.
# Alternatively, you can pass an iterator of examples
data = "QA Example Dataset v3"

# A string to prefix the experiment name with.
# If not provided, a random string will be generated.
experiment_prefix = "gpt-4-turbo-llm-judges"

# List of evaluators to score the outputs of target task
evaluators = [evaluate_accuracy]

# Evaluate the target task
results = evaluate(
    chain.invoke,
    data=data,
    evaluators=evaluators,
    experiment_prefix=experiment_prefix,
    num_repetitions=1,
    metadata={"version": "1.0.2", "revision_id": "beta"},
)
