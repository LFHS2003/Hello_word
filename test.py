# 导入streamlit库，这是创建Web页面的核心库，别名st是行业通用写法，简化后续调用
import streamlit as st

# 1. 页面主标题（title组件）：设置整个页面的核心标题，对应实训要求的title元素
st.title("学生黄少凌峰 - 数字档案")

# 2. 基础信息模块 - 二级标题（header组件）：划分“基础信息”模块，divider=blue添加蓝色分隔线，优化视觉
st.header("📋 基础信息", divider="blue")
# 文本展示（text组件）：展示纯文本格式的基础信息，对应实训要求的text元素
st.text("姓名：黄少凌峰 | 学号：22053040240 | 专业：信息管理与信息系统")
# 富文本展示（markdown组件）：支持加粗、特殊符号等格式，对应实训要求的markdown元素
st.markdown("**技能方向**：Python编程、数据可视化 | **学习状态**：🟢 正常在读")

# 3. 技能矩阵模块 - 二级标题：划分“技能矩阵”模块
st.header("💻 技能矩阵", divider="blue")
# 创建3列布局（columns）：让3个metric组件横向排列，优化页面布局
col1, col2, col3 = st.columns(3)
# 第一列：metric组件（指标展示），参数分别是“指标名”、“指标值”、“变化量”，对应实训要求的metric元素
with col1:
    st.metric("Python", "95%", "+5%")
# 第二列：展示Streamlit技能掌握度
with col2:
    st.metric("Streamlit", "87%", "+3%")
# 第三列：展示数据分析技能掌握度
with col3:
    st.metric("数据分析", "68%", "+2%")

# 4. 课程进度模块 - 二级标题：划分“课程进度”模块
st.header("📚 Streamlit课程进度", divider="blue")
# 定义表格数据：用字典格式存储，key是列名，value是列内容，为后续table组件做准备
progress_data = {
    "章节": ["基础语法", "组件使用", "实战开发"],  # 第一列：章节名称
    "完成度": ["100%", "80%", "50%"],            # 第二列：章节完成度
    "状态": ["✅ 已完成", "🔄 进行中", "📋 未开始"]  # 第三列：章节状态
}
# 表格展示（table组件）：将上述字典数据以表格形式展示，对应实训要求的table元素
st.table(progress_data)

# 5. 任务日志模块 - 二级标题：划分“任务日志”模块
st.header("📝 任务日志", divider="blue")
# markdown模拟简易表格：用markdown语法快速实现日志表格，补充可视化效果
st.markdown("| 日期       | 任务内容       | 完成星级 |")  # 表格表头
st.markdown("|------------|----------------|----------|")  # 表格分隔线
st.markdown("| 2024-10-01 | 学习基础组件   | ⭐⭐⭐⭐⭐ |")  # 第一行日志
st.markdown("| 2024-10-05 | 编写数字档案   | ⭐⭐⭐⭐ |")    # 第二行日志
# 纯文本补充日志信息：用text组件展示简单的最新任务说明
st.text("最新任务：完善实训代码 | 截止时间：2024-10-10")

# 6. 代码成果模块 - 二级标题：划分“最新代码成果”模块
st.header("💡 最新代码成果", divider="blue")
# 定义要展示的代码字符串：用三引号包裹多行代码，模拟实训的代码成果
demo_code = '''
import streamlit as st
# 数字档案核心代码示例
st.title("学生数字档案")
st.metric("Python技能", "95%", "+5%")
'''
# 代码展示（code组件）：将上述代码字符串以Python语法高亮展示，对应实训要求的code元素
# language="python"指定语法高亮的语言类型，确保代码展示格式正确
st.code(demo_code, language="python")