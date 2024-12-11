import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Define a Blueprint for modular application structure and routing
from flask import Blueprint

main = Blueprint("main", __name__)


class ChurnModel:
    def __init__(self, data: pd.DataFrame, target_column: str):
        """
        Initialize the ChurnModel with data and the target column name.

        :param data: Pandas DataFrame containing the dataset.
        :param target_column: Name of the target column for churn prediction.
        """
        self.data = data
        self.target_column = target_column
        self.model = None
        self.scaler = None
        self.X_train, self.X_test, self.y_train, self.y_test = (None, None, None, None)

    def preprocess_data(self):
        """Preprocess the dataset: encode, scale, and split."""
        # Drop unnecessary columns (customize as needed)
        self.data = self.data.drop(["RowNumber", "CustomerId", "Surname"], axis=1)

        # One-hot encode categorical columns
        self.data = pd.get_dummies(
            self.data, columns=["Geography", "Gender"], drop_first=True
        )

        # Split into features (X) and target (y)
        X = self.data.drop(self.target_column, axis=1)
        y = self.data[self.target_column]

        # Split into training and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Standardize features
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

    def train_model(self):
        """Train a Random Forest classifier on the preprocessed data."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)
        print("Model training completed.")

    def evaluate_model(self):
        """Evaluate the model's performance on the test set."""
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")
        return accuracy

    def save_artifacts(self, model_path="churn_model.pkl", scaler_path="scaler.pkl"):
        """
        Save the trained model and scaler to disk.

        :param model_path: File path to save the model.
        :param scaler_path: File path to save the scaler.
        """
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        print(f"Model saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
