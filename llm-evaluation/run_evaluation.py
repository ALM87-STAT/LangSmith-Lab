from src.evaluation.evaluators import Evaluators
from src.models.chains import CreateChain
from langsmith.evaluation import evaluate
from src.config.config_loader import ConfigLoader
from dotenv import load_dotenv


def main():
    # Cargar configuración
    load_dotenv()
    config = ConfigLoader().get_config

    # Inicializar componentes
    chain = CreateChain()

    # Inicializar evaluadores
    evaluator = Evaluators(chain.eval_chain)

    # Ejecutar evaluación
    results = evaluate(
        chain.app_chain.invoke,
        data=config.evaluation.dataset.name,
        evaluators=[evaluator.correctness],
        experiment_prefix=config.evaluation.experiment.prefix,
        num_repetitions=config.evaluation.experiment.num_repetitions,
        metadata=config.evaluation.experiment.metadata,
    )


if __name__ == "__main__":
    main()
