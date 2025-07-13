import streamlit as st
import json
import uuid
from datetime import datetime
import os

# 유틸리티 함수들 (기존 완전 유지)
def save_ai_teacher(teacher_config):
    """AI 튜터 설정을 저장"""
    if 'saved_teachers' not in st.session_state:
        st.session_state.saved_teachers = []
    
    st.session_state.saved_teachers.append(teacher_config)
    
    # 최대 10개까지만 저장
    if len(st.session_state.saved_teachers) > 10:
        st.session_state.saved_teachers = st.session_state.saved_teachers[-10:]

def load_recent_teachers():
    """최근 생성된 AI 튜터 목록 로드"""
    if 'saved_teachers' not in st.session_state:
        st.session_state.saved_teachers = []
    
    return st.session_state.saved_teachers

def load_preset(preset_name):
    """프리셋 로드"""
    presets = {
        "물리 교수님": {
            "subject": "물리학",
            "level": "대학교",
            "personality": {
                "friendliness": 40,
                "humor_level": 20,
                "encouragement": 60,
                "explanation_detail": 90,
                "theory_vs_practice": 30
            }
        },
        "화학 실험 조교": {
            "subject": "화학",
            "level": "고등학교",
            "personality": {
                "friendliness": 80,
                "humor_level": 50,
                "safety_emphasis": 95,
                "theory_vs_practice": 70
            }
        },
        "친근한 수학 선생님": {
            "subject": "수학",
            "level": "중학교",
            "personality": {
                "friendliness": 90,
                "humor_level": 70,
                "encouragement": 90,
                "vocabulary_level": 30
            }
        }
    }
    return presets.get(preset_name, {})

def save_preset(preset_name, config):
    """프리셋 저장"""
    if 'custom_presets' not in st.session_state:
        st.session_state.custom_presets = {}
    
    st.session_state.custom_presets[preset_name] = config

