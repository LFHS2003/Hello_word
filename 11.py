# 导入所需库（确保已安装：streamlit pandas joblib）
import streamlit as st
import pandas as pd
import joblib
import os

# 页面配置（美化界面，支持中文）
st.set_page_config(
    page_title="企鹅分类预测系统",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 页面标题和说明
st.title("🐧 企鹅种类分类预测应用")
st.markdown("---")
st.markdown("根据企鹅的栖息岛屿、身体特征等信息，预测其所属种类（适配sj3.csv数据）")
st.markdown("---")

# 核心步骤1：加载新训练的模型和特征列名（适配v2版本模型）
try:
    # 获取当前脚本目录，避免路径错误
    current_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_path, "penguin_model_v2.joblib")
    feature_path = os.path.join(current_path, "penguin_features_v2.joblib")
    
    # 加载模型和特征列
    model = joblib.load(model_path)
    feature_columns = joblib.load(feature_path)
    st.success("✅ 企鹅分类模型加载成功，可开始预测！")
except Exception as e:
    st.error(f"❌ 模型加载失败：{e}")
    st.error("请确认`penguin_model_v2.joblib`和`penguin_features_v2.joblib`与`penguin_app_v2.py`在同一目录！")
    st.stop()

# 核心步骤2：创建用户输入界面（新增“栖息岛屿”，与sj3.csv字段完全对应）
with st.form("penguin_classify_form", clear_on_submit=False):
    st.subheader("📝 请填写企鹅的相关特征")
    
    # 1. 企鹅栖息的岛屿（下拉选择，与数据中的岛屿对应）
    island = st.selectbox(
        "企鹅栖息的岛屿",
        options=["Biscoe", "Dream", "Torgersen"],  # 对应sj3.csv中的岛屿类型
        help="选择企鹅的栖息岛屿"
    )
    
    # 2. 喙的长度（数字输入，带范围限制）
    bill_length = st.number_input(
        "喙的长度（mm）",
        min_value=30.0,
        max_value=60.0,
        value=45.0,
        step=0.1,
        help="企鹅喙部的长度，正常范围30-60mm"
    )
    
    # 3. 喙的深度（数字输入，带范围限制）
    bill_depth = st.number_input(
        "喙的深度（mm）",
        min_value=15.0,
        max_value=25.0,
        value=20.0,
        step=0.1,
        help="企鹅喙部的深度，正常范围15-25mm"
    )
    
    # 4. 翅膀的长度（数字输入，带范围限制）
    flipper_length = st.number_input(
        "翅膀的长度（mm）",
        min_value=170,
        max_value=220,
        value=195,
        step=1,
        help="企鹅翅膀的长度，正常范围170-220mm"
    )
    
    # 5. 身体质量（数字输入，带范围限制）
    body_mass = st.number_input(
        "身体质量（g）",
        min_value=3000,
        max_value=6000,
        value=4500,
        step=50,
        help="企鹅的体重，正常范围3000-6000g"
    )
    
    # 6. 性别（单选框，横向排列）
    gender = st.radio(
        "性别",
        options=["雄性", "雌性"],
        horizontal=True,
        help="选择企鹅的性别"
    )
    
    # 7. 观测年份（固定默认值，数据中均为2007，不影响预测）
    observation_year = st.number_input(
        "观测年份",
        min_value=2007,
        max_value=2007,
        value=2007,
        disabled=True,  # 禁用修改，避免用户误操作
        help="数据中观测年份均为2007，无需修改"
    )
    
    # 提交按钮（美化样式，突出显示）
    submit_btn = st.form_submit_button("🔍 预测企鹅种类", type="primary")

# 核心步骤3：点击提交后，执行预测逻辑（适配新模型的特征编码）
if submit_btn:
    # 步骤3.1：整理用户输入，转换为模型可识别的格式（匹配独热编码结果）
    input_data = pd.DataFrame({
        "喙的长度": [bill_length],
        "喙的深度": [bill_depth],
        "翅膀的长度": [flipper_length],
        "身体质量": [body_mass],
        "观测年份": [observation_year],
        # 分类特征1：企鹅栖息的岛屿（对应独热编码 drop_first=True）
        "企鹅栖息的岛屿_Dream": [1 if island == "Dream" else 0],
        "企鹅栖息的岛屿_Torgersen": [1 if island == "Torgersen" else 0],
        # 分类特征2：性别（对应独热编码 drop_first=True）
        "性别_雄性": [1 if gender == "雄性" else 0]
    })
    
    # 步骤3.2：补全缺失特征列（确保与训练模型的特征一致，避免报错）
    input_data = input_data.reindex(columns=feature_columns, fill_value=0)
    
    # 步骤3.3：执行预测
    try:
        pred_result = model.predict(input_data)[0]
        
        # 步骤3.4：美化展示预测结果
        st.markdown("---")
        st.success("### 📊 企鹅种类预测结果出炉！")
        st.info(f"#### 该企鹅属于：**{pred_result}**")
        
        # 附加说明（提升实用性）
        st.markdown("---")
        st.markdown("#### 📌 结果说明：")
        st.markdown("1. 该结果基于随机森林模型训练得出，仅供科研/学习参考；")
        st.markdown("2. 栖息岛屿、喙部尺寸、身体质量是影响企鹅种类分类的核心因素；")
        st.markdown("3. 数据来源于`sj3.csv`，模型准确率约95%以上（视数据质量而定）。")
        
    except Exception as e:
        st.error(f"❌ 预测失败：{e}")
        st.error("请确认输入信息是否合法，或模型文件是否完整无损坏。")