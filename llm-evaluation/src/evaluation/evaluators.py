from langsmith.schemas import Run, Example


class Evaluators:
    def __init__(self, llm_chain):
        self.llm_chain = llm_chain

    def correctness(self, run: Run, example: Example) -> dict:
        asistente = run.outputs.get("output")
        experto = example.outputs.get("output")

        score = self.llm_chain.invoke({"experto": experto, "asistente": asistente})

        return {"key": "correctness score", "score": score["total_score"]}
