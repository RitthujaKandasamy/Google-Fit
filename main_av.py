
from utilities import *
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier

# Load data
data = pd.read_csv('data/dataset_5secondWindow.csv')
print('raw_data: ', data.shape)

df = data.copy()

# Select columns to use
keep_columns = 'accelerometer|sound|orientation|linear_acceleration|speed|gyroscope|rotation_vector|game_rotation_vector|gyroscope_uncalibrated|target'
df = select_columns(df, keep_columns)

print('after column selection: ', df.shape)


# Drop columns with high percentage of missing values
df = drop_col_percent_na(df, 50)

print('after dropping column(s): ', df.shape)

# Features target separation
X = df.drop(columns='target')

y = df['target']


# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)
print('Train sets: ', X_train.shape, y_train.shape,
      '\nTest sets: ', X_test.shape, y_test.shape)


# Pipelines (preprocessing + model)
models = {'rf': RandomForestClassifier(random_state=0),
          "gb": GradientBoostingClassifier(random_state=0),
          'svm': SVC(),
          'mlp': MLPClassifier(random_state=0, max_iter=1000),
          'sgd': SGDClassifier(random_state=0)
          }


pipes = pipelines(models)


# Performance
