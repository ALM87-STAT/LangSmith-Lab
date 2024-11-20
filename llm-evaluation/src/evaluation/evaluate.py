import pandas as pd
from typing import Dict, Any
import tqdm


class LLMEvaluate:

    def _init_(
        self,
        llm_chain,
        reference_data_path: str,
        evaluation_data_path: str,
        config: Dict[str, Any],
    ):
        self.llm_chain = llm_chain
        self.reference_data = pd.read_csv(reference_data_path)
        self.evaluation_data = pd.read_csv(evaluation_data_path)
        self.config = config
        self.num_repetitions = self.config.evaluation.experiment.num_repetitions

    def evaluate(self, evaluator) -> None:
        for idx, row in tqdm.tqdm(
            self.reference_data.iterrows(), total=len(self.reference_data)
        ):
            example_id = row["example_id"]
            context = row["context"]
            input = row["input"]
            reference_output = row["reference_output"]

            for repetition in range(self.num_repetitions):
                app_output = self.__app_responses(context, input)
                evaluation_output = evaluator(reference_output, app_output)

                new_row = {
                    "experiment_tag": self.config.evaluation.experiment.prefix,
                    "example_id": example_id,
                    "replication": repetition,
                    "model": self.config.models.application.provider,
                    "temperature": self.config.models.application.parameters.temperature,
                    "app_output": app_output,
                    "reasoning": evaluation_output["reasoning"],
                    "score": evaluation_output["total_score"],
                }

                self.evaluation_data = pd.concat(
                    [self.evaluation_data, pd.DataFrame([new_row])], ignore_index=True
                )

                self.__save_results()

    def __app_responses(self, context: str, input: str):
        responses = self.llm_chain.invoke({"context": context, "requirements": input})

        return responses

    def __save_results(self):
        self.results_db.to_csv(self.output_path, index=False)
