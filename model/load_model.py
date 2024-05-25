from tensorflow.keras.models import load_model

def get_model():
    model = load_model('model/gesture_model.h5')
    return model
