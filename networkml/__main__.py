import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from networkml.feature_conversion import label_encode

if __name__ == "__main__":
    df = pd.read_csv('../data/out.csv', escapechar="\\")

    print(df.head(3))

    df_label_enc = label_encode(df)

    print(df_label_enc.head(3))

    y = df_label_enc['label'].values
    print('Y Shape', y.shape)

    X = df_label_enc.drop('label', axis=1).values
    print('X Shape', X.shape)

    # divide data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    # select model
    model = DecisionTreeClassifier()

    # train the model
    model.fit(X_train, y_train)

    # prediction using the testing phase
    y_pred = model.predict(X_test)

    print("\n" + "-----------------\n"*3)

    # Measuring the performance using Confusion Matrix
    print("Confusion Matrix", confusion_matrix(y_test, y_pred))

    # Measuring performance using Recall
    print("Recall", recall_score(y_test, y_pred))
    # Measuring performance using Precision
    print("Precision", precision_score(y_test, y_pred))
    # Measuring performance using Accuracy
    print("Accuracy", accuracy_score(y_test, y_pred))
    # Measuring performance using F-Measure
    print("F-Measure", f1_score(y_test, y_pred))
