from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith.evaluation import evaluate, LangChainStringEvaluator

# Target task definition
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Respond to the users question in a short, concise manner (one short sentence).",
        ),
        ("user", "{question}"),
    ]
)
chat_model = ChatOpenAI(model="gpt-4-turbo")
output_parser = StrOutputParser()

chain = prompt | chat_model | output_parser

# The name or UUID of the LangSmith dataset to evaluate on.
# Alternatively, you can pass an iterator of examples
data = "QA Example Dataset v2"

# A string to prefix the experiment name with.
# If not provided, a random string will be generated.
experiment_prefix = "gpt-4-turbo"

# List of evaluators to score the outputs of target task
evaluators = [LangChainStringEvaluator("cot_qa")]

# Evaluate the target task
results = evaluate(
    chain.invoke,
    data=data,
    evaluators=evaluators,
    experiment_prefix=experiment_prefix,
    num_repetitions=1,
    metadata={"version": "1.0.0", "revision_id": "beta"},
)
