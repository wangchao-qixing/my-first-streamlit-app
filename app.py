#1、调用工具，搭建环境
import streamlit as st
from asset_parser import count_character_lines, filter_major_characters

# --- 1.5. 状态初始化 ---
# 确保所有会被用到的session_state键在第一次运行时都存在
if 'user_text_input' not in st.session_state:
    st.session_state.user_text_input = ""
if 'min_line_slider' not in st.session_state:
    st.session_state.min_line_slider = 3
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

#2、定义回调函数
def run_analysis():
    #定义赋值变量
    script_text = st.session_state.user_text_input
    threshold = st.session_state.min_line_slider
    
    #用户输入内容后，调用函数，赋值结果
    if script_text:
        count = count_character_lines(script_text)
        maincha = filter_major_characters(count, threshold)
        #存储结果到st.session_state函数
        st.session_state.count_results = count
        st.session_state.maincha_results = maincha
        st.session_state.last_threshold = threshold
        st.session_state.analysis_run = True

    else:
        # 如果文本框变空，就将结果更新为空字典，并重置标志位
        st.session_state.count_results = {}
        st.session_state.maincha_results = {}
        st.session_state.analysis_run = False

def clear_all():
    # 这个函数负责将一切恢复到初始状态
    st.session_state.user_text_input = ""
    st.session_state.min_line_slider = 3 # 也可以重置滑块
    st.session_state.count_results = {}
    st.session_state.maincha_results = {}
    st.session_state.analysis_run = False

#3、页面布局
st.title('剧本资产清单拆解器')
st.header('V0.6 - 实时分析版')

#4、输入控件
st.text_area('请输入剧本内容:', key='user_text_input', on_change=run_analysis)
st.slider('选择主要角色的最小台词数:', 1, 20, 3, key='min_line_slider', on_change=run_analysis)
st.button('清除所有内容', on_click=clear_all)

#5、结果展示区
st.write("--- 分析结果 ---")

if st.session_state.count_results:
    st.write('**全角色统计:**')
    st.dataframe(st.session_state.count_results)
    
    if st.session_state.maincha_results:
        st.write(f"**主要角色 (台词 >= {st.session_state.last_threshold}):**")
        st.dataframe(st.session_state.maincha_results)
    else:
        st.info(f"根据当前阈值({st.session_state.last_threshold})，没有找到符合条件的主要角色。")
else:
    if st.session_state.analysis_run:
        st.info("分析完成：无法从当前文本中分析出任何角色。")
    else:
        st.info("请在上方输入或粘贴剧本内容，分析结果将实时显示。")
