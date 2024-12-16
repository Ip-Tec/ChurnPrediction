import joblib
import base64
import pandas as pd
import seaborn as sns
from io import BytesIO
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


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

        # Fill missing values for numerical columns
        self.data = self.data.fillna(self.data.select_dtypes(include="number").mean())

        # Fill missing values for categorical columns with the mode
        if "Region" in self.data.columns:
            self.data["Region"] = self.data["Region"].fillna(
                self.data["Region"].mode()[0]
            )
        if "Gender" in self.data.columns:
            self.data["Gender"] = self.data["Gender"].fillna(
                self.data["Gender"].mode()[0]
            )

        # One-hot encode categorical columns
        self.data = pd.get_dummies(
            self.data, columns=["Region", "Gender"], drop_first=True
        )

        # Split into features (X) and target (y)
        X = self.data.drop(self.target_column, axis=1)
        y = self.data[self.target_column]

        # Check for nulls in the target column
        if y.isnull().any():
            raise ValueError(
                f"Target column '{self.target_column}' contains null values"
            )

        # Encode target column if necessary
        if y.dtype == "object":
            le = LabelEncoder()
            y = le.fit_transform(y)

        # Ensure only numerical columns are passed to the scaler
        numeric_features = X.select_dtypes(include=["float64", "int64"]).columns
        X = X[numeric_features]

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

    def predict(self):
        """Make predictions on the test set."""
        if self.model is None:
            print("Model not trained. Please run train_model() first.")
            raise ValueError("Model not trained")
        return self.model.predict(self.X_test)

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

    def generate_pie_chart(self):
        """Generate a pie chart for the target column."""
        churn_counts = self.data[self.target_column].value_counts()
        plt.figure(figsize=(6, 6))
        churn_counts.plot.pie(
            autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff"]
        )
        plt.title("Churn Distribution")
        plt.ylabel("")  # Hide the y-label

        # Convert plot to PNG image
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode("utf-8")

    def generate_histogram(self):
        """Generate a histogram for feature distribution."""
        plt.figure(figsize=(8, 6))
        self.data[self.target_column].hist(bins=30, color="#66b3ff", edgecolor="black")
        plt.title(f"Distribution of {self.target_column}")
        plt.xlabel(self.target_column)
        plt.ylabel("Frequency")

        # Convert plot to PNG image
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode("utf-8")

    def generate_feature_importance_chart(self):
        """Generate a feature importance chart from the trained model."""
        if self.model is None:
            raise ValueError("Model not trained. Please run train_model() first.")

        importances = self.model.feature_importances_
        feature_names = self.X_train.columns

        plt.figure(figsize=(10, 6))
        sns.barplot(x=importances, y=feature_names, palette="viridis")
        plt.title("Feature Importance")
        plt.xlabel("Importance")
        plt.ylabel("Features")

        # Convert plot to PNG image
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode("utf-8")

    def generate_prediction_table(self):
        """Generate a table of predictions alongside actual values."""
        y_pred = self.predict()
        result_df = pd.DataFrame({"Actual": self.y_test, "Predicted": y_pred})
        return result_df.to_html(classes="table table-striped")

    def send_churn_results(self):
        """Generate and return all the visualizations and tables."""
        pie_chart = self.generate_pie_chart()
        histogram = self.generate_histogram()
        feature_importance = self.generate_feature_importance_chart()
        prediction_table = self.generate_prediction_table()

        return {
            "pie_chart": pie_chart,
            "histogram": histogram,
            "feature_importance": feature_importance,
            "prediction_table": prediction_table,
        }
