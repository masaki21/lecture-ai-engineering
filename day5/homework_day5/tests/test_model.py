"""
モデルの精度・推論速度・リグレッションを確認するテスト。
pytest -q day5/homework_day5/tests/test_model.py
"""
import time
from pathlib import Path
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score

# === パス設定 ===
# ファイルの深さが  lecture-ai-engineering/day5/homework_day5/tests/test_model.py
# なので、リポジトリルートは parents[4]
ROOT = Path(__file__).resolve().parents[4]

MODEL_CUR  = ROOT / "day5/演習1/models/titanic_model.pkl"
MODEL_PREV = ROOT / "day5/演習1/models/titanic_model_prev.pkl"
TEST_CSV   = ROOT / "day5/homework_day5/data/Titanic.csv"

ACC_THRESHOLD   = 0.78
MAX_LATENCY_SEC = 0.002  # 1 サンプルあたり

def _load_xy():
    df = pd.read_csv(TEST_CSV)[["Pclass", "Sex", "Age", "Fare", "Survived"]].dropna()
    X = df.drop("Survived", axis=1)
    y = df["Survived"]
    return X, y

def _load_model(path: Path):
    with open(path, "rb") as f:
        return pickle.load(f)

def test_accuracy():
    X, y = _load_xy()
    acc = accuracy_score(y, _load_model(MODEL_CUR).predict(X))
    assert acc >= ACC_THRESHOLD, f"Accuracy {acc:.3f} < {ACC_THRESHOLD}"

def test_latency():
    X, _ = _load_xy()
    t0 = time.time()
    _ = _load_model(MODEL_CUR).predict(X)
    per_sample = (time.time() - t0) / len(X)
    assert per_sample <= MAX_LATENCY_SEC, f"Latency {per_sample:.4f}s > {MAX_LATENCY_SEC}s"

def test_regression():
    if not MODEL_PREV.exists():
        return        # 比較対象が無ければスキップ
    X, y = _load_xy()
    cur_acc  = accuracy_score(y, _load_model(MODEL_CUR).predict(X))
    prev_acc = accuracy_score(y, _load_model(MODEL_PREV).predict(X))
    assert cur_acc >= prev_acc - 1e-4, f"Current acc ({cur_acc:.3f}) < prev ({prev_acc:.3f})"

