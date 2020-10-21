import pandas as pd
from sklearn.preprocessing import LabelEncoder


def label_encode(df):
    df_zeros = fill_missing(df)

    # Get the categorical features of the data
    # obj_df = df_zeros.select_dtypes(include=['object']).copy()
    # print(obj_df.head(3))

    # Label Encoding
    df_label_enc = df_zeros
    number = LabelEncoder()
    df_label_enc['sport'] = number.fit_transform(df_zeros['sport'].astype('str'))
    df_label_enc['dport'] = number.fit_transform(df_zeros['dport'].astype('str'))
    df_label_enc['uri'] = number.fit_transform(df_zeros['uri'].astype('str'))
    df_label_enc['label'] = number.fit_transform(df_zeros['label'].astype('str'))

    return df_label_enc


def one_hot_encode(df):
    df_zeros = fill_missing(df)

    df_dummies = pd.get_dummies(df_zeros)

    return df_dummies


def fill_missing(df):
    # Handle missing data
    return df.fillna(0)
