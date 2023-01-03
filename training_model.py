import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import cv2

dt = ['right', 'left', 'front', 'back', 'stop', 'none']

dat=pd.read_csv(f"D:/Programming/VS Code/Python/pdc/trainData/train_set_mask.csv")
dat.columns=range(3601)

x = dat.drop(columns=3600)
x = x/255.
print(x)
y = dat[3600]
print(y)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=1)

train=RandomForestClassifier()
# train = LinearRegression()
# train=DecisionTreeClassifier(criterion='gini', random_state=6, max_depth=6, min_samples_leaf=6)
# train=DecisionTreeClassifier(criterion='entropy', random_state=1, max_depth=7, min_samples_leaf=6)
train.fit(x_train, y_train)

mdl_name = "RFC_Model_HandSigns_mask.joblib"
# mdl_name = "1LR_Model_HandSigns.joblib"
# mdl_name = "10-7DTC_gini_Model_HandSigns.joblib"
# mdl_name = "1DTC_entropy_Model_HandSigns.joblib"

#1 3 10

joblib.dump(train, mdl_name)

# ld_model = joblib.load(mdl_name)
# print("coef",train.coef_)
# print("score",train.score(x_test, y_test))

pr = train.predict(x_test)
print(pr)
print(accuracy_score(pr, y_test))

# print(train.score(x_test, y_test))

print(y_test)
# print(pr)
