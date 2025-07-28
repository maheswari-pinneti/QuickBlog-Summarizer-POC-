from transformers import pipeline

def get_model(language: str = 'english', model_name: str = None):
    """
    Returns a HuggingFace summarization pipeline based on language and model name.
    """
    language = language.lower()

    if language == 'english':
        model_name = model_name or 'sshleifer/distilbart-cnn-12-6'
    elif language == 'hindi':
        model_name = model_name or 'csebuetnlp/mT5_multilingual_XLSum'
    else:
        model_name = model_name or 'facebook/bart-large-cnn'

    return pipeline("summarization", model=model_name)
