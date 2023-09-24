# Project Name
* Insurance Premium Prediction

#### Project Status: [Completed]

## Project Objective
The purpose of this project is to predict insurance premium based on attributes like Sex, BMI, Region etc.

### Methods Used
* XGBoost Regressor

### Technologies
* Python
* Pandas, Numpy
* Sklearn, Xgb
* Streamlit
* MongoDB

## Project Description
* The purpose of this project is to predict insurance premium based on attributes like Sex, BMI, Region etc.
* The data has been taken from https://www.kaggle.com/datasets/noordeen/insurance-premium-prediction
* After trying various learning algorithms, XGBoost regressor has been used to perform insurance premium prediction in this project.
* This project gets the data from MongoDB database during data ingestion stage.
* Streamlit has been used to develop a simple web app to perform model predictions.

## Getting Started

1. Raw Data is kept in [insurance.csv].

2. Data Ingestion scripts are kept in [ippredictor\components\data_ingestion.py]
    
3. Data transformation scripts are kept in [ippredictor\components\data_transformation.py]

4. Data validation scripts are kept in [ippredictor\components\data_validation.py]

5. Model training scripts are kept in [ippredictor\components\model_trainer.py]

6. Model evaluation scripts are kept in [ippredictor\components\model_evaluation.py]

7. MongoDB configuration is kept in [ippredictor\config.py]

8. Streamlit web app is configured in [app.py]

## Featured Notebooks/Analysis/Deliverables
* [ippredictor\pipeline\training_pipeline.py] is the training pipeline that is responsible for training the model.

## Contact
* Name :- Pradeep.P 
* Mobile :- 8197607412
* Email :- pradeep.pvj8@gmail.com