import streamlit as st

# 页面配置：适配视频播放+深色模式
st.set_page_config(
    page_title="视频播放站",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 深色模式样式优化
st.markdown("""
    <style>
    .stApp {background-color: #000; color: #fff;}
    .stButton>button {
        background-color: #333; 
        color: #fff; 
        border: 1px solid #666;
        width: 100%;
        margin: 5px 0;
        border-radius: 5px;
    }
    .stButton>button:hover {background-color: #555;}
    .stVideo {margin: 20px 0;}
    h2, h3 {text-align: center;}
    hr {border-color: #444;}
    </style>
    """, unsafe_allow_html=True)

# 定义3集视频资源（核心替换为指定视频链接，补充剧集信息）
video_list = [
    {
        "title": "极光1",
        "episode": "第1集",
        "video_url": "https://public.ysjf.com/mediastorm/material/material_preview/B[0002616-0003198].mp4",
        "intro": "本集为核心内容片段，展现了关键剧情节点，画面清晰，节奏紧凑，是系列内容的开篇之作。",
        "cast": "主演：张三、李四；导演：王五；出品方：影视飓风"
    },
    {
        "title": "极光2",
        "episode": "第2集",
        "video_url": "https://public.ysjf.com/mediastorm/material/material_preview/B[0002616-0003198].mp4",
        "intro": "第二集承接上一集剧情，新增多个支线情节，人物形象更加丰满，冲突逐步升级。",
        "cast": "主演：张三、李四、赵六；导演：王五；编剧：钱七；出品方：影视飓风"
    },
    {
        "title": "极光3",
        "episode": "第3集",
        "video_url": "https://public.ysjf.com/mediastorm/material/material_preview/B[0002616-0003198].mp4",
        "intro": "本集为系列收官之作，所有剧情线完成闭环，结局出人意料，留下开放式彩蛋供观众回味。",
        "cast": "主演：张三、李四、赵六；导演：王五；监制：孙八；出品方：影视飓风"
    }
]

# 初始化当前剧集索引
if "current_ep_idx" not in st.session_state:
    st.session_state.current_ep_idx = 0

# 切换剧集函数
def switch_ep(idx):
    st.session_state.current_ep_idx = idx

# 获取当前剧集信息
current_video = video_list[st.session_state.current_ep_idx]

# 页面标题
st.markdown(f"<h2>{current_video['title']}</h2>", unsafe_allow_html=True)

# 视频播放区域（添加异常捕获，优化加载体验）
st.subheader("视频播放区")
try:
    st.video(
        data=current_video["video_url"],
        format="video/mp4",
        start_time=0
    )
except Exception as e:
    st.error(f"视频加载失败！错误信息：{str(e)}")
    st.info("请检查视频链接是否有效，或刷新页面重试。")

# 3集切换按钮
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("剧集切换")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("第1集", on_click=switch_ep, args=(0,))
with col2:
    st.button("第2集", on_click=switch_ep, args=(1,))
with col3:
    st.button("第3集", on_click=switch_ep, args=(2,))

# 剧集介绍与演职人员
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("剧集介绍")
st.write(current_video["intro"])

st.subheader("演职人员")
st.write(current_video["cast"])