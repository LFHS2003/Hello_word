import streamlit as st

# 页面配置：深色模式适配+标题
st.set_page_config(
    page_title="个人简历生成器",
    layout="wide",
    initial_sidebar_state="expanded"
)
# 深色模式样式（匹配示例界面）
st.markdown("""
    <style>
    .stApp {background-color: #121212; color: #ffffff;}
    .stSidebar {background-color: #1e1e1e;}
    .resume-card {border: 1px solid #333; padding: 20px; border-radius: 8px; margin: 10px 0;}
    h2, h3 {border-bottom: 2px solid #4CAF50; padding-bottom: 8px;}
    </style>
    """, unsafe_allow_html=True)

# 侧边栏：信息填写区
with st.sidebar:
    st.title("个人信息填写")
    name = st.text_input("姓名", "黄少凌峰")
    avatar = st.text_input("头像链接", "https://picsum.photos/id/64/100/100")
    gender = st.selectbox("性别", ["男", "女"])
    age = st.number_input("年龄", min_value=18, max_value=60, value=22)
    phone = st.text_input("电话", "12312312312")
    email = st.text_input("邮箱", "python@xxx.com")
    education = st.text_input("学历", "本科")
    school = st.text_input("毕业院校", "xx大学")
    major = st.text_input("专业", "信息管理信息系统")
    job_intent = st.text_input("求职意向", "软件开发工程师")
    
    st.subheader("个人简介")
    intro = st.text_area("简介内容", "具备扎实的编程基础，熟练掌握Python、Streamlit等技术，有项目开发经验...")
    
    st.subheader("专业技能")
    skills = st.text_area("技能列表", "Python开发、Streamlit可视化、数据处理、前端基础")
    
    st.subheader("项目经验")
    project = st.text_area("项目描述", "1. 个人简历生成器：使用Streamlit开发，实现信息填写与简历展示\n2. 其他项目：...")

# 主页面：简历展示区
st.title("个人简历生成器")
st.markdown("<div class='resume-card'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 3])
with col1:
    st.image(avatar, width=100)
    st.write(f"**姓名**：{name}")
    st.write(f"**性别**：{gender}")
    st.write(f"**年龄**：{age}")
with col2:
    st.write(f"**电话**：{phone}")
    st.write(f"**邮箱**：{email}")
    st.write(f"**学历**：{education}")
    st.write(f"**毕业院校**：{school}")
    st.write(f"**专业**：{major}")
    st.write(f"**求职意向**：{job_intent}")
st.markdown("</div>", unsafe_allow_html=True)

st.subheader("个人简介")
st.write(intro)

st.subheader("专业技能")
st.write(skills)

st.subheader("项目经验")
st.write(project)