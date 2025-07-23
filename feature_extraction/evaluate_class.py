import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

dataset_path = "pose_data_with_angles.csv" #pick dataset
df = pd.read_csv(dataset_path, header=None).dropna()

df = df[df.apply(lambda row: all(pd.to_numeric(row[:-1], errors='coerce').notna()), axis=1)]

X = df.iloc[:, :-1].astype(float) 
y = df.iloc[:, -1].astype(str)    

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42)

classifiers = {
    "nb": GaussianNB(),
    "lr": LogisticRegression(max_iter=1000),
    "dt": DecisionTreeClassifier(random_state=42),
}

for name, clf in classifiers.items():
    print(f"\nTraining: {name.upper()}")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_, zero_division=0))

    model_file = f"{name}_model.pkl"
    joblib.dump(clf, model_file)

joblib.dump(encoder, "encoder.pkl")
joblib.dump(scaler, "scaler.pkl")
