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
        try:
            data = (
                pd.read_csv(file_path)
                if file_path.endswith(".csv")
                else pd.read_excel(file_path)
            )
        except Exception as e:
            return f"Error loading file: {str(e)}"

        try:
            # Train the model and make predictions
            churn_model = TrainModel.ChurnModel(data, target_column)
            churn_model.preprocess_data()
            churn_model.train_model()
            result = churn_model.predict()
            accuracy = churn_model.evaluate_model()

            # Generate the pie chart for churn distribution
            pie_chart = churn_model.generate_pie_chart()
            # Generate the feature importance chart
            feature_importance = churn_model.generate_feature_importance_chart()
            # Generate the histogram for feature distribution
            histogram = churn_model.generate_histogram()
            # Return both the result and charts
            return {
                "accuracy": accuracy,
                "pie_chart": pie_chart,
                "histogram": histogram,
                "feature_importance": feature_importance,
            }
        except Exception as e:
            return f"Error in churn prediction: {str(e)}"
