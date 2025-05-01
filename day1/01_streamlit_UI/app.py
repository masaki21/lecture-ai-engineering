import streamlit as st
import pandas as pd
import time

# ページ設定
st.set_page_config(
    page_title="おいしい食品ストア",
    layout="wide",
    initial_sidebar_state="expanded"
)

# タイトルと説明
st.title("🍎 おいしい食品オンラインストア")
st.markdown("毎日の食卓に、安全で美味しい食品をお届けします。")

# サイドバー - フィルターや情報
st.sidebar.header("🛒 商品フィルター")
category = st.sidebar.selectbox("カテゴリーを選択", ["すべて", "野菜", "果物", "肉", "飲み物"])

# デモ商品データ
product_data = pd.DataFrame([
    {"商品名": "りんご", "価格": 150, "カテゴリ": "果物", "在庫": 20},
    {"商品名": "みかん", "価格": 120, "カテゴリ": "果物", "在庫": 30},
    {"商品名": "キャベツ", "価格": 100, "カテゴリ": "野菜", "在庫": 15},
    {"商品名": "牛肉", "価格": 780, "カテゴリ": "肉", "在庫": 10},
    {"商品名": "緑茶", "価格": 200, "カテゴリ": "飲み物", "在庫": 25}
])

# カテゴリでフィルタリング
if category != "すべて":
    product_data = product_data[product_data["カテゴリ"] == category]

# 商品一覧表示
st.subheader("📦 商品一覧")
for index, row in product_data.iterrows():
    with st.container():
        cols = st.columns([2, 1, 1, 2])
        cols[0].markdown(f"**{row['商品名']}**")
        cols[1].markdown(f"価格: ¥{row['価格']}")
        cols[2].markdown(f"在庫: {row['在庫']}個")

        quantity = cols[3].number_input(
            f"{row['商品名']}の注文数", min_value=0, max_value=row["在庫"], key=f"qty_{index}"
        )

        if quantity > 0:
            st.success(f"{row['商品名']}を{quantity}個カートに追加しました")

# プログレスバー＆バルーン（注文完了イメージ）
if st.button("✅ 注文を確定する"):
    st.info("注文を処理中...")
    progress = st.progress(0)
    for i in range(101):
        time.sleep(0.01)
        progress.progress(i)
    st.success("ご注文ありがとうございます！🎉")
    st.balloons()

# フッター
st.divider()
st.caption("© 2025 おいしい食品オンラインストア")
