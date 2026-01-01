import streamlit as st
import os

# 页面配置：深色模式+示例界面风格
st.set_page_config(
    page_title="简易音乐播放器",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# 深色模式样式（完全匹配示例黑底白字）
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ffffff;}
    .stButton>button {
        background-color: #333333; 
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stButton>button:hover {background-color: #555555;}
    .stAudio {padding: 10px 0;}
    </style>
    """, unsafe_allow_html=True)

# ---------------- 关键：本地音频文件配置 ----------------
# 步骤1：在项目文件夹新建「audio」文件夹，放入3个MP3文件（命名如下）
# audio/1.mp3、audio/2.mp3、audio/3.mp3
# 若没有本地文件，可先用下方测试音频（备用方案）
TEST_AUDIO_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# 定义歌曲信息（适配示例界面的3首歌结构）
music_list = [
    {
        "cover": "https://picsum.photos/id/1015/200/200",  # 专辑封面
        "song": "歌曲1",
        "singer": "歌手A",
        "audio": "audio/1.mp3" if os.path.exists("audio/1.mp3") else TEST_AUDIO_URL
    },
    {
        "cover": "https://picsum.photos/id/1016/200/200",
        "song": "歌曲2",
        "singer": "歌手B",
        "audio": "audio/2.mp3" if os.path.exists("audio/2.mp3") else TEST_AUDIO_URL
    },
    {
        "cover": "https://picsum.photos/id/1018/200/200",
        "song": "歌曲3",
        "singer": "歌手C",
        "audio": "audio/3.mp3" if os.path.exists("audio/3.mp3") else TEST_AUDIO_URL
    }
]

# 初始化会话状态（记录当前播放歌曲索引）
if "current_song_idx" not in st.session_state:
    st.session_state.current_song_idx = 0

# 切换歌曲函数（循环切换）
def prev_song():
    st.session_state.current_song_idx = (st.session_state.current_song_idx - 1) % len(music_list)

def next_song():
    st.session_state.current_song_idx = (st.session_state.current_song_idx + 1) % len(music_list)

# ---------------- 页面渲染（完全匹配示例界面） ----------------
# 标题
st.markdown("<h2 style='text-align: center;'>简易音乐播放器</h2>", unsafe_allow_html=True)

# 当前歌曲信息（封面+歌名+歌手）
current_song = music_list[st.session_state.current_song_idx]
col1, col2 = st.columns([1, 2], gap="large")
with col1:
    # 专辑封面（固定200x200，匹配示例）
    st.image(current_song["cover"], width=200, caption=f"《{current_song['song']}》封面")
with col2:
    st.markdown(f"<h4>🎵 歌曲名称：{current_song['song']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<p>👨‍🎤 歌手：{current_song['singer']}</p>", unsafe_allow_html=True)

# 切换按钮（上一首/下一首，居中布局）
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, _, btn_col3 = st.columns([1, 1, 1])  # 中间列占位，实现按钮左右分布
with btn_col1:
    st.button("⬅️ 上一首", on_click=prev_song, use_container_width=True)
with btn_col3:
    st.button("下一首 ➡️", on_click=next_song, use_container_width=True)

# 音频播放组件（核心：确保可播放）
st.markdown("<br>", unsafe_allow_html=True)
st.audio(
    current_song["audio"],
    format="audio/mp3",
    start_time=0,
    loop=False,
    autoplay=False
)

# 播放进度条（模拟，匹配示例）
st.progress(40)
st.caption("📻 播放进度：40%（模拟）")

# 功能说明（完全复刻示例）
st.markdown("<br><h5>音乐播放器功能说明：</h5>", unsafe_allow_html=True)
st.write("1. 点击“上一首/下一首”切换3首歌曲")
st.write("2. 显示当前歌曲的封面、歌手及歌名")
st.write("3. 进度条模拟音乐播放状态")