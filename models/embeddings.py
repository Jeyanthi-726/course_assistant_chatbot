from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """Return a sentence embedding model"""
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)
