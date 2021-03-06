# Dependencies
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.pipeline import Pipeline
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import StandardScaler


from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay
from sklearn.model_selection import cross_val_score


def select_columns(dataset, columns_to_keep):
    """Filters columns of `dataset` to keep only those specified by the `columns_to_keep` paramater

    Args:
        dataset (Pandas DataFrame): Dataset to filter
        columns_to_keep ( regex expression, str): columns names to keep

    Returns:
        Pandas Dataframe: Dataset with selected column(s)
    """
    column_filter = dataset.columns.str.replace(
        'android.sensor.|mean|std|min|max|#', '', regex=True).str.fullmatch(columns_to_keep)

    return dataset.loc[:, column_filter]


def drop_col_percent_na(dataset, threshold):
    """Drop columns missing value greater than `threshold`

    Args:
        dataset (Pandas Dataframe): Dataframe from which to drop columns
        threshold (float/int): Percentage of NaN beyong which a column should be dropped (from 1 to 100)

    Returns:
        Pandas Dataframe: Dataset with dropped column(s)
    """
    to_drop = (dataset.isnull().sum()/dataset.shape[0]*100) > threshold

    return dataset.loc[:, ~to_drop]


def pipelines(models):
    """Create pipelines made up preprocessors(Imputer, StandardScaler) and models

    Args:
        models (dict): A dictionary of model's name as key and sklearn corresponding algorithm as value

    Returns:
        dict: A dictionary of model's name as key and pipeline (preprocessing + model) as value
    """

    # Preprocessors
    imputer = IterativeImputer(random_state=0, max_iter=30)
    scaler = StandardScaler()

    # Pipelines of preprocessor(s) and models
    pipes = {name: Pipeline([
        ('imputer', imputer),
        ('scaler', scaler),
        ('model', model)
    ]) for name, model in models.items()}

    return pipes

# Model performance
@ignore_warnings(category=ConvergenceWarning)
def perfomance(pipes, X_train, y_train, X_test, y_test):
    """Compute mean and std of cross validation scores, accuracy on test set
       as well as training and predicting time
    Args: pipes(dict); as defined in `pipelines` function.
          X_train, y_train; training sets
          X_test, y_test; test sets
    Returns:
        Pandas Dataframe: Dataframe of computed performance metrics sorted by accuracy on test set
    """
    results = pd.DataFrame()

    for name, model in pipes.items():

        # training time
        t0 = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - t0

        # predicting time
        t0 = time.time()
        preds = model.predict(X_test)
        pred_time = time.time() - t0

        # cross validation
        scores = cross_val_score(model, X_train, y_train)

        # append to results
        results = pd.concat([results, pd.DataFrame({'name': [name],
                                                    'mean_score': [scores.mean()],
                                                    'std_score':[scores.std()],
                                                    'test_accuracy': [accuracy_score(y_test, preds)],
                                                    'training_time': [train_time],
                                                    'predicting_time': [pred_time]})
                             ])

    return results.sort_values(by='test_accuracy', ascending=False)