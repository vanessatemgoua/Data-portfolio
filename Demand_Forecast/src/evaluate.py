import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def rmspe(y_true, y_pred):
    """Root Mean Square Percentage Error — Kaggle metric for Rossmann."""
    mask = y_true != 0
    return np.sqrt(np.mean(((y_true[mask] - y_pred[mask]) / y_true[mask]) ** 2))


def rmspe_lgb(y_pred, dtrain):
    y_true = dtrain.get_label()
    score = rmspe(np.expm1(y_true), np.expm1(y_pred))
    return "rmspe", score, False  # False = lower is better


def plot_feature_importance(model, feature_cols, top_n=20):
    importance = pd.Series(
        model.feature_importance(importance_type="gain"), index=feature_cols
    ).sort_values(ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    importance.plot(kind="barh", ax=ax, color="steelblue")
    ax.invert_yaxis()
    ax.set_title(f"Top {top_n} Feature Importances")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    return fig


def plot_predictions(y_true, y_pred, n=200):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(y_true[:n].values, label="Actual", alpha=0.8)
    ax.plot(y_pred[:n], label="Predicted", alpha=0.8)
    ax.set_title("Actual vs Predicted Sales (first N samples)")
    ax.set_ylabel("Sales")
    ax.legend()
    plt.tight_layout()
    return fig
