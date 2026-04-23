import streamlit as st
import pandas as pd
import os
import random

st.set_page_config(page_title="Ứng dụng Học Trắc Nghiệm", page_icon="🎓", layout="wide")

# --- CUSTOM CSS KHÔNG SỬ DỤNG TAILWIND ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    /* Bắt buộc áp dụng Font chữ hiện đại hơn, cỡ 20px */
    html, body, [class*="css"], p, div, span, label, button {
        font-family: 'Inter', sans-serif !important;
        font-size: 20px !important;
    }
    
    /* Overall Background and App */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .block-container {
        pointer-events: auto;
        padding: 3rem 4rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-top: 0rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    h1 {
        color: #1e3a8a !important;
        font-weight: bold !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        font-size: 40px !important;
        border-bottom: 2px dashed #93c5fd;
        padding-bottom: 15px !important;
        text-shadow: 1px 1px 2px rgba(30, 58, 138, 0.1);
    }
    
    h3 {
        color: #1e293b !important;
        line-height: 1.6 !important;
        font-size: 28px !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
        letter-spacing: 0.5px;
    }
    
    /* Đóng gói các lựa chọn radio */
    div.stRadio > div {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div.stRadio > div:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-color: #94a3b8;
        transform: translateY(-2px);
    }
    
    .stRadio label {
        font-size: 24px !important;
        color: #334155 !important;
        padding: 8px 0px;
        cursor: pointer;
    }
    
    /* Feedback Box */
    .success-box {
        background: linear-gradient(to right, #ecfdf5, #d1fae5);
        color: #065f46;
        padding: 20px 25px;
        border-radius: 12px;
        border-left: 6px solid #10b981;
        margin-top: 25px;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
        animation: fadeIn 0.4s ease-out;
    }
    
    .error-box {
        background: linear-gradient(to right, #fef2f2, #fee2e2);
        color: #991b1b;
        padding: 20px 25px;
        border-radius: 12px;
        border-left: 6px solid #ef4444;
        margin-top: 25px;
        font-size: 24px;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
        animation: fadeIn 0.4s ease-out;
    }
    
    .error-correct-ans {
        margin-top: 15px;
        color: #065f46;
        font-weight: bold;
        background-color: #d1fae5;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #34d399;
        font-size: 22px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Các nút bấm stButton */
    .stButton button {
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        padding: 12px 30px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.5px;
        white-space: nowrap !important;
        width: auto !important;
        min-width: 150px;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(37,99,235,0.3) !important;
    }
    .stButton button[kind="primary"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(37,99,235,0.4) !important;
    }
    .stButton button:not([kind="primary"]) {
        background-color: white !important;
        border: 2px solid #cbd5e1 !important;
        color: #475569 !important;
    }
    .stButton button:not([kind="primary"]):hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        border-color: #94a3b8 !important;
    }
    
    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        background-image: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
        border-bottom: none;
        text-shadow: none;
    }
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_sheets(file_path):
    if file_path.endswith('.xls'):
        xl = pd.ExcelFile(file_path, engine='xlrd')
    else:
        xl = pd.ExcelFile(file_path, engine='openpyxl')
    return xl.sheet_names

@st.cache_data
def load_data(file_path, sheet_name):
    # Đọc dữ liệu với engine tương ứng dựa vào phần mở rộng
    if file_path.endswith('.xls'):
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='xlrd')
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        
    questions = []
    current_q = None
    
    for _, row in df.iterrows():
        # Clean data row
        full_row_str = [str(x).strip() if pd.notna(x) else "" for x in row.values]
        if not any(full_row_str):
            continue
            
        full_row_str = full_row_str + [""] * (5 - len(full_row_str)) # Pad for safety
            
        is_q = False
        is_a = False
        
        # Nhận diện dòng Câu hỏi (Q) và Trả lời (A)
        if full_row_str[0].upper() == 'Q':
            is_q = True
        elif full_row_str[0].upper() == 'A':
            is_a = True
        elif full_row_str[0] == "" and full_row_str[1].lower().strip('.') in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            is_a = True
            
        if is_q:
            q_text = full_row_str[2] if (full_row_str[1].isdigit() and full_row_str[2] != "") else full_row_str[1]
            if not q_text and len(full_row_str) > 2:
                q_text = full_row_str[2]
            
            if q_text:
                if current_q and current_q["options"]:
                    questions.append(current_q)
                current_q = {
                    "question": q_text,
                    "options": [],
                    "correct_index": -1
                }
        elif is_a and current_q is not None:
            ans_text = ""
            # Xử lý trường hợp có "A, a, Nội dung" và "A, Nội dung"
            is_enumerator = full_row_str[1].lower().strip('.') in ['a', 'b', 'c', 'd', 'e', 'f', 'g']
            if is_enumerator and len(full_row_str) > 2 and full_row_str[2] != "":
                ans_text = full_row_str[2]
            else:
                ans_text = full_row_str[1]
            
            if ans_text:
                current_q["options"].append(ans_text)
                # Kiểm tra đánh dấu đáp án đúng "x" hoặc "X" ở các cột sau
                for cell in full_row_str[1:]:
                    if str(cell).lower() == 'x':
                        current_q["correct_index"] = len(current_q["options"]) - 1
                        break
                        
    if current_q and current_q["options"]:
        questions.append(current_q)
        
    return questions

# 1. Quản lý File và chọn Chủ đề
import sys
# Lấy đường dẫn chính xác của thư mục code ứng dụng để tránh lỗi khi deploy lên web
data_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
files = [f for f in os.listdir(data_dir) if (f.endswith('.xls') or f.endswith('.xlsx')) and not f.startswith('~')]

if not files:
    st.error(f"Không tìm thấy tệp Excel nào trong thư mục: {data_dir}")
    st.stop()

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3303/3303319.png", width=100)
st.sidebar.title("📚 Chủ Đề Bài Học")
selected_file = st.sidebar.radio("Chọn bộ đề:", files, format_func=lambda x: x.split('.')[0])

# Dữ liệu theo chủ đề
file_path = os.path.join(data_dir, selected_file)
sheets = get_sheets(file_path)
selected_sheet = st.sidebar.radio("Chọn chủ đề (sheet):", sheets)

questions = load_data(file_path, selected_sheet)

if not questions:
    st.warning("Xin lỗi, không có câu hỏi nào được lấy từ file và sheet được chọn.")
    st.stop()

st.title(f"📖 {selected_sheet} - {selected_file.split('.')[0]}")

# 2. Khởi tạo trạng thái Session
topic_key = f"{selected_file}_{selected_sheet}"
if 'current_topic' not in st.session_state or st.session_state.current_topic != topic_key:
    st.session_state.current_topic = topic_key
    st.session_state.current_q_index = 0
    st.session_state.checked = False
    
    # Xáo trộn câu hỏi
    shuffled_qs = list(questions)
    random.shuffle(shuffled_qs)
    st.session_state.session_questions = shuffled_qs

q_index = st.session_state.current_q_index
session_questions = st.session_state.session_questions

# Kết thúc bài
if q_index >= len(session_questions):
    st.balloons()
    st.success("🎉 Bạn đã hoàn thành toàn bộ câu hỏi của chủ đề này!")
    if st.button("Làm lại từ đầu", type="primary"):
        st.session_state.current_q_index = 0
        st.session_state.checked = False
        
        # Xáo trộn lại câu hỏi
        shuffled_qs = list(questions)
        random.shuffle(shuffled_qs)
        st.session_state.session_questions = shuffled_qs
        st.rerun()
    st.stop()

current_q = session_questions[q_index]

# Progress
st.progress(q_index / len(session_questions))
st.write(f"**Câu {q_index + 1} / {len(session_questions)}**")

# 3. Giao diện hiển thị Câu hỏi và Option
st.markdown(f"### {current_q['question']}")

options = current_q['options']
user_choice = st.radio("Chọn đáp án của bạn:", options, index=None, key=f"radio_{q_index}_{topic_key}")

# 4. Logic Kiểm tra (Check) và Qua câu (Next)

if st.button("Kiểm tra", type="primary", disabled=st.session_state.checked):
        if user_choice is None:
            st.warning("Bạn chưa chọn đáp án!")
        else:
            st.session_state.checked = True
            st.rerun()

if st.session_state.checked:
    correct_idx = current_q['correct_index']
    
    # Trường hợp data quên ko đánh dấu đúng (rất hiếm) -> mặc định câu đầu
    if correct_idx == -1:
        correct_idx = 0 
        
    correct_ans = options[correct_idx]
    
    if user_choice == correct_ans:
        st.markdown('''
            <div class="success-box">
                ✔️ Giỏi quá! Bạn đã trả lời chính xác.
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="error-box">
                ❌ Rất tiếc, bạn đã trả lời sai rồi.<br/>
                <div class="error-correct-ans">Đáp án đúng là: <b>{correct_ans}</b></div>
            </div>
        ''', unsafe_allow_html=True)
        
    st.write("") # spacing
    if st.button("Câu tiếp theo ➡️", type="primary"):
        st.session_state.current_q_index += 1
        st.session_state.checked = False
        st.rerun()
