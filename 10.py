# 导入所需库（确保已安装：streamlit pandas joblib）
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import os

# 页面配置（美化界面，支持中文）
st.set_page_config(
    page_title="医疗费用预测Web应用",
    layout="centered",  # 居中布局，更简洁
    initial_sidebar_state="collapsed"  # 隐藏侧边栏，聚焦输入
)

# 页面标题和说明
st.title("🏥 医疗费用预测应用")
st.markdown("---")
st.markdown("根据个人信息（年龄、BMI、吸烟状态等），预测个人年度医疗费用，为保险规划提供参考。")
st.markdown("---")

# 核心步骤1：加载训练好的模型和特征列名（确保文件在同一目录）
try:
    # 获取当前脚本目录（避免路径错误）
    current_path = os.path.dirname(os.path.abspath(__file__))
    # 拼接模型文件路径
    model_path = os.path.join(current_path, "medical_cost_model.joblib")
    feature_path = os.path.join(current_path, "feature_columns.joblib")
    
    # 加载模型和特征列
    model = joblib.load(model_path)
    feature_columns = joblib.load(feature_path)
    st.success("✅ 模型加载成功，可开始预测！")
except Exception as e:
    st.error(f"❌ 模型加载失败：{e}")
    st.error("请确认`medical_cost_model.joblib`和`feature_columns.joblib`与`app.py`在同一目录！")
    st.stop()  # 加载失败则停止运行

# 核心步骤2：创建用户输入界面（与你的sj2数据字段完全对应）
with st.form("medical_cost_form", clear_on_submit=False):
    st.subheader("📝 请填写个人信息")
    
    # 1. 年龄（滑块输入，符合实际范围）
    age = st.slider("年龄", min_value=0, max_value=100, value=30, step=1, help="请选择你的实际年龄")
    
    # 2. 性别（单选框）
    gender = st.radio("性别", options=["男性", "女性"], horizontal=True, help="请选择你的性别")
    
    # 3. BMI指数（数字输入，带范围限制）
    bmi = st.number_input(
        "BMI指数",
        min_value=10.0,
        max_value=50.0,
        value=24.0,
        step=0.1,
        help="BMI=体重(kg)÷身高(m)²，正常范围18.5-23.9"
    )
    
    # 4. 子女数量（滑块输入）
    children = st.slider("子女数量", min_value=0, max_value=10, value=0, step=1, help="请选择你的子女数量")
    
    # 5. 是否吸烟（单选框）
    smoker = st.radio("是否吸烟", options=["是", "否"], horizontal=True, help="是否有长期吸烟习惯")
    
    # 6. 所在区域（下拉选择框）
    region = st.selectbox(
        "所在区域",
        options=["西南部", "东南部", "东北部", "西北部"],
        help="请选择你的常住区域"
    )
    
    # 提交按钮（美化样式）
    submit_btn = st.form_submit_button("🔍 生成医疗费用预测", type="primary")

# 核心步骤3：点击提交后，执行预测逻辑
if submit_btn:
    # 步骤3.1：整理用户输入，转换为模型可识别的格式（匹配独热编码）
    input_data = pd.DataFrame({
        "年龄": [age],
        "BMI": [bmi],
        "子女数量": [children],
        # 分类特征：对应训练时的独热编码结果（drop_first=True）
        "性别_男性": [1 if gender == "男性" else 0],
        "是否吸烟_是": [1 if smoker == "是" else 0],
        "区域_东北部": [1 if region == "东北部" else 0],
        "区域_西北部": [1 if region == "西北部" else 0],
        "区域_东南部": [1 if region == "东南部" else 0]
    })
    
    # 步骤3.2：补全缺失特征列（确保与训练模型的特征一致，避免报错）
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)
    
    # 步骤3.3：执行预测
    try:
        predicted_cost = model.predict(input_data)[0]
        
        # 步骤3.4：美化展示预测结果
        st.markdown("---")
        st.success("### 📊 预测结果出炉！")
        st.info(f"#### 你的年度医疗费用预测为：**¥{predicted_cost:,.2f}**")
        
        # 附加说明（提升实用性）
        st.markdown("---")
        st.markdown("#### 📌 结果说明：")
        st.markdown("1. 该结果基于随机森林模型训练得出，仅供参考；")
        st.markdown("2. 吸烟、高BMI是影响医疗费用的核心因素；")
        st.markdown("3. 实际医疗费用受就医频率、疾病类型等多种因素影响。")
        
    except Exception as e:
        st.error(f"❌ 预测失败：{e}")
        st.error("请确认输入信息是否合法，或模型文件是否完整。")