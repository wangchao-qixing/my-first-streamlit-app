#1、调用工具，搭建环境
import streamlit as st
from asset_parser import count_character_lines, filter_major_characters

# --- 1.5. 状态初始化 ---
# 只初始化那些会被回调函数读取的【输入控件】相关的状态
if 'user_text_input' not in st.session_state:
    st.session_state.user_text_input = ""
if 'min_line_slider' not in st.session_state:
    st.session_state.min_line_slider = 3
# 以及我们的状态标志位
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

#2、定义回调函数
def run_analysis():
    script_text = st.session_state.user_text_input
    threshold = st.session_state.min_line_slider

    if script_text:
        count = count_character_lines(script_text)
        maincha = filter_major_characters(count, threshold)
        
        st.session_state.count_results = count
        st.session_state.maincha_results = maincha
        st.session_state.last_threshold = threshold
        st.session_state.analysis_run = True
    else:
        st.session_state.count_results = {}
        st.session_state.maincha_results = {}
        st.session_state.analysis_run = False

def clear_all():
    st.session_state.user_text_input = ""
    st.session_state.min_line_slider = 3
    st.session_state.count_results = {}
    st.session_state.maincha_results = {}
    st.session_state.analysis_run = False

#3、页面布局
st.title('剧本资产清单拆解器')
st.header('V1.0 - 实时分析版')

#4、输入控件
st.text_area('请输入剧本内容:', key='user_text_input', on_change=run_analysis, placeholder="在此粘贴你的剧本...")
st.slider('选择主要角色的最小台词数:', 1, 20, 3, key='min_line_slider', on_change=run_analysis)
st.button('清除所有内容', on_click=clear_all)

#5、结果展示区
st.write("--- 分析结果 ---")

# 使用 .get() 方法来安全地读取可能不存在的键
count_res = st.session_state.get('count_results', {})
maincha_res = st.session_state.get('maincha_results', {})
analysis_has_run = st.session_state.get('analysis_run', False)
last_thresh = st.session_state.get('last_threshold', 3)

if count_res:
    st.write('**全角色统计:**')
    st.dataframe(count_res)
    
    if maincha_res:
        st.write(f"**主要角色 (台词 >= {last_thresh}):**")
        st.dataframe(maincha_res)
    else:
        st.info(f"根据当前阈值({last_thresh})，没有找到符合条件的主要角色。")
else:
    if analysis_has_run:
        st.info("分析完成：无法从当前文本中分析出任何角色。")
    else:
        st.info("请在上方输入或粘贴剧本内容，分析结果将实时显示。")