
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# بارگذاری داده‌ها
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
# ایجاد و آموزش مدل
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# پیش‌بینی
y_pred = model.predict(X_test)

# ارزیابی مدل
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=data.target_names)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("\nClassification Report:\n", report)
print("\nConfusion Matrix:\n", conf_matrix)

# ذخیره مدل
with open('breast_cancer.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('breast_cancer.pkl','rb') as f:
    model = pickle.load(f)

def predict_class(features):
    predictions = model.predict([features])
    return predictions[0]
import pickle

# Load the model
with open('breast_cancer.pkl', 'rb') as f:
    model = pickle.load(f)

# Function to predict the class and return descriptive result
def predict_class(features):
    predictions = model.predict([features])
    if predictions[0] == 0:
        return "Benign (خوش‌خیم)"
    else:
        return "Malignant (بدخیم)"
