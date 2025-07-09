import streamlit as st

# 튜터 설정 확인
if 'selected_teacher' not in st.session_state:
    st.error("⚠️ 튜터 설정이 없습니다. 먼저 AI 튜터를 생성해주세요.")
    if st.button("🏠 AI 튜터 팩토리로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

teacher_config = st.session_state.selected_teacher

# 헤더
st.title(f"🎓 {teacher_config['name']} 선생님")
st.markdown(f"**과목:** {teacher_config['subject']} | **수준:** {teacher_config['level']}")

# 성공 메시지
st.success("🎉 페이지 전환 성공! 튜터 설정이 정상적으로 전달되었습니다.")

# 튜터 정보 간단 표시
st.subheader("👨‍🏫 튜터 정보")
st.write(f"이름: {teacher_config['name']}")
st.write(f"과목: {teacher_config['subject']}")
st.write(f"친근함: {teacher_config['personality']['friendliness']}%")

# 돌아가기 버튼
if st.button("🏠 튜터 팩토리로 돌아가기"):
    st.switch_page("app.py")

st.info("🚧 WebSocket 음성 대화 기능은 현재 개발 중입니다.")
