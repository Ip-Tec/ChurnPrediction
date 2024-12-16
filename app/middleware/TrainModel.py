import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class ChurnModel:
    def __init__(self, data: pd.DataFrame, target_column: str):
        """
        Initialize the ChurnModel with data and the target column name.

        :param data: Pandas DataFrame containing the dataset.
        :param target_column: Name of the target column for churn prediction.
        """
        # print(
        # f"Initializing ChurnModel with data shape: {str(data.shape)} and target_column: {target_column}"
        # )
        self.data = data
        self.target_column = target_column
        self.model = None
        self.scaler = None
        self.X_train, self.X_test, self.y_train, self.y_test = (None, None, None, None)

        # Validate target column
        if self.target_column not in self.data.columns:
            # print(f"Target column '{self.target_column}' not found in the dataset.")
            raise ValueError(
                f"Target column '{self.target_column}' not found in the dataset"
            )

    def preprocess_data(self):
        """Preprocess the dataset: encode, scale, and split."""
        # Drop unnecessary columns
        self.data = self.data.drop(
            columns=[
                col
                for col in ["RowNumber", "CustomerId", "Surname"]
                if col in self.data
            ],
            errors="ignore",
        )

        # Handle missing values in features (fill with mean or drop rows)
        self.data = self.data.fillna(self.data.mean())

        # One-hot encode categorical columns
        self.data = pd.get_dummies(
            self.data, columns=["Geography", "Gender"], drop_first=True
        )

        # Split into features (X) and target (y)
        X = self.data.drop(self.target_column, axis=1)
        y = self.data[self.target_column]

        # Check for nulls in the target column
        if y.isnull().any():
            # print(f"Target column '{self.target_column}' contains null values")
            raise ValueError(
                f"Target column '{self.target_column}' contains null values"
            )

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
        if self.X_train is None or self.y_train is None:
            print("Data not preprocessed. Please run preprocess_data() first.")
            raise ValueError("Data not preprocessed")

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)
        print("Model training completed.")

    def evaluate_model(self):
        """Evaluate the model's performance on the test set."""
        if self.model is None:
            print("Model not trained. Please run train_model() first.")
            raise ValueError("Model not trained")

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
        if self.model is None:
            print("Model not trained. Please run train_model() first.")
            raise ValueError("Model not trained")

        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        # print(f"Model saved to {model_path}")
        # print(f"Scaler saved to {scaler_path}")
