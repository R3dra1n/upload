import json
import streamlit as st

def generate_json(case_data):
    """生成 JSON 数据并返回字符串"""
    return json.dumps(case_data, indent=4, ensure_ascii=False)

# Streamlit 前端界面
st.title("JSON 文件生成工具")
st.write("请填写以下字段，点击按钮生成并下载 JSON 文件。")

# 用户输入字段
case_id = st.text_input("案例编号 (case_id)", "case_001")
original_image = st.text_input("原始图片名称 (original_image)", "case_001_original.jpg")
disputed_image = st.text_input("纠纷图片名称 (disputed_image)", "case_001_disputed.jpg")
label = st.selectbox("是否侵权 (label)", ["侵权", "不侵权"])
modification_type = st.text_input("修改类型 (modification_type)", "")
visual_similarity_score = st.slider("视觉相似度评分", 0.0, 1.0, 0.5)
court = st.text_input("审理法院 (court)", "")
judgment_date = st.date_input("判决日期 (judgment_date)")
description = st.text_area("描述信息 (description)", "")
source = st.text_input("数据来源 (source)", "")

# 按钮生成 JSON 文件并提供下载
if st.button("生成 JSON 文件"):
    case_data = {
        "case_id": case_id,
        "original_image": original_image,
        "disputed_image": disputed_image,
        "label": label,
        "modification_type": modification_type,
        "visual_similarity_score": visual_similarity_score,
        "court": court,
        "judgment_date": str(judgment_date),
        "description": description,
        "source": source
    }
    
    # 将 JSON 数据生成字符串
    json_string = generate_json(case_data)
    st.success("JSON 文件已生成！点击下面按钮下载。")
    
    # 提供下载按钮
    st.download_button(
        label="下载 JSON 文件",
        data=json_string,
        file_name=f"{case_id}.json",
        mime="application/json"
    )
