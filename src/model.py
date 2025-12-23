import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


# -----------------------------------
# Model feature set
# -----------------------------------
FEATURE_COLUMNS = [
    "fg_pct",
    "fg3_pct",
    "ft_pct",
    "assists_per_game",
    "rebounds_per_game",
    "turnovers_per_game",
    "net_rating",
    "efg_pct",
    "pie",
]


TARGET_COLUMN = "win_flag"


# -----------------------------------
# Prepare training data
# -----------------------------------
def prepare_model_data(team_season_df: pd.DataFrame) -> tuple:
    """
    Prepares feature matrix X and target y for modeling.

    Args:
        team_season_df (pd.DataFrame): Team-season metrics

    Returns:
        X (pd.DataFrame)
        y (pd.Series)
    """

    required_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = set(required_cols) - set(team_season_df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns for modeling: {missing}"
        )

    df = team_season_df.copy()

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y


# -----------------------------------
# Train logistic regression model
# -----------------------------------
def train_win_prediction_model(
    team_season_df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """
    Trains a logistic regression model to predict wins.

    Returns:
        dict: Trained model and performance metrics
    """

    X, y = prepare_model_data(team_season_df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000)),
        ]
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    return {
    "model": pipeline,
    "accuracy": accuracy,
    "X_test": X_test,
    "y_test": y_test,
    "y_pred": y_pred,
    "feature_names": X.columns.tolist(),
    }



# -----------------------------------
# Predict win probability
# -----------------------------------
def predict_win_probability(
    model_pipeline: Pipeline,
    input_data: pd.DataFrame,
) -> pd.Series:
    """
    Predicts win probability for given team metrics.

    Args:
        model_pipeline (Pipeline): Trained model
        input_data (pd.DataFrame): Feature data

    Returns:
        pd.Series: Win probabilities
    """

    missing = set(FEATURE_COLUMNS) - set(input_data.columns)
    if missing:
        raise ValueError(
            f"Missing required input features: {missing}"
        )

    probabilities = model_pipeline.predict_proba(
        input_data[FEATURE_COLUMNS]
    )[:, 1]

    return pd.Series(probabilities, index=input_data.index)
