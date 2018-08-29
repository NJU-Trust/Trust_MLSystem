from sklearn.externals import joblib
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import metrics
from hep_ml.nnet import MLPRegressor
def load_data():
    diabetes = datasets.load_boston()
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data, diabetes.target, test_size=0.20, random_state=0)
    return X_train, X_test, y_train, y_test

def predict():
    X_train,X_test,y_train,y_test=load_data()
    abc = joblib.load('logit.pkl')
    y_pred = abc.predict(X_test)
    return str(metrics.mean_squared_error(y_test, y_pred))
