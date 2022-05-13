# Dependencies
from tqdm import tqdm

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler, QuantileTransformer


from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, balanced_accuracy_score, f1_score, recall_score, precision_score
from sklearn.model_selection import cross_val_score


# Select columns
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


# drop column(s) based on missing value percentage
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


# Split train test sets
def split_train_test(data, upper_boundary=1, lower_boundary=3, nb_users_test=3):
    """Split `data` into train and test sets based on users. Users with highest number of
    records as well as very few numbers of records are excluded from being choosen for the test set.

    Args:
        data (Pandas DataFrame): Dataset to split
        upper_boundary (int, optional): Controls k-number of users with high number of records to exclude. Defaults to 1.
        lower_boundary (int, optional): Controls k-number of users with low number of records to exclude. Defaults to 3.
        nb_users_test (int, optional): Number of users to include in the test set. Defaults to 3.

    Returns:
        Tuple(Pandas DataFrame, Pandas DataFrame): Both train and test sets
    """
    np.random.seed(0)

    # number of records per user (sorted from highest to lowest)
    user_dist = data.user.value_counts()

    # array of users from which to choose the ones going into test set
    to_choose_from = user_dist[upper_boundary: len(
        user_dist) - lower_boundary].index

    # users in test set
    test_users = np.random.choice(to_choose_from, nb_users_test, replace=False)

    # splitting into train and test sets
    train = pd.DataFrame()
    test = pd.DataFrame()
    for _, row in data.iterrows():
        if row["user"] in test_users:
            test = pd.concat([test, row], axis=1)

        else:
            train = pd.concat([train, row], axis=1)

    return train.T, test.T


def split_train_test2(df, test_users):
    train = pd.DataFrame()
    test = pd.DataFrame()
    for _, row in df.iterrows():
        if row["user"] in test_users:
            test = pd.concat([test, row], axis=1)

        else:
            train = pd.concat([train, row], axis=1)

    return train.T, test.T


# Preprocessing + model pipeline
def pipelines(models):
    """Create pipelines made up preprocessors(Imputer, StandardScaler) and models

    Args:
        models (dict): A dictionary of model's name as key and sklearn corresponding algorithm as value

    Returns:
        dict: A dictionary of model's name as key and pipeline (preprocessing + model) as value
    """

    # Preprocessors
    # imputer = IterativeImputer(random_state=0, max_iter=30)
    imputer = KNNImputer()
    # imputer = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    qtransf = QuantileTransformer(output_distribution='normal')

    # Pipelines of preprocessor(s) and models
    pipes = {name: Pipeline([
        ('imputer', imputer),
        ('scaler', scaler),
        ('qtransf', qtransf),
        ('model', model)
    ]) for name, model in models.items()}

    return pipes


# Model performance
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

    for i in tqdm(range(len(pipes))):

        name = list(pipes.keys())[i]
        model = list(pipes.values())[i]

        # training time
        t0 = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - t0

        # predicting time
        t0 = time.time()
        preds = model.predict(X_test)
        pred_time = time.time() - t0

        # cross validation
        # scores = cross_val_score(model, X_train, y_train)

        # append to results
        results = pd.concat([results, pd.DataFrame({'name': [name],
                                                    # 'mean_score': [scores.mean()],
                                                    # 'std_score':[scores.std()],
                                                    # 'test_accuracy': [accuracy_score(y_test, preds)],
                                                    'balanced_accuracy':[balanced_accuracy_score(y_test, preds)],
                                                    'f1_score': [f1_score(y_test, preds)],
                                                    'precision': [precision_score(y_test, preds)],
                                                    'recall': [recall_score(y_test, preds)],
                                                    'training_time': [train_time],
                                                    'predicting_time': [pred_time]})
                             ])

    return results.sort_values(by='balanced_accuracy', ascending=False)
