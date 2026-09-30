import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# -------------------------------------------------
# 1. Read DVC dataset version
# -------------------------------------------------

with open("data/diabetes.csv.dvc", "r") as file:
    dvc_version = file.read().strip()


# -------------------------------------------------
# 2. Load the dataset
# -------------------------------------------------

data = pd.read_csv("data/diabetes.csv")


# -------------------------------------------------
# 3. Separate features and target
# -------------------------------------------------

X = data[["glucose", "bloodpressure"]]
y = data["diabetes"]


# -------------------------------------------------
# 4. Split the dataset into training and testing
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -------------------------------------------------
# 5. Create MLflow experiment
# -------------------------------------------------

mlflow.set_experiment("My_First_ML_Project")


# -------------------------------------------------
# 6. Start MLflow run
# -------------------------------------------------

with mlflow.start_run():

    # Model parameter
    n_estimators = 100

    # Create Random Forest model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=42
    )

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)


    # -------------------------------------------------
    # 7. Log DVC dataset version
    # -------------------------------------------------

    mlflow.log_param(
        "dataset_version",
        dvc_version
    )


    # -------------------------------------------------
    # 8. Log Random Forest parameter
    # -------------------------------------------------

    mlflow.log_param(
        "n_estimators",
        n_estimators
    )


    # -------------------------------------------------
    # 9. Log accuracy
    # -------------------------------------------------

    mlflow.log_metric(
        "accuracy",
        accuracy
    )


    # -------------------------------------------------
    # 10. Log the trained Random Forest model
    # -------------------------------------------------

    mlflow.sklearn.log_model(
        model,
        name="random_forest_model",
        skops_trusted_types=[
            "sklearn.tree._tree.Tree"
        ]
    )


    # -------------------------------------------------
    # 11. Print results
    # -------------------------------------------------

    print("Experiment tracked in MLflow!")
    print("DVC dataset version:")
    print(dvc_version)
    print(f"Accuracy: {accuracy:.4f}")