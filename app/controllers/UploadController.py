import pandas as pd  # For data manipulation and analysis
from sklearn.metrics import accuracy_score  # To evaluate the accuracy of the model
from sklearn.model_selection import train_test_split  # For splitting the dataset
from sklearn.ensemble import (
    RandomForestClassifier,
)  # Random Forest model for prediction
from sklearn.preprocessing import (
    StandardScaler,
)  # To standardize features by removing the mean and scaling to unit variance


class FileProcessor:
    @staticmethod
    def UploadFile(file_path):
        """
        Handles the uploaded file path and processes it based on file type.
        """
        if file_path.endswith(".csv") or file_path.endswith(".xlsx"):
            return FileProcessor.Churn(file_path)
        else:
            return "File type not supported"

    @staticmethod
    def Churn(file_path):
        """
        Processes churn prediction for CSV or Excel files.
        """
        result = FileProcessor.ChurnPredictionModel(file_path)
        return result

    @staticmethod
    def ChurnPredictionModel(file_path):
        """
        Analyzes data and predicts churn users based on the provided dataset.
        """
        # Read the file into a DataFrame based on its type
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            return "File type not supported"

        # Drop unnecessary columns
        if set(["RowNumber", "CustomerId", "Surname"]).issubset(df.columns):
            df = df.drop(["RowNumber", "CustomerId", "Surname"], axis=1)

        # Convert categorical data to numerical format using one-hot encoding
        df = pd.get_dummies(df, columns=["Geography", "Gender"])

        # Split the data into features (X) and target (y)
        if "Exited" not in df.columns:
            return "Error: The dataset does not contain the required 'Exited' column."

        X = df.drop("Exited", axis=1)  # Features: All columns except "Exited"
        y = df["Exited"]  # Target: "Exited" column

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Standardize the features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Train the Random Forest classifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict churn on the testing data
        y_pred = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)

        # Return the results
        return {
            "accuracy": accuracy,
            "predictions": y_pred.tolist(),  # Convert numpy array to list for JSON serialization
        }
