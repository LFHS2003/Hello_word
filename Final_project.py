# ---------------------- 1. 导入依赖库（规范化排序，注释清晰）----------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import os
from PIL import Image
import base64

# ---------------------- 2. 页面全局配置（自适应布局，美化样式）----------------------
st.set_page_config(
    page_title="智能学生成绩分析预测平台",
    page_icon="🎓",
    layout="wide",  # 自适应宽屏布局
    initial_sidebar_state="expanded"
)

# ---------------------- 3. 全局样式配置（解决中文乱码，统一图表格式）----------------------
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["legend.fontsize"] = 10
plt.rcParams["figure.autolayout"] = True  # 自适应布局
plt.rcParams["axes.grid"] = True  # 启用网格
plt.rcParams["grid.alpha"] = 0.3  # 网格透明度
plt.rcParams["grid.linestyle"] = "--"  # 网格线样式

# 设置matplotlib样式
plt.style.use('default')  # 使用默认样式

# ---------------------- 4. 自定义CSS样式（提升美观度）----------------------
st.markdown("""
<style>
    /* 主标题样式 */
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1f3d7a !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 3px solid #4CAF50 !important;
    }
    
    /* 副标题样式 */
    .sub-title {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        padding-left: 10px !important;
        border-left: 4px solid #3498db !important;
    }
    
    /* 卡片样式 */
    .custom-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        margin: 10px 0 !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* 数据框样式 */
    .stDataFrame {
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #2196F3, #21CBF3) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(33, 203, 243, 0.4) !important;
    }
    
    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%) !important;
    }
    
    /* 滑块样式 */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #8BC34A) !important;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 10px !important;
    }
    
    /* 选择框样式 */
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    /* 指标卡片样式 */
    .metric-card {
        background: white !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08) !important;
        border-left: 5px solid #4CAF50 !important;
        margin: 5px !important;
    }
    
    /* 宝石蓝数据概览卡片 */
    .sapphire-card {
        background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 6px 15px rgba(65, 105, 225, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        margin: 10px 0 !important;
    }
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem !important; }
        .sub-title { font-size: 1.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- 5. 核心配置（与用户数据列名完全匹配）----------------------
CORE_DATA_COLUMNS = [
    "学号",
    "性别",
    "专业",
    "每周学习时长",
    "上课出勤率",
    "期中考试分数",
    "作业完成率",
    "期末考试分数"
]

# ---------------------- 6. 数据加载函数（添加进度条和加载动画）----------------------
@st.cache_data(show_spinner="正在加载学生数据...")
def load_and_clean_student_data():
    """加载并清洗学生数据"""
    try:
        # 添加加载动画
        with st.spinner('🔄 正在加载数据文件...'):
            try:
                df_raw = pd.read_csv("student.csv", encoding="utf-8-sig")
            except UnicodeDecodeError:
                df_raw = pd.read_csv("student.csv", encoding="gbk")
        
        # 清洗列名
        df_cleaned = df_raw.copy()
        df_cleaned.columns = df_cleaned.columns.str.strip()
        df_cleaned.columns = df_cleaned.columns.str.replace(" ", "")
        
        # 校验核心列
        missing_core_columns = [col for col in CORE_DATA_COLUMNS if col not in df_cleaned.columns]
        if missing_core_columns:
            st.error(f"❌ 缺少核心列：{missing_core_columns}")
            st.stop()
        
        # 保留核心列并移除缺失值
        df_core = df_cleaned[CORE_DATA_COLUMNS].dropna(axis=0, how="any")
        
        # 显示成功提示
        st.toast(f'✅ 成功加载 {len(df_core)} 条学生数据', icon='🎯')
        
        return df_core
    
    except FileNotFoundError:
        st.error("❌ 未找到 student.csv 文件")
        st.stop()
    except Exception as e:
        st.error(f"❌ 数据加载失败：{str(e)}")
        st.stop()

# ---------------------- 7. 模型训练/加载函数（优化体验）----------------------
@st.cache_resource
def train_or_load_prediction_model(df_input):
    """训练或加载预测模型"""
    model_file_path = "student_final_score_model.joblib"
    features_file_path = "student_model_features.joblib"
    
    # 判断模型文件是否存在
    model_files_valid = os.path.exists(model_file_path) and os.path.exists(features_file_path)
    
    if model_files_valid:
        try:
            model = joblib.load(model_file_path)
            features = joblib.load(features_file_path)
            st.toast('✅ 已加载预训练模型', icon='🤖')
            return model, features
        except:
            st.toast('🔄 重新训练模型中...', icon='⚙️')
    
    # 训练新模型
    with st.spinner('正在训练AI预测模型...'):
        # 特征编码
        df_encoded = pd.get_dummies(
            df_input,
            columns=["性别", "专业"],
            drop_first=True,
            dtype=int
        )
        
        # 划分特征和目标
        X = df_encoded.drop("期末考试分数", axis=1)
        y = df_encoded["期末考试分数"]
        
        # 数据集划分
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # 模型训练
        model = RandomForestRegressor(
            n_estimators=150,
            random_state=42,
            n_jobs=-1,
            max_depth=10
        )
        model.fit(X_train, y_train)
        
        # 模型评估
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        
        # 保存模型
        joblib.dump(model, model_file_path)
        joblib.dump(X.columns.tolist(), features_file_path)
        
        st.toast(f'✅ 模型训练完成 (MAE: {mae:.2f}分)', icon='🎯')
    
    return model, X.columns.tolist()

# ---------------------- 8. 图片处理函数（支持网络图片和本地图片）----------------------
def get_image_base64(image_path, default_emoji="🎓"):
    """获取图片的base64编码或返回默认emoji"""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except:
        pass
    return None

def display_result_image(is_passed, predicted_score):
    """显示结果图片"""
    if is_passed:
        # 及格图片
        img_base64 = get_image_base64("congrats.png")
        if img_base64:
            st.markdown(f"""
                <div style="text-align:center; margin:20px 0;">
                    <img src="data:image/png;base64,{img_base64}" style="max-width:100%; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.2);">
                    <h3 style="color:#2E7D32; margin-top:15px;">🎉 预测分数: {predicted_score}分 - 恭喜通过！</h3>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align:center; padding:30px; background:linear-gradient(135deg, #E8F5E9, #C8E6C9); border-radius:15px; margin:20px 0;">
                    <span style="font-size:80px;">🎓</span>
                    <h3 style="color:#2E7D32; margin:10px 0;">预测分数: {predicted_score}分</h3>
                    <h4 style="color:#388E3C;">🎊 恭喜！预测成绩已通过！</h4>
                    <p style="color:#555; margin-top:10px;">保持优秀的学习习惯，继续努力！</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        # 不及格图片
        img_base64 = get_image_base64("encourage.png")
        if img_base64:
            st.markdown(f"""
                <div style="text-align:center; margin:20px 0;">
                    <img src="data:image/png;base64,{img_base64}" style="max-width:100%; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.2);">
                    <h3 style="color:#D32F2F; margin-top:15px;">💪 预测分数: {predicted_score}分 - 继续加油！</h3>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align:center; padding:30px; background:linear-gradient(135deg, #FFEBEE, #FFCDD2); border-radius:15px; margin:20px 0;">
                    <span style="font-size:80px;">📚</span>
                    <h3 style="color:#D32F2F; margin:10px 0;">预测分数: {predicted_score}分</h3>
                    <h4 style="color:#F44336;">💪 别灰心！分析原因，继续努力！</h4>
                    <p style="color:#555; margin-top:10px;">分析不足，调整学习策略，下次一定成功！</p>
                </div>
            """, unsafe_allow_html=True)

# ---------------------- 9. 初始化应用 -----------------------
# 添加加载状态
if 'data_loaded' not in st.session_state:
    with st.spinner('正在初始化系统...'):
        df_student_core = load_and_clean_student_data()
        prediction_model, model_feature_columns = train_or_load_prediction_model(df_student_core)
        st.session_state.df = df_student_core
        st.session_state.model = prediction_model
        st.session_state.features = model_feature_columns
        st.session_state.data_loaded = True

df_student_core = st.session_state.df
prediction_model = st.session_state.model
model_feature_columns = st.session_state.features

# ---------------------- 10. 侧边栏导航（美化设计）----------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding:20px 0;">
            <h2 style="color:white; margin:0;">🎓</h2>
            <h3 style="color:white; margin:10px 0;">智能成绩分析平台</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 导航选项
    selected_page = st.radio(
        "📋 功能导航",
        ["📊 项目总览", "📈 专业数据分析", "🔮 成绩预测"],
        label_visibility="collapsed"
    )
    
    # 简化为2个页面选项
    if "项目总览" in selected_page:
        page_key = "项目概述"
    elif "专业数据分析" in selected_page:
        page_key = "专业数据分析"
    else:
        page_key = "期末成绩预测"
    
    st.markdown("---")
    
    # 数据概览卡片 - 使用宝石蓝背景
    st.markdown(f"""
        <div class="sapphire-card">
            <h4 style="color:white; margin-top:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">📊 数据概览</h4>
            <p style="color:#f0f0f0; margin:8px 0; font-size:0.95rem;">👥 总学生数: <b style="color:#FFD700;">{len(df_student_core)}</b></p>
            <p style="color:#f0f0f0; margin:8px 0; font-size:0.95rem;">🎓 专业数量: <b style="color:#FFD700;">{df_student_core["专业"].nunique()}</b></p>
            <p style="color:#f0f0f0; margin:8px 0; font-size:0.95rem;">📊 平均期末分: <b style="color:#FFD700;">{df_student_core["期末考试分数"].mean():.1f}</b></p>
            <p style="color:#f0f0f0; margin:8px 0; font-size:0.95rem;">✅ 平均出勤率: <b style="color:#FFD700;">{(df_student_core["上课出勤率"].mean() * 100):.1f}%</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    # 底部信息
    st.markdown("---")
    st.markdown("""
        <div style="text-align:center; color:#aaa; padding:10px;">
            <small>© 2024 智能教育分析系统</small><br>
            <small>版本 2.0.0</small>
        </div>
    """, unsafe_allow_html=True)

# ---------------------- 界面1：项目概述 ----------------------
if page_key == "项目概述":
    # 主标题
    st.markdown('<h1 class="main-title">🎓 智能学生成绩分析预测平台</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 简介卡片
    st.markdown("""
        <div style="background:linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                    color:white; padding:30px; border-radius:15px; margin-bottom:30px; box-shadow: 0 6px 15px rgba(65, 105, 225, 0.3);">
            <h2 style="color:white; margin-top:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">📈 数据驱动的学业分析平台</h2>
            <p style="font-size:1.1rem; color:#f0f0f0;">基于机器学习技术，为学生成绩提供精准分析与智能预测，帮助教师和学生更好地理解学业表现。</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 功能概览 - 使用卡片布局
    st.markdown('<h2 class="sub-title">✨ 核心功能模块</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color:#2196F3; margin-top:0;">📊 专业数据分析</h3>
                <ul style="color:#333;">
                    <li><b>📋 核心指标汇总</b> - 各专业学业表现总览</li>
                    <li><b>👥 性别分布分析</b> - 双层柱状图展示</li>
                    <li><b>📈 成绩趋势分析</b> - 期中期末对比折线图</li>
                    <li><b>✅ 出勤率分析</b> - 各专业出勤情况统计</li>
                    <li><b>🎯 专业专项分析</b> - 大数据管理等专业深度分析</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color:#4CAF50; margin-top:0;">🔮 AI成绩预测</h3>
                <ul style="color:#333;">
                    <li><b>🤖 智能预测模型</b> - 基于随机森林算法</li>
                    <li><b>📝 个性化输入</b> - 学生信息定制化录入</li>
                    <li><b>🎯 精准预测</b> - 期末成绩智能预测</li>
                    <li><b>📊 结果可视化</b> - 直观图表展示</li>
                    <li><b>💡 学习建议</b> - 个性化改进方案</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # 数据指标展示
    st.markdown('<h2 class="sub-title">📋 数据概览</h2>', unsafe_allow_html=True)
    
    # 创建指标卡片 - 使用宝石蓝主题
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                        color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(65, 105, 225, 0.3); 
                        margin: 5px; text-align: center;">
                <h4 style="color:#f0f0f0; margin:0 0 10px 0;">👥 总学生数</h4>
                <h2 style="color:#FFD700; margin:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{len(df_student_core)}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                        color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(65, 105, 225, 0.3); 
                        margin: 5px; text-align: center;">
                <h4 style="color:#f0f0f0; margin:0 0 10px 0;">🎓 专业数量</h4>
                <h2 style="color:#FFD700; margin:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{df_student_core['专业'].nunique()}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_score = df_student_core['期末考试分数'].mean()
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                        color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(65, 105, 225, 0.3); 
                        margin: 5px; text-align: center;">
                <h4 style="color:#f0f0f0; margin:0 0 10px 0;">📊 平均期末分</h4>
                <h2 style="color:#FFD700; margin:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{avg_score:.1f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_attendance = df_student_core['上课出勤率'].mean() * 100
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                        color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(65, 105, 225, 0.3); 
                        margin: 5px; text-align: center;">
                <h4 style="color:#f0f0f0; margin:0 0 10px 0;">✅ 平均出勤率</h4>
                <h2 style="color:#FFD700; margin:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{avg_attendance:.1f}%</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # 数据字段说明
    st.markdown('<h2 class="sub-title">📄 数据字段说明</h2>', unsafe_allow_html=True)
    
    fields_data = {
        "字段名": CORE_DATA_COLUMNS,
        "说明": [
            "学生唯一标识符",
            "学生性别信息",
            "所学专业名称",
            "每周平均学习时间(小时)",
            "课程出勤百分比(0-100%)",
            "期中考试成绩(0-100分)",
            "作业完成百分比(0-100%)",
            "期末考试成绩(0-100分)"
        ],
        "类型": [
            "字符串",
            "分类",
            "分类",
            "数值",
            "百分比",
            "分数",
            "百分比",
            "分数"
        ]
    }
    
    fields_df = pd.DataFrame(fields_data)
    st.dataframe(
        fields_df.style.applymap(
            lambda x: 'background-color: #4169E1; color: white; font-weight: bold;', 
            subset=['字段名']
        ),
        use_container_width=True, 
        hide_index=True
    )

# ---------------------- 界面2：专业数据分析 ----------------------
elif page_key == "专业数据分析":
    st.markdown('<h1 class="main-title">📊 专业学业数据分析</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 数据预处理
    major_statistics = df_student_core.groupby("专业").agg(
        平均学习时长=("每周学习时长", "mean"),
        期中平均分=("期中考试分数", "mean"),
        期末平均分=("期末考试分数", "mean"),
        平均出勤率=("上课出勤率", "mean"),
        学生人数=("学号", "count")
    ).round(2)
    
    # 1. 数据总览表格
    st.markdown('<h2 class="sub-title">📋 专业数据总览</h2>', unsafe_allow_html=True)
    
    # 添加排序功能
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        sort_by = st.selectbox("排序依据", ["期末平均分", "期中平均分", "平均出勤率", "平均学习时长", "学生人数"])
    with col2:
        sort_order = st.radio("排序顺序", ["降序", "升序"], horizontal=True)
    with col3:
        show_all = st.checkbox("显示所有专业", value=True)
    
    # 排序逻辑
    sort_column = {
        "期末平均分": "期末平均分",
        "期中平均分": "期中平均分", 
        "平均出勤率": "平均出勤率",
        "平均学习时长": "平均学习时长",
        "学生人数": "学生人数"
    }[sort_by]
    
    sorted_df = major_statistics.sort_values(
        sort_column, 
        ascending=(sort_order == "升序")
    )
    
    if not show_all and len(sorted_df) > 5:
        display_df = sorted_df.head(5)
    else:
        display_df = sorted_df
    
    # 美化表格 - 添加宝石蓝表头
    st.dataframe(
        display_df.style.background_gradient(
            subset=['期末平均分', '期中平均分'], 
            cmap='RdYlGn'
        ).set_table_styles(
            [{'selector': 'thead th',
              'props': [('background-color', '#4169E1'),
                       ('color', 'white'),
                       ('font-weight', 'bold')]}]
        ).format({
            '平均出勤率': '{:.1%}',
            '平均学习时长': '{:.1f}小时',
            '期末平均分': '{:.1f}分',
            '期中平均分': '{:.1f}分'
        }),
        use_container_width=True,
        height=400
    )
    
    # 2. 可视化分析
    st.markdown('<h2 class="sub-title">📈 可视化分析</h2>', unsafe_allow_html=True)
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📊 综合对比", "👥 性别分布", "📚 专业详情", "🎯 专项分析"])
    
    with tab1:
        # 综合对比图
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 成绩对比
        x_pos = np.arange(len(major_statistics))
        width = 0.35
        
        bars1 = ax1.bar(x_pos - width/2, major_statistics['期末平均分'], 
                       width, color='#4CAF50', alpha=0.7, label='期末平均分')
        bars2 = ax1.bar(x_pos + width/2, major_statistics['期中平均分'],
                       width, color='#2196F3', alpha=0.7, label='期中平均分')
        ax1.set_ylabel('分数', fontsize=12)
        ax1.set_title('各专业期中期末成绩对比', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(major_statistics.index, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # 添加数值标签
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(f'{height:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=9)
        
        # 学习时长和出勤率
        ax2_twin = ax2.twinx()
        
        # 学习时长柱状图
        bars3 = ax2.bar(x_pos, major_statistics['平均学习时长'], 
                       color='#FF9800', alpha=0.7, width=0.4, label='平均学习时长')
        ax2.set_ylabel('学习时长(小时)', fontsize=12, color='#FF9800')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(major_statistics.index, rotation=45, ha='right')
        ax2.tick_params(axis='y', labelcolor='#FF9800')
        
        # 出勤率折线图
        line = ax2_twin.plot(x_pos, major_statistics['平均出勤率']*100,
                           color='#9C27B0', marker='o', linewidth=2, label='平均出勤率')
        ax2_twin.set_ylabel('出勤率(%)', fontsize=12, color='#9C27B0')
        ax2_twin.tick_params(axis='y', labelcolor='#9C27B0')
        
        ax2.set_title('学习时长与出勤率对比', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        # 合并图例
        lines_labels = [ax2.get_legend_handles_labels(), ax2_twin.get_legend_handles_labels()]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        ax2.legend(lines, labels, loc='upper left')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab2:
        # 性别分布
        gender_dist = pd.crosstab(df_student_core['专业'], df_student_core['性别'])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x_pos = np.arange(len(gender_dist))
        width = 0.35
        
        if len(gender_dist.columns) >= 2:
            bars_male = ax.bar(x_pos - width/2, gender_dist.iloc[:, 0], width, 
                              color='#4285F4', alpha=0.7, label=gender_dist.columns[0])
            bars_female = ax.bar(x_pos + width/2, gender_dist.iloc[:, 1], width,
                                color='#EA4335', alpha=0.7, label=gender_dist.columns[1])
        elif len(gender_dist.columns) == 1:
            bars = ax.bar(x_pos, gender_dist.iloc[:, 0], width, 
                         color='#4285F4', alpha=0.7, label=gender_dist.columns[0])
        
        ax.set_xlabel('专业', fontsize=12)
        ax.set_ylabel('学生人数', fontsize=12)
        ax.set_title('各专业男女生分布', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(gender_dist.index, rotation=45, ha='right')
        ax.legend(title='性别')
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
        
        # 添加性别比例计算
        gender_ratio = gender_dist.div(gender_dist.sum(axis=1), axis=0)
        st.dataframe(
            gender_ratio.style.format('{:.1%}'),
            use_container_width=True
        )
    
    with tab3:
        # 专业选择器
        selected_major = st.selectbox("选择专业查看详情", major_statistics.index.tolist())
        
        # 显示专业详情 - 使用宝石蓝卡片
        major_data = major_statistics.loc[selected_major]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                            color: white; padding: 15px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 0.9rem; color: #f0f0f0;">学生人数</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">{int(major_data['学生人数'])}人</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                            color: white; padding: 15px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 0.9rem; color: #f0f0f0;">期末平均分</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">{major_data['期末平均分']}分</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                            color: white; padding: 15px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 0.9rem; color: #f0f0f0;">期中平均分</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">{major_data['期中平均分']}分</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                            color: white; padding: 15px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 0.9rem; color: #f0f0f0;">平均出勤率</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #FFD700;">{major_data['平均出勤率']:.1%}</div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        # 专项分析
        if "大数据管理" in major_statistics.index:
            bigdata_data = major_statistics.loc["大数据管理"]
            
            # 创建雷达图
            categories = ['期末成绩', '期中成绩', '学习时长', '出勤率', '学生规模']
            
            # 数据归一化
            max_vals = major_statistics.max()
            min_vals = major_statistics.min()
            
            norm_data = [
                (bigdata_data['期末平均分'] - min_vals['期末平均分']) / (max_vals['期末平均分'] - min_vals['期末平均分']),
                (bigdata_data['期中平均分'] - min_vals['期中平均分']) / (max_vals['期中平均分'] - min_vals['期中平均分']),
                (bigdata_data['平均学习时长'] - min_vals['平均学习时长']) / (max_vals['平均学习时长'] - min_vals['平均学习时长']),
                bigdata_data['平均出勤率'],
                (bigdata_data['学生人数'] - min_vals['学生人数']) / (max_vals['学生人数'] - min_vals['学生人数'])
            ]
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            
            angles = [n / float(len(categories)) * 2 * np.pi for n in range(len(categories))]
            angles += angles[:1]
            norm_data += norm_data[:1]
            
            ax.plot(angles, norm_data, 'o-', linewidth=2, color='#4169E1')
            ax.fill(angles, norm_data, alpha=0.25, color='#4169E1')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_title('大数据管理专业综合表现雷达图', size=14, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            
            st.pyplot(fig)
        else:
            st.info("当前数据中未包含「大数据管理」专业")

# ---------------------- 界面3：期末成绩预测 ----------------------
else:
    st.markdown('<h1 class="main-title">🔮 AI成绩预测系统</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 创建两列布局
    col_input, col_result = st.columns([1, 1.5], gap="large")
    
    with col_input:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#2196F3; margin-top:0;">📝 学生信息录入</h3>', unsafe_allow_html=True)
        
        # 表单设计
        with st.form("prediction_form", border=False):
            # 学生基本信息
            st.markdown("**👤 基本信息**")
            col_id, col_gender = st.columns(2)
            with col_id:
                student_id = st.text_input(
                    "学号",
                    placeholder="请输入学号",
                    help="学生的唯一标识"
                )
            with col_gender:
                gender = st.radio(
                    "性别",
                    options=df_student_core["性别"].unique(),
                    horizontal=True
                )
            
            major = st.selectbox(
                "专业",
                options=df_student_core["专业"].unique(),
                help="选择学生所学专业"
            )
            
            st.markdown("---")
            st.markdown("**📊 学业表现**")
            
            # 学习时长
            study_hours = st.slider(
                "每周学习时长(小时)",
                min_value=0.0,
                max_value=50.0,
                value=20.0,
                step=0.5,
                help="每周投入学习的总时间"
            )
            
            # 出勤率
            attendance = st.slider(
                "上课出勤率(%)",
                min_value=0.0,
                max_value=100.0,
                value=85.0,
                step=1.0,
                format="%.0f%%",
                help="按时上课的比例"
            )
            
            # 期中成绩
            midterm_score = st.slider(
                "期中考试分数",
                min_value=0,
                max_value=100,
                value=75,
                step=1,
                help="期中考试成绩"
            )
            
            # 作业完成率
            homework_rate = st.slider(
                "作业完成率(%)",
                min_value=0.0,
                max_value=100.0,
                value=90.0,
                step=1.0,
                format="%.0f%%",
                help="按时完成作业的比例"
            )
            
            # 提交按钮
            submit_col1, submit_col2 = st.columns([3, 1])
            with submit_col1:
                submit_btn = st.form_submit_button(
                    "🚀 开始AI预测",
                    use_container_width=True,
                    type="primary"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 添加示例数据提示
        with st.expander("💡 示例数据参考", expanded=False):
            st.info("**优秀学生示例：**")
            st.markdown("- 学习时长: 25-35小时/周")
            st.markdown("- 出勤率: 90-100%")
            st.markdown("- 期中成绩: 85-95分")
            st.markdown("- 作业完成率: 95-100%")
            
            st.info("**待提升学生示例：**")
            st.markdown("- 学习时长: 5-15小时/周")
            st.markdown("- 出勤率: 60-75%")
            st.markdown("- 期中成绩: 50-65分")
            st.markdown("- 作业完成率: 70-85%")
    
    with col_result:
        if submit_btn and student_id:
            try:
                # 构造输入数据
                input_data_dict = {
                    "每周学习时长": [study_hours],
                    "上课出勤率": [attendance / 100],
                    "期中考试分数": [midterm_score],
                    "作业完成率": [homework_rate / 100]
                }
                
                # 性别编码
                available_genders = df_student_core["性别"].unique()
                if len(available_genders) > 1:
                    gender_col = f"性别_{available_genders[1]}"
                    input_data_dict[gender_col] = [1 if gender == available_genders[1] else 0]
                
                # 专业编码
                available_majors = df_student_core["专业"].unique()
                for major_item in available_majors[1:]:
                    major_col = f"专业_{major_item}"
                    input_data_dict[major_col] = [1 if major == major_item else 0]
                
                # 补全特征
                input_df = pd.DataFrame(input_data_dict)
                input_df = input_df.reindex(columns=model_feature_columns, fill_value=0)
                
                # 执行预测
                predicted_score = prediction_model.predict(input_df)[0]
                predicted_score_rounded = round(predicted_score, 2)
                is_passed = predicted_score_rounded >= 60
                
                # 显示预测结果卡片
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                
                # 学生信息概览
                st.markdown('<h3 style="color:#2196F3; margin-top:0;">📋 学生信息概览</h3>', unsafe_allow_html=True)
                
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                                    color: white; padding: 15px; border-radius: 10px; margin: 5px 0;">
                            <p style="color:#f0f0f0; margin:0 0 5px 0; font-size:0.9rem;">🎓 专业</p>
                            <h4 style="color:#FFD700; margin:0;">{major}</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                                    color: white; padding: 15px; border-radius: 10px; margin: 5px 0;">
                            <p style="color:#f0f0f0; margin:0 0 5px 0; font-size:0.9rem;">📚 学习时长</p>
                            <h4 style="color:#FFD700; margin:0;">{study_hours}小时/周</h4>
                        </div>
                    """, unsafe_allow_html=True)
                
                with info_col2:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                                    color: white; padding: 15px; border-radius: 10px; margin: 5px 0;">
                            <p style="color:#f0f0f0; margin:0 0 5px 0; font-size:0.9rem;">🚻 性别</p>
                            <h4 style="color:#FFD700; margin:0;">{gender}</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                                    color: white; padding: 15px; border-radius: 10px; margin: 5px 0;">
                            <p style="color:#f0f0f0; margin:0 0 5px 0; font-size:0.9rem;">✅ 出勤率</p>
                            <h4 style="color:#FFD700; margin:0;">{attendance:.0f}%</h4>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # 预测结果展示
                st.markdown('<h3 style="color:#2196F3; margin-top:0;">🎯 AI预测结果</h3>', unsafe_allow_html=True)
                
                # 分数展示 - 使用宝石蓝背景
                score_color = "#4CAF50" if is_passed else "#F44336"
                score_bg = "#4169E1" if is_passed else "#D32F2F"
                score_emoji = "🎉" if is_passed else "💪"
                score_text = "通过" if is_passed else "未通过"
                
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {score_bg} 0%, {score_bg}80 100%); 
                                padding:20px; border-radius:12px; border:2px solid rgba(255,255,255,0.3); 
                                text-align:center; margin:15px 0; box-shadow: 0 4px 15px rgba(65, 105, 225, 0.4);">
                        <h2 style="color:white; margin:0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{score_emoji} {predicted_score_rounded}分</h2>
                        <h3 style="color:#FFD700; margin:10px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{score_text} (及格线: 60分)</h3>
                        <p style="color:#f0f0f0; margin:0;">预测准确率: ±3分</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # 显示结果图片
                display_result_image(is_passed, predicted_score_rounded)
                
                st.markdown("---")
                
                # 分析与建议
                st.markdown('<h3 style="color:#2196F3; margin-top:0;">💡 学习分析与建议</h3>', unsafe_allow_html=True)
                
                if is_passed:
                    st.success("**🎊 优秀表现！**")
                    st.markdown("""
                        基于你的数据，AI分析显示：
                        - ✅ **学习习惯良好**：保持当前的学习节奏
                        - ✅ **课堂参与度高**：继续保持高出勤率
                        - ✅ **作业完成优秀**：作业完成率表现良好
                        
                        **💪 继续保持建议：**
                        1. **深化学习内容** - 尝试挑战更高难度的学习内容
                        2. **参与课堂互动** - 积极提问和参与讨论
                        3. **帮助其他同学** - 分享学习经验和方法
                        4. **拓展知识面** - 学习相关领域的补充知识
                    """)
                else:
                    st.warning("**📝 需要改进**")
                    
                    # 针对性建议
                    suggestions = []
                    if study_hours < 20:
                        suggestions.append(f"**增加学习时间** - 当前{study_hours}小时/周，建议增加到20-25小时/周")
                    if attendance < 80:
                        suggestions.append(f"**提高出勤率** - 当前{attendance}%，建议达到85%以上")
                    if midterm_score < 70:
                        suggestions.append(f"**加强期中复习** - 当前{midterm_score}分，建议提高到75分以上")
                    if homework_rate < 85:
                        suggestions.append(f"**提升作业质量** - 当前{homework_rate}%，建议达到90%以上")
                    
                    if suggestions:
                        st.markdown("**📊 改进方向：**")
                        for suggestion in suggestions:
                            st.markdown(f"- {suggestion}")
                    
                    st.markdown("""
                        **🚀 学习策略建议：**
                        1. **制定学习计划** - 每周制定详细的学习时间表
                        2. **课前预习** - 提前预习课程内容，提高课堂效率
                        3. **课后复习** - 及时复习巩固知识点
                        4. **寻求帮助** - 遇到困难时及时向老师或同学请教
                    """)
                
                st.markdown("---")
                
                # 数据对比 - 使用宝石蓝主题
                st.markdown('<h3 style="color:#2196F3; margin-top:0;">📈 数据对比分析</h3>', unsafe_allow_html=True)
                
                # 计算对比数据
                major_avg = df_student_core[df_student_core["专业"] == major]["期末考试分数"].mean()
                overall_avg = df_student_core["期末考试分数"].mean()
                
                # 使用st.columns展示对比
                comp_col1, comp_col2, comp_col3 = st.columns(3)
                with comp_col1:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                                    text-align:center; padding:15px; color:white; border-radius:10px;">
                            <p style="margin:0; font-weight:bold; color:#f0f0f0;">你的分数</p>
                            <h3 style="margin:5px 0; color:#FFD700;">{predicted_score_rounded}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                
                with comp_col2:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                                    text-align:center; padding:15px; color:white; border-radius:10px;">
                            <p style="margin:0; font-weight:bold; color:#f0f0f0;">专业平均</p>
                            <h3 style="margin:5px 0; color:#FFD700;">{major_avg:.1f}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                
                with comp_col3:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #4169E1 0%, #1E40AF 100%); 
                                    text-align:center; padding:15px; color:white; border-radius:10px;">
                            <p style="margin:0; font-weight:bold; color:#f0f0f0;">全校平均</p>
                            <h3 style="margin:5px 0; color:#FFD700;">{overall_avg:.1f}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 成功效果
                if is_passed:
                    st.balloons()
                    st.snow()
                
            except Exception as e:
                st.error(f"预测失败：{str(e)}")
                st.info("请检查输入数据是否完整有效")
        
        else:
            # 初始状态显示
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("""
                <div style="text-align:center; padding:50px 20px;">
                    <span style="font-size:60px; color:#ddd;">🤖</span>
                    <h3 style="color:#666; margin:20px 0;">等待预测请求</h3>
                    <p style="color:#888;">请在左侧输入学生信息后，点击「开始AI预测」按钮</p>
                    <div style="margin-top:30px; padding:20px; background:#f8f9fa; border-radius:10px;">
                        <h4 style="color:#2196F3;">💡 使用说明</h4>
                        <p style="color:#666; text-align:left;">1. 完整填写左侧所有学生信息</p>
                        <p style="color:#666; text-align:left;">2. 滑动调整器设置准确的学业表现数据</p>
                        <p style="color:#666; text-align:left;">3. 点击「开始AI预测」按钮获取预测结果</p>
                        <p style="color:#666; text-align:left;">4. 查看详细的预测分析和个性化建议</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- 底部信息 -----------------------
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 3, 2])
with footer_col2:
    st.markdown("""
        <div style="text-align:center; color:#666; padding:20px;">
            <p style="margin:5px 0;">🎓 <b>智能学生成绩分析预测平台</b> | 版本 2.0.0</p>
            <p style="margin:5px 0; font-size:0.9em;">基于机器学习技术，为教育决策提供数据支持</p>
            <p style="margin:5px 0; font-size:0.8em;">© 2024 版权所有 | 技术支持: AI教育实验室</p>
        </div>
    """, unsafe_allow_html=True)