import io
import base64
from flask import jsonify
import pandas as pd  # To get the data
from app.middleware import TrainModel


class FileProcessor:
    def __init__(self, file_path: str, target_column: str):
        self.UploadFile(file_path, target_column)

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
        try:
            data = (
                pd.read_csv(file_path)
                if file_path.endswith(".csv")
                else pd.read_excel(file_path)
            )
        except Exception as e:
            return f"Error loading file: {str(e)}"

        try:
            churn_model = TrainModel.ChurnModel(data, target_column)
            churn_model.preprocess_data()
            churn_model.train_model()
            churn_model.predict()
            accuracy = churn_model.evaluate_model()

            # Generate charts
            pie_chart = churn_model.generate_pie_chart()
            feature_importance = churn_model.generate_feature_importance_chart()
            histogram = churn_model.generate_histogram()

            # If charts are images, convert them to base64
            pie_chart_base64 = FileProcessor.to_base64(pie_chart)
            feature_importance_base64 = FileProcessor.to_base64(feature_importance)
            histogram_base64 = FileProcessor.to_base64(histogram)

            # Return a JSON-serializable dictionary
            return {
                "accuracy": accuracy,
                "pie_chart": pie_chart_base64,
                "feature_importance": feature_importance_base64,
                "histogram": histogram_base64,
            }

        except Exception as e:
            return f"Error in churn prediction: {str(e)}"

    @staticmethod
    def to_base64(image):
        """Convert an image to a base64-encoded string."""
        if isinstance(image, bytes):
            return base64.b64encode(image).decode("utf-8")
        elif isinstance(image, str):
            return image  # Assume the image is already base64 encoded
        else:
            raise ValueError("Image is not in a valid format")
