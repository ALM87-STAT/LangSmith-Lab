import pandas as pd
from typing import List, Dict, Any
import json
from datetime import datetime


class LLMEvaluator:
    def __init__(self, judge_model, reference_data_path: str, output_path: str):
        """
        Inicializa el evaluador de LLM.

        Args:
            judge_model: Modelo LLM que actuará como juez
            reference_data_path: Ruta al archivo CSV con los datos de referencia
            output_path: Ruta donde se guardarán los resultados
        """
        self.judge_model = judge_model
        self.reference_data = pd.read_csv(reference_data_path)
        self.output_path = output_path
        self.results_db = pd.DataFrame(
            columns=[
                "input_id",
                "input_text",
                "reference_output",
                "model_output",
                "replica_number",
                "evaluation_score",
                "evaluation_feedback",
                "timestamp",
            ]
        )

    def generate_evaluation_prompt(
        self, input_text: str, reference_output: str, model_output: str
    ) -> str:
        """
        Genera el prompt para el modelo juez.
        """
        return f"""Por favor evalúa la siguiente respuesta del modelo en una escala del 1 al 10, donde 10 es perfecto.
        
        Input del usuario: {input_text}
        
        Respuesta de referencia: {reference_output}
        
        Respuesta del modelo a evaluar: {model_output}
        
        Proporciona tu evaluación en el siguiente formato JSON:
        {{
            "score": <puntaje del 1-10>,
            "feedback": "<explicación detallada de la evaluación>"
        }}
        """

    def evaluate_response(
        self,
        model_to_evaluate,
        input_text: str,
        reference_output: str,
        replica_number: int,
    ) -> Dict[str, Any]:
        """
        Evalúa una respuesta individual del modelo.
        """
        # Generar respuesta del modelo a evaluar
        model_output = model_to_evaluate(input_text)

        # Generar prompt para el juez
        evaluation_prompt = self.generate_evaluation_prompt(
            input_text, reference_output, model_output
        )

        # Obtener evaluación del juez
        judge_response = self.judge_model(evaluation_prompt)

        try:
            evaluation = json.loads(judge_response)
        except json.JSONDecodeError:
            evaluation = {
                "score": 0,
                "feedback": "Error al parsear la respuesta del juez",
            }

        return {
            "model_output": model_output,
            "evaluation_score": evaluation["score"],
            "evaluation_feedback": evaluation["feedback"],
        }

    def run_evaluation(self, model_to_evaluate, num_replicas: int = 5):
        """
        Ejecuta la evaluación completa para todos los inputs con múltiples réplicas.
        """
        for idx, row in self.reference_data.iterrows():
            input_text = row["input"]
            reference_output = row["output_reference"]

            for replica in range(num_replicas):
                # Evaluar la respuesta
                evaluation_result = self.evaluate_response(
                    model_to_evaluate, input_text, reference_output, replica
                )

                # Agregar resultados a la base de datos
                new_row = {
                    "input_id": idx,
                    "input_text": input_text,
                    "reference_output": reference_output,
                    "model_output": evaluation_result["model_output"],
                    "replica_number": replica,
                    "evaluation_score": evaluation_result["evaluation_score"],
                    "evaluation_feedback": evaluation_result["evaluation_feedback"],
                    "timestamp": datetime.now().isoformat(),
                }

                self.results_db = pd.concat(
                    [self.results_db, pd.DataFrame([new_row])], ignore_index=True
                )

                # Guardar resultados parciales
                self.save_results()

    def save_results(self):
        """
        Guarda los resultados en un archivo CSV.
        """
        self.results_db.to_csv(self.output_path, index=False)

    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Genera estadísticas resumidas de las evaluaciones.
        """
        summary = {
            "mean_score": self.results_db["evaluation_score"].mean(),
            "std_score": self.results_db["evaluation_score"].std(),
            "median_score": self.results_db["evaluation_score"].median(),
            "total_evaluations": len(self.results_db),
            "evaluations_per_input": self.results_db.groupby("input_id").size().mean(),
            "timestamp": datetime.now().isoformat(),
        }

        return summary


# Inicializar el evaluador
evaluator = LLMEvaluator(
    judge_model=my_judge_model,
    reference_data_path="reference_data.csv",
    output_path="evaluation_results.csv",
)

# Ejecutar evaluación
evaluator.run_evaluation(model_to_evaluate=my_model_to_evaluate)

# Obtener estadísticas
summary = evaluator.get_summary_statistics()
print(summary)

########################################################################


import random
import pandas as pd


class LLMEvaluator:
    def __init__(self, input_output_db):
        """
        Inicializa la clase con la base de datos de input-output.

        Args:
        input_output_db (pd.DataFrame): DataFrame con 'input' y 'output_reference'.
        """
        self.input_output_db = input_output_db
        self.generated_responses_db = pd.DataFrame(
            columns=["input", "output_generated", "score"]
        )

    def generate_responses(self, input_text, n=5):
        """
        Genera múltiples respuestas para un input dado usando el modelo LLM.

        Args:
        input_text (str): El texto de entrada para el modelo LLM.
        n (int): El número de réplicas a generar.

        Returns:
        List[str]: Una lista con las respuestas generadas.
        """
        # Pseudocódigo para generación de respuestas (simulado)
        responses = [f"Response {i} to '{input_text}'" for i in range(1, n + 1)]
        return responses

    def judge_response(self, input_text, generated_response, reference_output):
        """
        Usa el modelo LLM-as-judge para evaluar una respuesta generada.

        Args:
        input_text (str): El texto de entrada original.
        generated_response (str): La respuesta generada por el modelo.
        reference_output (str): La respuesta de referencia correcta.

        Returns:
        float: Una puntuación de evaluación.
        """
        # Pseudocódigo para la evaluación (simulado)
        score = random.uniform(
            0, 1
        )  # Genera una puntuación aleatoria entre 0 y 1 para simular
        return score

    def evaluate_all(self):
        """
        Evalúa todas las entradas en la base de datos input-output y guarda las respuestas generadas y sus evaluaciones.
        """
        for idx, row in self.input_output_db.iterrows():
            input_text = row["input"]
            reference_output = row["output_reference"]

            # Genera 5 respuestas para cada input
            responses = self.generate_responses(input_text, n=5)

            # Evalúa cada respuesta generada y guarda en la base de datos
            for response in responses:
                score = self.judge_response(input_text, response, reference_output)
                new_row = {
                    "input": input_text,
                    "output_generated": response,
                    "score": score,
                }
                self.generated_responses_db = self.generated_responses_db.append(
                    new_row, ignore_index=True
                )

    def save_generated_responses(self, file_path):
        """
        Guarda la base de datos de respuestas generadas y evaluadas en un archivo CSV.

        Args:
        file_path (str): Ruta del archivo donde se guardarán los datos.
        """
        self.generated_responses_db.to_csv(file_path, index=False)
