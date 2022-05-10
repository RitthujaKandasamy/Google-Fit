# Dependencies
import matplotlib.pyplot as plt

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
