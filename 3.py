import streamlit as st
import pandas as pd
import numpy as np
import altair as alt  # 导入altair库解决评分图表显示问题

# 页面基础配置：适配深色模式，固定居中布局
st.set_page_config(
    page_title="南宁美食数据仪表盘",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={"About": "南宁美食数据可视化仪表盘"}
)
# 深色模式适配：设置全局文字颜色
st.markdown("""
    <style>
    .stHeader {color: white;}
    .stCaption {color: #cccccc;}
    </style>
    """, unsafe_allow_html=True)

st.title("南宁本地美食数据仪表盘")

# 固定宽度主容器（统一页面宽度）
main_container = st.container(border=True)
with main_container:
    # --------------- 1. 南宁美食地图（固定宽高）---------------
    st.header("🍜 南宁美食分布", divider="orange")
    map_data = pd.DataFrame({
        "店铺名称": ["老南宁米粉店", "中山路酸嘢摊", "老友粉王", "卷筒粉小店", "南宁糖水铺"],
        "lat": [22.8170, 22.8258, 22.8065, 22.8203, 22.7989],
        "lon": [108.3634, 108.3430, 108.3402, 108.3525, 108.3318]
    })
    st.map(map_data, zoom=13, width=800, height=300)

    # --------------- 2. 店铺评分对比（彻底修复显示问题）---------------
    st.header("⭐ 店铺评分对比", divider="orange")
    score_data = pd.DataFrame({
        "店铺名称": ["老南宁米粉店", "中山路酸嘢摊", "老友粉王", "卷筒粉小店", "南宁糖水铺"],
        "评分": [4.8, 4.6, 4.9, 4.5, 4.7]
    })
    # 使用altair绘制柱状图（适配深色模式+固定宽高）
    score_chart = alt.Chart(score_data).mark_bar(color="#FF7F50").encode(
        x=alt.X("店铺名称:N", axis=alt.Axis(labelAngle=-45, labelColor="white", titleColor="white")),
        y=alt.Y("评分:Q", scale=alt.Scale(domain=[4, 5]), axis=alt.Axis(labelColor="white", titleColor="white")),
        tooltip=["店铺名称", "评分"]
    ).properties(width=800, height=300)
    st.altair_chart(score_chart)
    # 补充数据表格兜底
    st.caption("评分原始数据：")
    st.dataframe(score_data, width=800)

    # --------------- 3. 12个月价格走势（固定宽高）---------------
    st.header("📈 5家店铺12个月价格走势", divider="orange")
    months = [f"{i}月" for i in range(1, 13)]
    price_data = pd.DataFrame({
        "月份": months,
        "老南宁米粉店": np.random.uniform(8, 12, 12),
        "中山路酸嘢摊": np.random.uniform(10, 15, 12),
        "老友粉王": np.random.uniform(9, 13, 12),
        "卷筒粉小店": np.random.uniform(6, 9, 12),
        "南宁糖水铺": np.random.uniform(5, 8, 12)
    }).set_index("月份")
    st.line_chart(
        price_data,
        color=["#FF6347", "#32CD32", "#1E90FF", "#FFD700", "#FF69B4"],
        width=800,
        height=350,
        use_container_width=False
    )

    # --------------- 4. 用餐高峰时段（固定宽高）---------------
    st.header("📊 用餐高峰时段分布", divider="orange")
    time_data = pd.DataFrame({
        "时段": ["10:00", "12:00", "14:00", "18:00", "20:00", "22:00"],
        "客流量": [20, 80, 30, 90, 70, 40]
    }).set_index("时段")
    st.area_chart(
        time_data,
        color="#FFA500",
        width=800,
        height=300,
        use_container_width=False
    )

    # --------------- 5. 店铺详情（固定宽度）---------------
    st.header("📋 店铺详情", divider="orange")
    detail_col1, detail_col2 = st.columns(2, width=800)
    with detail_col1:
        st.write("""
        - **老南宁米粉店**：兴宁区民生路 | 生榨米粉
        - **中山路酸嘢摊**：青秀区中山路 | 芒果酸嘢
        - **老友粉王**：西乡塘区火炬路 | 经典老友粉
        """)
    with detail_col2:
        st.write("""
        - **卷筒粉小店**：江南区星光大道 | 猪肉卷筒粉
        - **南宁糖水铺**：良庆区五象大道 | 槐花粉糖水
        """)