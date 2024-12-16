import pandas as pd  # To get the data
from app.middleware import TrainModel


class FileProcessor:
    @staticmethod
    def UploadFile(file_path, target_column):
        """
        Handles the uploaded file path and processes it based on file type.
        """
        if file_path.endswith(".csv") or file_path.endswith(".xlsx"):
            return FileProcessor.Churn(file_path, target_column)
        else:
            return "File type not supported"

    @staticmethod
    def Churn(file_path, target_column):
        """
        Processes churn prediction for CSV or Excel files.
        Load the dataset from the file path.
        """
        data = (
            pd.read_csv(file_path)
            if file_path.endswith(".csv")
            else pd.read_excel(file_path)
        )
        # Train the model and make predictions
        churn_model = TrainModel.ChurnModel(data, target_column)
        churn_model.preprocess_data()
        churn_model.train_model()
        result = churn_model.predict()
        # print(f"Result: {result}")
        # print(result)
        return result
