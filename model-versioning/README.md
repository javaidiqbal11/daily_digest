# MLflow Complete Example Flow

This directory contains a complete MLflow learning example tailored for model versioning and tracking.

## Overview
MLflow is an open-source platform to manage the ML lifecycle, including experimentation, reproducibility, deployment, and a central model registry.

### Features Covered:
1. **Experiment Tracking**: Logging parameters, metrics, and models.
2. **Model Evaluation**: Metrics calculation like RMSE, R2, and MAE.
3. **Artifact Logging**: Storing the trained ML models.

## How to Run the Example

### 1. Install Requirements
Make sure you have installed the necessary libraries:
```bash
pip install mlflow scikit-learn pandas numpy
```

### 2. Run the Script
You can run the script with different parameters to simulate different experiment runs. The script takes `alpha` and `l1_ratio` as arguments.

Run 1: Default parameters
```bash
python example_mlflow.py
```

Run 2: Changing `alpha`
```bash
python example_mlflow.py 0.1 0.5
```

Run 3: Changing `alpha` and `l1_ratio`
```bash
python example_mlflow.py 0.8 0.2
```

### 3. View the MLflow UI
After running the script, a folder named `mlruns` will be created in this directory. 
To visualize the experiments and logged runs, start the MLflow server:
```bash
mlflow ui
```
Then, open your browser and navigate to `http://localhost:5000`. You will see the **Wine Quality ElasticNet** experiment and their respective runs, logged parameters, and metrics.

### 4. Advanced: Using a Model Registry
By default, the script logs to the local `mlruns` file directory. If you want to use the **Model Registry** to version models (e.g., Staging, Production), you must start the MLflow tracking server with a database backend:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
```
Then, uncomment line 46 in `example_mlflow.py` and set the tracking URI:
```python
mlflow.set_tracking_uri("http://localhost:5000")
```
Running the script again will automatically register your model as `ElasticnetWineModel` because the registry supports database backends.
