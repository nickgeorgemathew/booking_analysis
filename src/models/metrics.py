from sklearn.metrics import f1_score, accuracy_score, confusion_matrix

def evaluate(y_true, y_pred):
    return {
        'f1': f1_score(y_true, y_pred),
        'accuracy': accuracy_score(y_true, y_pred),
        'confusion_matrix': confusion_matrix(y_true, y_pred)
    }
