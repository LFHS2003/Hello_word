import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

# ---------------------- 1. 中文显示与全局配置 ----------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 启用黑体显示中文
plt.rcParams["axes.unicode_minus"] = False    # 解决负号显示异常

st.set_page_config(
    page_title="2022年前3个月销售数据仪表盘",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ffffff;}
    .stSidebar {background-color: #121212; color: #ffffff; padding: 20px;}
    .filter-card {background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 15px;}
    .kpi-card {background-color: #1e1e1e; padding: 15px; border-radius: 8px; text-align: center; margin: 5px;}
    h1, h2, h3, h4 {color: #ffffff;}
    .stMatplotlibChart {background-color: #000000; padding: 10px;}
    </style>
    """, unsafe_allow_html=True)

# ---------------------- 2. 数据加载 ----------------------
@st.cache_data
def load_sales_data():
    desktop_path = str(Path.home() / "Desktop")
    file_path = os.path.join(desktop_path, "sj.xlsx")
    
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, engine="openpyxl", header=1)
        st.success(f"成功读取表头：{list(df.columns)}")
        
        # 日期处理
        df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
        if df["日期"].isnull().any():
            df["日期"] = df["日期"].fillna(pd.date_range(start="2022-01-01", periods=len(df)))
        return df
    else:
        st.error("❌ 桌面未找到sj.xlsx")
        # 兜底数据
        df = pd.DataFrame({
            "订单号": [f"ORD{i}" for i in range(1000)],
            "日期": pd.date_range(start="2022-01-01", periods=1000),
            "城市": pd.Series(["太原", "大同", "临汾"]).sample(n=1000, replace=True).values,
            "产品类型": pd.Series(["健康美容", "电子配件", "食品饮料"]).sample(n=1000, replace=True).values,
            "总价": pd.Series(range(100, 5000, 10)).sample(n=1000, replace=True).values,
            "评分": pd.Series([round(x,1) for x in pd.np.random.uniform(4,10,1000)]).values
        })
        return df

sales_df = load_sales_data()

# ---------------------- 3. 侧边栏筛选 ----------------------
with st.sidebar:
    st.markdown("<div class='filter-card'>", unsafe_allow_html=True)
    st.subheader("数据筛选")
    
    date_min = sales_df["日期"].min()
    date_max = sales_df["日期"].max()
    selected_dates = st.date_input(
        "日期范围",
        value=[date_min, date_max],
        min_value=date_min,
        max_value=date_max
    )
    
    selected_cities = st.multiselect("城市", sales_df["城市"].unique(), default=sales_df["城市"].unique())
    selected_products = st.multiselect("产品类型", sales_df["产品类型"].unique(), default=sales_df["产品类型"].unique())
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- 4. 数据筛选与KPI计算 ----------------------
filtered_df = sales_df[
    (sales_df["日期"] >= pd.Timestamp(selected_dates[0])) &
    (sales_df["日期"] <= pd.Timestamp(selected_dates[1])) &
    (sales_df["城市"].isin(selected_cities)) &
    (sales_df["产品类型"].isin(selected_products))
]

# 正确计算KPI
total_sales = filtered_df["总价"].sum()
avg_rating = filtered_df["评分"].mean().round(1)
total_orders = filtered_df["订单号"].nunique() if "订单号" in filtered_df.columns else len(filtered_df)
avg_sales_per_order = (total_sales / total_orders).round(2) if total_orders > 0 else 0

# ---------------------- 5. 可视化展示（核心：图表1改为每周趋势） ----------------------
st.title("2022年前3个月销售数据仪表盘")

# KPI卡片
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='kpi-card'><h4>总销售额</h4><h2 style='color: #1f77b4'>¥ {total_sales:,.0f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card'><h4>平均评分</h4><h2 style='color: #ff7f0e'>{avg_rating} ⭐</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card'><h4>总订单数</h4><h2 style='color: #2ca02c'>{total_orders}</h2></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card'><h4>每单均价</h4><h2 style='color: #d62728'>¥ {avg_sales_per_order:,.2f}</h2></div>", unsafe_allow_html=True)

st.divider()

# 图表区域（核心修改：图表1改为每周销售额趋势）
col1, col2 = st.columns(2)

# 图表1：每周销售额趋势（彻底修改，替换原每日趋势）
with col1:
    st.subheader("每周销售额趋势")  # 标题更新为“每周”
    # 关键修改：按周聚合数据（freq="W" 代表按周分组）
    weekly_sales = filtered_df.groupby(
        pd.Grouper(key="日期", freq="W")  # 按周聚合，自动合并一周内的所有数据
    ).agg({"总价": "sum"}).reset_index()  # 聚合每周的总销售额
    
    # 简化日期显示（格式：YYYY-MM 第W周，清晰不密集）
    weekly_sales["每周标签"] = weekly_sales["日期"].dt.strftime("%Y-%m") + " 第" + (weekly_sales["日期"].dt.isocalendar().week).astype(str) + "周"
    
    # 绘制每周销售额柱状图
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="#000000")
    ax.set_facecolor("#000000")
    ax.bar(
        weekly_sales["每周标签"],  # 横坐标使用简化的每周标签
        weekly_sales["总价"],
        color="#1f77b4",
        edgecolor="#ffffff",
        width=0.6  # 调整柱形宽度，更美观
    )
    # 坐标轴配置（清晰显示，无重叠）
    ax.set_xlabel("时间（年-月 第X周）", color="#ffffff", fontsize=10)
    ax.set_ylabel("销售额（元）", color="#ffffff", fontsize=10)
    plt.xticks(rotation=45, ha="right", color="#ffffff")  # 轻微旋转+右对齐，避免少量重叠
    plt.yticks(color="#ffffff")
    ax.grid(axis="y", alpha=0.2, color="#444444")  # 添加水平网格，更易读数据
    st.pyplot(fig)

# 图表2：产品类型销售额分布（保持不变）
with col2:
    st.subheader("产品类型销售额分布")
    product_sales = filtered_df.groupby("产品类型")["总价"].sum().sort_values(ascending=True).reset_index()
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="#000000")
    ax.set_facecolor("#000000")
    ax.barh(
        product_sales["产品类型"],
        product_sales["总价"],
        color="#ff7f0e",
        edgecolor="#ffffff"
    )
    ax.set_xlabel("销售额（元）", color="#ffffff", fontsize=10)
    ax.set_ylabel("产品类型", color="#ffffff", fontsize=10)
    plt.xticks(color="#ffffff")
    plt.yticks(color="#ffffff")
    st.pyplot(fig)