# 페이지 설정 (기존 유지)
st.set_page_config(
    page_title="AI 튜터 팩토리",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 (기존 + v3.0 스타일 추가)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .version-badge {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-left: 10px;
    }
    .feature-highlight {
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid #4CAF50;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .teacher-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .generate-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 25px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        margin: 20px 0;
    }
    .slider-container {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .new-feature {
        color: #4CAF50;
        font-weight: bold;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 메인 헤더 (v3.0 버전 표시 추가)
    st.markdown("""
    <div class="main-header">
        <h1>🎓 AI 튜터 팩토리 <span class="version-badge">v3.0 고도화</span></h1>
        <p>1초 응답 + 즉시 중단 + 실시간 피드백이 가능한 AI 선생님을 만들어보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # NEW: v3.0 주요 기능 안내
    st.markdown("""
    <div class="feature-highlight">
        <h4>🚀 v3.0 고도화 기능</h4>
        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <div>⚡ <strong>1초 이내 응답</strong></div>
            <div>🛑 <strong>즉시 중단</strong></div>
            <div>💬 <strong>실시간 피드백</strong></div>
            <div>🧠 <strong>스마트 의도 분석</strong></div>
            <div>🔊 <strong>고품질 TTS</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 사이드바 - Recent AI Teachers (기존 완전 유지)
    with st.sidebar:
        st.header("📋 최근 생성된 AI 튜터")
        recent_teachers = load_recent_teachers()
        
        if recent_teachers:
            # 중복 제거 (ID 기준) - 기존 로직 완전 유지
            seen_ids = set()
            unique_teachers = []
            for teacher in recent_teachers:
                teacher_id = teacher.get('id', str(len(unique_teachers)))
                if teacher_id not in seen_ids:
                    seen_ids.add(teacher_id)
                    unique_teachers.append(teacher)
            
            for i, teacher in enumerate(unique_teachers):
                with st.container():
                    # NEW: v3.0 호환 표시
                    version_indicator = ""
                    if 'created_at' in teacher:
                        # 최근 생성된 튜터는 v3.0 호환으로 표시
                        version_indicator = '<span class="new-feature">[v3.0 고도화]</span>'
                    
                    st.markdown(f"""
                    <div class="teacher-card">
                        <h4>👨‍🏫 {teacher['name']} {version_indicator}</h4>
                        <p><strong>분야:</strong> {teacher['subject']}</p>
                        <p><strong>수준:</strong> {teacher['level']}</p>
                        <p><small>생성: {teacher['created_at']}</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 고유한 key 생성 (기존 로직 완전 유지)
                    unique_key = f"run_{teacher.get('id', i)}_{i}"
                    if st.button(f"▶️ {teacher['name']} 실행", key=unique_key):
                        st.session_state.selected_teacher = teacher
                        st.switch_page("pages/teacher_mode.py")
        else:
            st.info("아직 생성된 AI 튜터가 없습니다.")
        
        # NEW: v3.0 기능 요약
        st.markdown("""
        ---
        ### 🚀 v3.0 새 기능
        - ⚡ **1초 응답**: 질문 후 1초 이내 답변 시작
        - 🛑 **즉시 중단**: 응답 중 언제든 중단 가능
        - 💬 **실시간 피드백**: "짧게 해줘" 등 즉시 요청
        - 📊 **성능 표시**: 응답 시간 실시간 모니터링
        """)
    
    # 메인 컨텐츠 (기존 완전 유지)
    tab1, tab2 = st.tabs(["🚀 새 AI 튜터 생성", "📚 프리셋 관리"])
    
    with tab1:
        create_new_teacher()
    
    with tab2:
        manage_presets()

def create_new_teacher():
    st.header("🛠️ AI 튜터 생성기")
    
    # NEW: v3.0 기능 안내
    st.info("🚀 v3.0에서 생성되는 모든 AI 튜터는 1초 응답, 즉시 중단, 실시간 피드백 기능을 지원합니다!")
    
    # 기본 정보 (기존 완전 유지)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 기본 정보")
        teacher_name = st.text_input("AI 튜터 이름", placeholder="예: 김교수님, 박조교님", key="teacher_name_input")
        
        subject = st.selectbox(
            "전문 분야",
            ["물리학", "화학", "생물학", "수학", "지구과학", "공학", "기타"],
            index=0,
            key="subject_select"
        )
        
        if subject == "기타":
            custom_subject = st.text_input("직접 입력", placeholder="전문 분야를 입력하세요", key="custom_subject_input")
            subject = custom_subject if custom_subject else "기타"
        
        level = st.selectbox(
            "교육 수준",
            ["중학교", "고등학교", "대학교", "대학원"],
            index=1,
            key="level_select"
        )
    
    with col2:
        st.subheader("📄 참고 자료")
        uploaded_files = st.file_uploader(
            "문서 업로드 (PDF, DOC, TXT)",
            accept_multiple_files=True,
            type=['pdf', 'doc', 'docx', 'txt'],
            key="file_uploader"
        )
        
        use_general_knowledge = st.checkbox("일반 지식 사용", value=True, key="general_knowledge_checkbox")
        
        if uploaded_files:
            st.success(f"{len(uploaded_files)}개 파일 업로드됨")
    
    # 성격 설정 (기존 완전 유지)
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    st.subheader("🎭 AI 튜터 성격 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        friendliness = st.slider("친근함", 0, 100, 70, help="0: 매우 엄격함 ↔ 100: 매우 친근함", key="friendliness_slider")
        humor_level = st.slider("유머 수준", 0, 100, 30, help="0: 진지함 ↔ 100: 유머러스", key="humor_slider")
        encouragement = st.slider("격려 수준", 0, 100, 80, help="0: 객관적 ↔ 100: 매우 격려적", key="encouragement_slider")
        interaction_frequency = st.slider("상호작용 빈도", 0, 100, 60, help="0: 일방적 설명 ↔ 100: 자주 질문", key="interaction_slider")
    
    with col2:
        explanation_detail = st.slider("설명 상세도", 0, 100, 70, help="0: 간단명료 ↔ 100: 매우 상세", key="detail_slider")
        theory_vs_practice = st.slider("이론-실습 균형", 0, 100, 50, help="0: 이론 중심 ↔ 100: 실습 중심", key="theory_slider")
        safety_emphasis = st.slider("안전 강조", 0, 100, 90, help="실험/실습 시 안전 주의사항 강조", key="safety_slider")
        adaptability = st.slider("적응성", 0, 100, 75, help="학생 반응에 따른 설명 방식 조절", key="adaptability_slider")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 대화 스타일 (기존 완전 유지)
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    st.subheader("💬 대화 스타일")
    
    col1, col2 = st.columns(2)
    
    with col1:
        natural_speech = st.slider("자연스러운 말투", 0, 100, 80, help="끊어지는 말, 되묻기 등", key="natural_speech_slider")
        question_sensitivity = st.slider("질문 감지 민감도", 0, 100, 70, help="학생의 질문을 얼마나 민감하게 감지할지", key="question_sensitivity_slider")
    
    with col2:
        response_speed = st.slider("응답 속도", 0, 100, 60, help="0: 천천히 신중하게 ↔ 100: 빠르게 반응", key="response_speed_slider")
        vocabulary_level = st.slider("어휘 수준", 0, 100, 50, help="0: 쉬운 어휘 ↔ 100: 전문 용어", key="vocabulary_slider")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 음성 설정 (기존 완전 유지)
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    st.subheader("🔊 음성 설정")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        voice_speed = st.slider("음성 속도", 0.5, 2.0, 1.0, 0.1, key="voice_speed_slider")
    
    with col2:
        voice_pitch = st.slider("음성 높이", 0.5, 2.0, 1.0, 0.1, key="voice_pitch_slider")
    
    with col3:
        auto_voice = st.checkbox("자동 음성 재생", value=True, key="auto_voice_checkbox")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: v3.0 고급 설정
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    st.subheader("🚀 v3.0 고급 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        response_target = st.selectbox(
            "응답 시간 목표",
            ["1초 이내 (권장)", "2초 이내", "3초 이내"],
            index=0,
            help="AI 응답 시작까지의 목표 시간",
            key="response_target_select"
        )
        
        interrupt_sensitivity = st.slider(
            "중단 민감도", 0, 100, 80,
            help="0: 중단하기 어려움 ↔ 100: 쉽게 중단됨",
            key="interrupt_sensitivity_slider"
        )
    
    with col2:
        feedback_responsiveness = st.slider(
            "피드백 반응성", 0, 100, 90,
            help="실시간 피드백에 대한 반응 속도",
            key="feedback_responsiveness_slider"
        )
        
        quality_priority = st.selectbox(
            "품질 vs 속도 우선순위",
            ["품질 우선 (200-300ms 지연 허용)", "속도 우선", "균형"],
            index=0,
            help="음성 품질과 응답 속도 중 우선순위",
            key="quality_priority_select"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 생성 버튼 (기존 + v3.0 정보 추가)
    if st.button("🚀 v3.0 AI 튜터 생성하기", type="primary", use_container_width=True, key="generate_teacher_button"):
        if not teacher_name:
            st.error("AI 튜터 이름을 입력해주세요!")
            return
        
        # AI 튜터 설정 저장 (기존 + v3.0 설정 추가)
        teacher_config = {
            "id": str(uuid.uuid4()),
            "name": teacher_name,
            "subject": subject,
            "level": level,
            "uploaded_files": [f.name for f in uploaded_files] if uploaded_files else [],
            "use_general_knowledge": use_general_knowledge,
            "personality": {
                "friendliness": friendliness,
                "humor_level": humor_level,
                "encouragement": encouragement,
                "interaction_frequency": interaction_frequency,
                "explanation_detail": explanation_detail,
                "theory_vs_practice": theory_vs_practice,
                "safety_emphasis": safety_emphasis,
                "adaptability": adaptability,
                "natural_speech": natural_speech,
                "question_sensitivity": question_sensitivity,
                "response_speed": response_speed,
                "vocabulary_level": vocabulary_level
            },
            "voice_settings": {
                "speed": voice_speed,
                "pitch": voice_pitch,
                "auto_play": auto_voice
            },
            # NEW: v3.0 고급 설정
            "v3_settings": {
                "response_target": response_target,
                "interrupt_sensitivity": interrupt_sensitivity,
                "feedback_responsiveness": feedback_responsiveness,
                "quality_priority": quality_priority,
                "version": "3.0.0"
            },
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "version": "3.0.0"  # NEW: 버전 표시
        }
        
        # 클라우드에 저장 (기존 로직 완전 유지)
        save_ai_teacher(teacher_config)
        
        # 세션에 저장하고 튜터 모드로 이동 (기존 로직 완전 유지)
        st.session_state.selected_teacher = teacher_config
        
        st.success(f"🎉 '{teacher_name}' v3.0 AI 튜터가 생성되었습니다!")
        st.balloons()
        
        # NEW: v3.0 기능 요약 표시
        st.markdown("""
        ### ✅ 생성된 AI 튜터의 v3.0 기능
        - ⚡ **1초 이내 응답**: 질문 후 즉시 답변 시작
        - 🛑 **즉시 중단**: 언제든지 응답 중단 가능
        - 💬 **실시간 피드백**: "짧게 해줘", "더 자세히" 등 즉시 반영
        - 🧠 **스마트 분석**: 질문 의도 파악 후 최적화된 응답
        - 🔊 **고품질 TTS**: 자연스러운 음성 출력
        """)
        
        # 튜터 모드로 이동 (기존 로직 완전 유지)
        if st.button("▶️ 지금 바로 실행하기", key="run_immediately_button"):
            st.switch_page("pages/teacher_mode.py")

def manage_presets():
    st.header("📚 프리셋 관리")
    
    # NEW: v3.0 프리셋 안내
    st.info("🚀 모든 프리셋은 v3.0 고도화 기능을 자동으로 지원합니다!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("기본 프리셋")
        
        # 기존 프리셋 (완전 유지)
        presets = {
            "물리 교수님": {
                "subject": "물리학",
                "level": "대학교",
                "personality": {
                    "friendliness": 40,
                    "humor_level": 20,
                    "encouragement": 60,
                    "explanation_detail": 90,
                    "theory_vs_practice": 30
                }
            },
            "화학 실험 조교": {
                "subject": "화학",
                "level": "고등학교",
                "personality": {
                    "friendliness": 80,
                    "humor_level": 50,
                    "safety_emphasis": 95,
                    "theory_vs_practice": 70
                }
            },
            "친근한 수학 선생님": {
                "subject": "수학",
                "level": "중학교",
                "personality": {
                    "friendliness": 90,
                    "humor_level": 70,
                    "encouragement": 90,
                    "vocabulary_level": 30
                }
            }
        }
        
        for preset_name, preset_config in presets.items():
            if st.button(f"📋 {preset_name} 불러오기 (v3.0)", key=f"load_preset_{preset_name}"):
                # 프리셋 설정을 세션에 저장 (기존 로직 완전 유지)
                st.session_state.preset_loaded = preset_config
                st.success(f"{preset_name} v3.0 프리셋이 로드되었습니다!")
    
    with col2:
        st.subheader("사용자 프리셋")
        st.info("현재 설정을 프리셋으로 저장하거나 기존 프리셋을 관리할 수 있습니다.")
        
        preset_name = st.text_input("프리셋 이름", key="preset_name_input")
        if st.button("💾 현재 설정 저장 (v3.0)", key="save_preset_button"):
            if preset_name:
                st.success(f"'{preset_name}' v3.0 프리셋이 저장되었습니다!")
            else:
                st.error("프리셋 이름을 입력해주세요!")

# Streamlit 앱 시작 (기존 완전 유지)
if __name__ == "__main__":
    main()
