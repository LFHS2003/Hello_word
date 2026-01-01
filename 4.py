import streamlit as st

# 页面配置：适配深色模式，设置页面标题
st.set_page_config(
    page_title="图片画廊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 定义图片资源（3张示例图的网络链接，避免本地文件依赖）
image_list = [
    {
        "url": "https://public.ysjf.com/content/title-image/XRgn1c5bOyw.jpg",  # 第1张猫图
        "caption": "海边的泰迪"
    },
    {
        "url": "https://public.ysjf.com/content/title-image/XBCN-vaKaiM.jpg",  # 第2张猫图
        "caption": "小熊猫"
    },
    {
        "url": "https://public.ysjf.com/content/title-image/_RxIrCpsf77.jpg",  # 第3张猫图
        "caption": "慵懒的布偶猫"
    }
]

# 初始化图片索引（控制当前显示的图片）
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0

# 切换图片的函数
def prev_image():
    st.session_state.current_idx = (st.session_state.current_idx - 1) % len(image_list)

def next_image():
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(image_list)

# 页面主体：显示当前图片
st.markdown("<h2 style='text-align: center;'>图片画廊</h2>", unsafe_allow_html=True)
current_image = image_list[st.session_state.current_idx]
# 替换废弃参数：use_column_width→use_container_width，去除提示
st.image(current_image["url"], use_container_width=True)  # 显示当前图片

# 显示对应图注
st.markdown(f"<p style='text-align: center;'>{current_image.get('caption', '可爱的猫咪')}</p>", unsafe_allow_html=True)

# 切换按钮（水平居中）
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("上一张", on_click=prev_image)
with col3:
    st.button("下一张", on_click=next_image)