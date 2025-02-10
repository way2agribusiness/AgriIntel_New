from keras.models import load_model
from keras.optimizers import Adam

def load_pretrained_model(model_path):
    return load_model(model_path, compile=False)