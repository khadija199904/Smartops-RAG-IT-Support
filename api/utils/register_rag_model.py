import mlflow, pickle, os, tempfile
from pipelineRAG.retrieval import build_rag_chain
from api.core.config import MLFLOW_TRACKING_URI
    
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Smartops-RAG-Model-Registry")


def register_rag_pipeline(model_name="smartops-rag-pipeline"):
    

    with mlflow.start_run(run_name="rag_pipeline_registration") as run:
        rag_chain = build_rag_chain()
        temp_dir = tempfile.mkdtemp()
        pipeline_file = os.path.join(temp_dir, "rag_pipeline.pkl")

        with open(pipeline_file, "wb") as f:
            pickle.dump(rag_chain, f)

        mlflow.log_artifact(pipeline_file, artifact_path="pipeline")
        artifact_uri = mlflow.get_artifact_uri("pipeline/rag_pipeline.pkl")

        try:
            mlflow.register_model(model_uri=artifact_uri, name=model_name)
        except Exception as e:
            print(f" Nouvelle version ou erreur: {e}")

        mlflow.set_tag("model_type", "RAG_Pipeline")
        run_id = run.info.run_id

        os.remove(pipeline_file)
        os.rmdir(temp_dir)
        return run_id
