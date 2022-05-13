import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer


def data_cleaning(csv_path):
    df = pd.read_csv(csv_path)

    columns = ['activityrecognition#1', 'android.sensor.accelerometer#mean',
               'android.sensor.game_rotation_vector#mean',
               'android.sensor.gravity#mean', 'android.sensor.gyroscope#mean',
               'android.sensor.gyroscope_uncalibrated#mean',
               'android.sensor.linear_acceleration#mean',
               'android.sensor.magnetic_field#mean',
               'android.sensor.magnetic_field_uncalibrated#mean',
               'android.sensor.orientation#mean',
               'android.sensor.rotation_vector#mean', 'sound#mean', 'speed#mean', 'target', 'user']
    df = df[columns]
    df = df.sort_values(by='user')

    ord_encoder = OrdinalEncoder(categories=[df['target'].unique(), df['user'].unique()])
    df[['target', 'user']] = ord_encoder.fit_transform(df[['target', 'user']])

    df_copy = df

    df[['target', 'user']] = df_copy[['target', 'user']].astype(int)
    df = df.dropna()
    df_copy[['target', 'user']] = df_copy[['target', 'user']].astype(int)

    # df = df.groupby(['user', 'target']).transform(lambda x: x.fillna(x.mean()))

    df[['target', 'user']] = df_copy[['target', 'user']].astype(int)

    impute = SimpleImputer(missing_values=np.nan, strategy='mean')
    df = impute.fit_transform(df)

    df = pd.DataFrame(df, columns=df_copy.columns)
    columns_three = ['android.sensor.accelerometer#mean', 'sound#mean', 'android.sensor.gyroscope#mean', 'speed#mean', 'target', 'user']
    df = df[columns_three]
    return 