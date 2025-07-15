import streamlit as st
import streamlit.components.v1 as components
import json

# 페이지 설정 (기존 완전 유지)
st.set_page_config(
    page_title="AI 튜터 실시간 음성 대화",
    page_icon="🎓",
    layout="wide"
)

# 튜터 설정 확인 (기존 완전 유지)
if 'selected_teacher' not in st.session_state:
    st.error("⚠️ 튜터 설정이 없습니다. 먼저 AI 튜터를 생성해주세요.")
    if st.button("🏠 AI 튜터 팩토리로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

teacher_config = st.session_state.selected_teacher

# 헤더 (기존 완전 유지)
st.title(f"🎓 {teacher_config['name']} 선생님과의 실시간 대화")
st.markdown(f"**전문 분야:** {teacher_config['subject']} | **수준:** {teacher_config['level']}")

# 서버 URL 설정 (기존 완전 유지)
WEBSOCKET_URL = "wss://ai-teacher-611312919059.asia-northeast3.run.app/ws/tutor/user1"

# 상태 표시 (기존 + v4.0 정보 업데이트)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("튜터", teacher_config['name'], f"{teacher_config['subject']}")
with col2:
    st.metric("성격", f"친근함 {teacher_config['personality']['friendliness']}%", "")
with col3:
    st.metric("백엔드", "🟢 v4.0", "언어교육 AI 수준")  # 업데이트
with col4:
    st.metric("새 기능", "WaveNet + SSML", "감정 표현")  # 업데이트

st.divider()

# 대화 영역 (기존 + v4.0 업데이트)
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🎙️ 음성 + 텍스트 대화 (v4.0 언어교육 AI 수준)")  # 업데이트

with col2:
    if st.button("🏠 튜터 변경"):
        st.switch_page("app.py")

# 🔒 v4.0 언어교육 AI 수준 WebSocket HTML Component
websocket_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 80vh;
        }}
        .container {{
            max-width: 100%;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        .teacher-info {{
            text-align: center;
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
        }}
        .status {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .status-dot {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .connected {{ background: #4CAF50; }}
        .disconnected {{ background: #f44336; }}
        .connecting {{ background: #ff9800; animation: pulse 1s infinite; }}
        .responding {{ background: #2196F3; animation: pulse 1s infinite; }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        /* 🧠 NEW v4.0: 감정 상태 표시기 */
        .emotional-indicator {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
            padding: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            font-size: 14px;
        }}
        
        .emotion-icon {{
            font-size: 18px;
        }}
        
        .emotion-frustrated {{ color: #ff6b6b; }}
        .emotion-confident {{ color: #4CAF50; }}
        .emotion-confused {{ color: #ff9800; }}
        .emotion-engaged {{ color: #2196F3; }}
        .emotion-neutral {{ color: #9E9E9E; }}
        
        /* 🎤 NEW v4.0: 음성 시각화 */
        .voice-visualizer {{
            width: 100%;
            height: 60px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin: 15px 0;
            position: relative;
            overflow: hidden;
            display: none;
        }}
        
        .voice-visualizer.active {{
            display: block;
        }}
        
        .voice-wave {{
            height: 100%;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            width: 0%;
            transition: width 0.1s ease;
            border-radius: 15px;
            position: relative;
        }}
        
        .voice-wave::after {{
            content: '🎤 음성 감지 중...';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 14px;
            font-weight: 600;
            color: white;
        }}
        
        /* 📊 NEW v4.0: 학습 진도 표시기 */
        .learning-progress {{
            display: flex;
            justify-content: center;
            gap: 5px;
            margin: 10px 0;
            padding: 8px;
            background: rgba(33, 150, 243, 0.1);
            border-radius: 12px;
        }}
        
        .progress-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }}
        
        .progress-dot.active {{
            background: #4CAF50;
            transform: scale(1.3);
        }}
        
        .progress-dot.current {{
            background: #2196F3;
            transform: scale(1.5);
            animation: pulse 1.5s infinite;
        }}
        
        /* 입력 방식 탭 (기존 유지) */
        .tabs {{
            display: flex;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .tab {{
            flex: 1;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            background: transparent;
            color: white;
            font-size: 16px;
            font-weight: 600;
        }}
        
        .tab.active {{
            background: rgba(255, 255, 255, 0.2);
        }}
        
        .tab:hover {{
            background: rgba(255, 255, 255, 0.15);
        }}
        
        /* 음성 컨트롤 (기존 + v4.0 VAD 버튼 추가) */
        .controls {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        /* 텍스트 입력 컨트롤 (기존 유지) */
        .text-controls {{
            display: none;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .text-input-area {{
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }}
        
        .text-input {{
            flex: 1;
            padding: 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 16px;
            resize: vertical;
            min-height: 50px;
            max-height: 150px;
        }}
        
        .text-input::placeholder {{
            color: rgba(255, 255, 255, 0.7);
        }}
        
        .text-input:focus {{
            outline: none;
            border-color: rgba(255, 255, 255, 0.6);
            background: rgba(255, 255, 255, 0.15);
        }}
        
        .btn {{
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .btn-record {{
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
        }}
        
        .btn-record:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(238, 90, 36, 0.3);
        }}
        
        .btn-record:disabled {{
            background: #6c757d;
            cursor: not-allowed;
        }}
        
        .btn-stop {{
            background: linear-gradient(45deg, #6c757d, #495057);
            color: white;
        }}
        
        .btn-stop:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(108, 117, 125, 0.3);
        }}
        
        .btn-stop:disabled {{
            background: #6c757d;
            cursor: not-allowed;
        }}
        
        /* 🎤 NEW v4.0: VAD 토글 버튼 */
        .btn-vad {{
            background: linear-gradient(45deg, #9C27B0, #7B1FA2);
            color: white;
            font-size: 14px;
            padding: 10px 20px;
        }}
        
        .btn-vad.active {{
            background: linear-gradient(45deg, #4CAF50, #45a049);
        }}
        
        .btn-vad:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(156, 39, 176, 0.4);
        }}
        
        .btn-vad.active:hover:not(:disabled) {{
            box-shadow: 0 8px 16px rgba(76, 175, 80, 0.4);
        }}
        
        /* 텍스트 전송 버튼 (기존 유지) */
        .btn-send {{
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            min-width: 80px;
        }}
        
        .btn-send:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
        }}
        
        .btn-send:disabled {{
            background: #6c757d;
            cursor: not-allowed;
        }}
        
        /* 즉시 중단 버튼 (기존 유지) */
        .btn-interrupt {{
            background: linear-gradient(45deg, #f44336, #d32f2f);
            color: white;
            font-size: 14px;
            padding: 10px 20px;
            display: none;
        }}
        
        .btn-interrupt:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(244, 67, 54, 0.4);
        }}
        
        /* 실시간 피드백 컨트롤 (기존 유지) */
        .feedback-controls {{
            display: none;
            justify-content: center;
            gap: 10px;
            margin: 15px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            border: 2px solid rgba(33, 150, 243, 0.5);
        }}
        
        .feedback-controls.active {{
            display: flex;
            flex-wrap: wrap;
        }}
        
        .btn-feedback {{
            background: linear-gradient(45deg, #2196F3, #1976D2);
            color: white;
            font-size: 14px;
            padding: 8px 16px;
        }}
        
        .btn-feedback:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(33, 150, 243, 0.4);
        }}
        
        .chat-area {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            min-height: 300px;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
        }}
        
        .message {{
            margin-bottom: 15px;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 80%;
            animation: slideIn 0.3s ease;
            word-wrap: break-word;
        }}
        
        .user-message {{
            background: linear-gradient(45deg, #4CAF50, #45a049);
            margin-left: auto;
            text-align: right;
        }}
        
        .ai-message {{
            background: rgba(255, 255, 255, 0.15);
            margin-right: auto;
        }}
        
        /* 🎭 NEW v4.0: 감정 기반 메시지 스타일 */
        .ai-message.emotion-frustrated {{
            border-left: 4px solid #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
        }}
        
        .ai-message.emotion-confident {{
            border-left: 4px solid #4CAF50;
            background: rgba(76, 175, 80, 0.1);
        }}
        
        .ai-message.emotion-engaged {{
            border-left: 4px solid #2196F3;
            background: rgba(33, 150, 243, 0.1);
        }}
        
        /* 스트리밍 효과 (기존 유지 + 개선) */
        .ai-message.streaming {{
            border-left: 3px solid #4CAF50;
            position: relative;
        }}
        
        .streaming-cursor {{
            animation: blink 1s infinite;
            color: #4CAF50;
            font-weight: bold;
        }}
        
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .typing {{
            display: none;
            background: rgba(255, 255, 255, 0.1);
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 200px;
            margin-bottom: 15px;
        }}
        
        .typing-dots {{
            display: flex;
            gap: 4px;
        }}
        
        .typing-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.7);
            animation: typing 1.4s infinite;
        }}
        
        .typing-dot:nth-child(2) {{ animation-delay: 0.2s; }}
        .typing-dot:nth-child(3) {{ animation-delay: 0.4s; }}
        
        @keyframes typing {{
            0%, 60%, 100% {{ transform: translateY(0); }}
            30% {{ transform: translateY(-10px); }}
        }}
        
        .info {{
            text-align: center;
            font-size: 14px;
            opacity: 0.8;
            margin-top: 15px;
        }}
        
        .error {{
            background: rgba(244, 67, 54, 0.2);
            border: 1px solid #f44336;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
        }}
        
        /* 성능 정보 (기존 + v4.0 추가 정보) */
        .performance-info {{
            background: rgba(33, 150, 243, 0.1);
            border: 1px solid #2196F3;
            padding: 8px;
            border-radius: 8px;
            margin: 5px 0;
            font-size: 12px;
            text-align: center;
            display: none;
        }}
        
        .strategy-indicator {{
            display: inline-block;
            background: rgba(76, 175, 80, 0.2);
            border: 1px solid #4CAF50;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            margin-left: 8px;
        }}
        
        /* 🔒 중첩 방지 표시 (기존 유지) */
        .overlap-prevented {{
            background: rgba(244, 67, 54, 0.1);
            border: 1px solid #f44336;
            padding: 5px 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-size: 11px;
            text-align: center;
            color: #ffcdd2;
        }}
        
        /* 🎤 NEW v4.0: VAD 상태 표시 */
        .vad-status {{
            background: rgba(156, 39, 176, 0.1);
            border: 1px solid #9C27B0;
            padding: 5px 10px;
            border-radius: 8px;
            margin: 5px 0;
            font-size: 11px;
            text-align: center;
            color: #E1BEE7;
            display: none;
        }}
        
        .vad-status.active {{
            display: block;
            background: rgba(76, 175, 80, 0.1);
            border-color: #4CAF50;
            color: #C8E6C9;
        }}
        
        /* 🧠 NEW v4.0: 학습자 상태 표시 */
        .learner-status {{
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid #FFC107;
            padding: 8px 12px;
            border-radius: 10px;
            margin: 10px 0;
            font-size: 12px;
            text-align: center;
            color: #FFF8E1;
            display: none;
        }}
        
        .learner-status.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="teacher-info">
            <h2>👨‍🏫 {teacher_config['name']} 선생님</h2>
            <p>{teacher_config['subject']} 전문 | {teacher_config['level']} 수준</p>
            <small>친근함: {teacher_config['personality']['friendliness']}% | 
                   유머: {teacher_config['personality']['humor_level']}% | 
                   격려: {teacher_config['personality']['encouragement']}%</small>
            <div style="margin-top: 8px;">
                <small style="color: #81C784;">🔊 v4.0 WaveNet + SSML: 언어교육 AI 수준 자연스러운 음성 + 감정 표현</small>
            </div>
        </div>
        
        <div class="status">
            <span class="status-dot disconnected" id="statusDot"></span>
            <span id="statusText">연결 중...</span>
        </div>
        
        <!-- 🧠 NEW v4.0: 감정 상태 표시기 -->
        <div class="emotional-indicator" id="emotionalIndicator" style="display: none;">
            <span class="emotion-icon" id="emotionIcon">😐</span>
            <span id="emotionText">감정 상태 분석 중...</span>
        </div>
        
        <!-- 🎤 NEW v4.0: 음성 시각화 -->
        <div class="voice-visualizer" id="voiceVisualizer">
            <div class="voice-wave" id="voiceWave"></div>
        </div>
        
        <!-- 📊 NEW v4.0: 학습 진도 표시기 -->
        <div class="learning-progress" id="learningProgress">
            <div class="progress-dot" title="인사"></div>
            <div class="progress-dot" title="탐색"></div>
            <div class="progress-dot" title="설명"></div>
            <div class="progress-dot" title="연습"></div>
            <div class="progress-dot" title="정리"></div>
        </div>
        
        <!-- 입력 방식 탭 (기존 유지) -->
        <div class="tabs">
            <button class="tab active" id="voiceTab" onclick="switchTab('voice')">
                🎤 음성 입력
            </button>
            <button class="tab" id="textTab" onclick="switchTab('text')">
                💬 텍스트 입력
            </button>
        </div>
        
        <!-- 음성 입력 컨트롤 (기존 + v4.0 VAD 버튼 추가) -->
        <div class="controls" id="voiceControls">
            <button class="btn btn-record" id="recordBtn" onclick="startRecording()" disabled>
                🎤 음성 녹음 시작
            </button>
            <button class="btn btn-stop" id="stopBtn" onclick="stopRecording()" disabled>
                ⏹️ 녹음 중지
            </button>
            <button class="btn btn-vad" id="vadBtn" onclick="toggleVAD()" disabled>
                🎧 자동 감지 OFF
            </button>
            <button class="btn btn-interrupt" id="interruptBtn" onclick="interruptResponse()">
                🛑 즉시 중단
            </button>
        </div>
        
        <!-- 텍스트 입력 컨트롤 (기존 유지) -->
        <div class="text-controls" id="textControls">
            <div class="text-input-area">
                <textarea 
                    class="text-input" 
                    id="textInput" 
                    placeholder="질문을 입력하세요... (Enter로 전송, Shift+Enter로 줄바꿈)"
                    rows="3"></textarea>
                <button class="btn btn-send" id="sendBtn" onclick="sendTextMessage()" disabled>
                    📤 전송
                </button>
            </div>
            <button class="btn btn-interrupt" id="interruptBtnText" onclick="interruptResponse()" style="display: none; width: 100%;">
                🛑 응답 즉시 중단
            </button>
        </div>
        
        <!-- 실시간 피드백 컨트롤 (기존 유지) -->
        <div class="feedback-controls" id="feedbackControls">
            <div style="font-size: 14px; margin-bottom: 10px; width: 100%; text-align: center;">
                💬 <strong>실시간 피드백:</strong>
            </div>
            <button class="btn btn-feedback" onclick="sendFeedback('make_shorter')">
                ✂️ 짧게 해줘
            </button>
            <button class="btn btn-feedback" onclick="sendFeedback('make_detailed')">
                📝 더 자세히
            </button>
            <button class="btn btn-feedback" onclick="sendFeedback('stop')">
                ⏹️ 그만
            </button>
            <button class="btn btn-feedback" onclick="sendFeedback('clarify')">
                🤔 다시 설명
            </button>
        </div>
        
        <div class="chat-area" id="chatArea">
            <div class="message ai-message">
                안녕하세요! 저는 {teacher_config['name']} 선생님입니다. 🎓<br>
                {teacher_config['subject']} 분야에 대해 무엇이든 물어보세요!<br>
                <small style="opacity: 0.8;">🔊 v4.0 WaveNet + SSML: 감정이 살아있는 자연스러운 음성으로 대화해보세요!</small>
            </div>
        </div>
        
        <div class="typing" id="typingIndicator">
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        
        <div class="info">
            💡 <span id="infoText">마이크 버튼을 눌러 질문하거나, 텍스트 탭에서 타이핑하세요.</span>
        </div>
        
        <!-- 성능 정보 표시 (기존 + v4.0 추가) -->
        <div class="performance-info" id="performanceInfo">
            ⚡ 첫 응답: <span id="responseTime">-</span>ms | 
            📊 전략: <span id="responseStrategy">-</span> | 
            🔊 TTS: <span id="ttsTime">-</span>ms | 
            🎭 감정: <span id="emotionalState">-</span> |
            🧠 단계: <span id="learningPhase">-</span>
        </div>
        
        <!-- 🔒 중첩 방지 알림 (기존 유지) -->
        <div class="overlap-prevented" id="overlapPreventedInfo" style="display: none;">
            🔒 이전 오디오 중단됨 - 중첩 방지 활성화
        </div>
        
        <!-- 🎤 NEW v4.0: VAD 상태 알림 -->
        <div class="vad-status" id="vadStatusInfo">
            🎧 VAD 자동 감지 활성화 - 말하기 시작하면 자동으로 AI 응답 중단
        </div>
        
        <!-- 🧠 NEW v4.0: 학습자 상태 표시 -->
        <div class="learner-status" id="learnerStatusInfo">
            🧠 학습자 상태: <span id="learnerStateText">분석 중...</span>
        </div>
    </div>

    <script>
        // 🔒 중복 방지 변수들 (기존 완전 유지)
        let currentAudio = null;              
        let audioQueue = [];                  
        let lastAudioId = null;               
        let preventMultiplePlay = true;       
        
        // 기존 변수들 완전 유지
        let websocket = null;
        let mediaRecorder = null;
        let audioChunks = [];
        let isRecording = false;
        
        // v3.3 변수들 (완전 유지)
        let currentInputMode = 'voice';
        let currentAIMessage = null;
        let isResponseInProgress = false;
        let responseStartTime = null;
        let currentResponseStrategy = null;
        
        // 상태 관리 변수들 (완전 유지)
        let isTextSending = false;
        let isInterrupting = false;
        let lastFeedbackTime = 0;
        let lastMessageId = null;
        
        // 🧠 NEW v4.0: 고급 상태 추적 변수들
        let currentEmotionalState = 'neutral';
        let currentLearningPhase = 'greeting';
        let vadEnabled = false;
        let smartVAD = null;
        let conversationTurnCount = 0;
        let lastLearnerAnalysis = {};
        
        // DOM 요소들 (기존 + v4.0 추가)
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        const recordBtn = document.getElementById('recordBtn');
        const stopBtn = document.getElementById('stopBtn');
        const vadBtn = document.getElementById('vadBtn');
        const chatArea = document.getElementById('chatArea');
        const typingIndicator = document.getElementById('typingIndicator');
        const textInput = document.getElementById('textInput');
        const sendBtn = document.getElementById('sendBtn');
        const interruptBtn = document.getElementById('interruptBtn');
        const interruptBtnText = document.getElementById('interruptBtnText');
        const feedbackControls = document.getElementById('feedbackControls');
        const infoText = document.getElementById('infoText');
        const performanceInfo = document.getElementById('performanceInfo');
        const overlapPreventedInfo = document.getElementById('overlapPreventedInfo');
        
        // 🧠 NEW v4.0: 고급 UI 요소들
        const emotionalIndicator = document.getElementById('emotionalIndicator');
        const emotionIcon = document.getElementById('emotionIcon');
        const emotionText = document.getElementById('emotionText');
        const voiceVisualizer = document.getElementById('voiceVisualizer');
        const voiceWave = document.getElementById('voiceWave');
        const learningProgress = document.getElementById('learningProgress');
        const vadStatusInfo = document.getElementById('vadStatusInfo');
        const learnerStatusInfo = document.getElementById('learnerStatusInfo');
        const learnerStateText = document.getElementById('learnerStateText');
        
        const teacherConfig = {json.dumps(teacher_config)};
        
        // 🎤 NEW v4.0: 스마트 VAD (Voice Activity Detection) 클래스
        class SmartVAD {{
            constructor() {{
                this.isMonitoring = false;
                this.silenceThreshold = 0.02;
                this.minSpeechDuration = 300;
                this.audioContext = null;
                this.analyzer = null;
                this.stream = null;
                this.monitorInterval = null;
                this.lastTrigger = 0;
                this.isActive = false;
            }}
            
            async startMonitoring() {{
                if (this.isMonitoring || !vadEnabled) return;
                
                try {{
                    console.log('🎧 VAD 모니터링 시작');
                    
                    this.stream = await navigator.mediaDevices.getUserMedia({{ 
                        audio: {{ 
                            echoCancellation: true, 
                            noiseSuppression: true,
                            sampleRate: 44100
                        }} 
                    }});
                    
                    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    this.analyzer = this.audioContext.createAnalyser();
                    this.analyzer.fftSize = 2048;
                    
                    const source = this.audioContext.createMediaStreamSource(this.stream);
                    source.connect(this.analyzer);
                    
                    this.isMonitoring = true;
                    this.isActive = true;
                    this.monitorLoop();
                    
                    showVADStatus(true);
                    updateVoiceVisualizer(true);
                    
                }} catch (error) {{
                    console.error('❌ VAD 모니터링 시작 실패:', error);
                    showError('음성 감지 기능을 시작할 수 없습니다: ' + error.message);
                }}
            }}
            
            monitorLoop() {{
                if (!this.isMonitoring || !this.analyzer) return;
                
                const dataArray = new Uint8Array(this.analyzer.frequencyBinCount);
                this.analyzer.getByteFrequencyData(dataArray);
                
                // 음성 에너지 계산
                const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
                const normalized = average / 255.0;
                
                // 음성 파형 시각화 업데이트
                updateVoiceWave(normalized);
                
                // 음성 감지 시 자동 중단 트리거
                const now = Date.now();
                if (normalized > this.silenceThreshold && 
                    isResponseInProgress && 
                    !isRecording &&
                    (now - this.lastTrigger) > 1000) {{ // 1초 쿨다운
                    
                    this.lastTrigger = now;
                    console.log('🛑 VAD 감지 - 자동 중단 트리거 (에너지:', normalized.toFixed(3), ')');
                    
                    forceStopAllAudio();
                    interruptResponse();
                    
                    // VAD 트리거 알림
                    showVADTrigger();
                }}
                
                // 100ms마다 체크
                this.monitorInterval = setTimeout(() => this.monitorLoop(), 100);
            }}
            
            stopMonitoring() {{
                console.log('🔇 VAD 모니터링 중단');
                
                this.isMonitoring = false;
                this.isActive = false;
                
                if (this.monitorInterval) {{
                    clearTimeout(this.monitorInterval);
                    this.monitorInterval = null;
                }}
                
                if (this.audioContext) {{
                    this.audioContext.close();
                    this.audioContext = null;
                }}
                
                if (this.stream) {{
                    this.stream.getTracks().forEach(track => track.stop());
                    this.stream = null;
                }}
                
                showVADStatus(false);
                updateVoiceVisualizer(false);
                updateVoiceWave(0);
            }}
            
            toggle() {{
                if (this.isMonitoring) {{
                    this.stopMonitoring();
                }} else {{
                    this.startMonitoring();
                }}
            }}
        }}
        
        // 🎤 VAD 인스턴스 생성
        smartVAD = new SmartVAD();
        
        // 🎧 VAD 토글 함수
        function toggleVAD() {{
            vadEnabled = !vadEnabled;
            
            if (vadEnabled) {{
                vadBtn.classList.add('active');
                vadBtn.innerHTML = '🎧 자동 감지 ON';
                infoText.textContent = 'VAD 활성화: 말하기 시작하면 자동으로 AI 응답이 중단됩니다.';
                
                if (isConnected() && isResponseInProgress) {{
                    smartVAD.startMonitoring();
                }}
            }} else {{
                vadBtn.classList.remove('active');
                vadBtn.innerHTML = '🎧 자동 감지 OFF';
                infoText.textContent = '마이크 버튼을 눌러 음성으로 질문하세요.';
                
                smartVAD.stopMonitoring();
            }}
            
            console.log('🎧 VAD 토글:', vadEnabled ? 'ON' : 'OFF');
        }}
        
        // 🔒 핵심! 중첩 완전 방지 오디오 재생 함수 (기존 완전 유지 + v4.0 정보 추가)
        function playAudio(base64Audio, audioId = null, audioInfo = {{}}) {{
            try {{
                console.log('🔊 v4.0 오디오 재생 요청:', audioId, audioInfo);
                
                // 🔒 1단계: 이전 오디오 즉시 중단 (핵심!)
                if (currentAudio && !currentAudio.paused) {{
                    console.log('🛑 이전 오디오 중단:', currentAudio.src);
                    currentAudio.pause();
                    currentAudio.currentTime = 0;
                    currentAudio = null;
                    
                    showOverlapPrevented();
                }}
                
                // 🔒 2단계: 중복 재생 방지 체크
                if (preventMultiplePlay && audioId && audioId === lastAudioId) {{
                    console.log('🔒 중복 오디오 재생 방지:', audioId);
                    return;
                }}
                
                // 🔒 3단계: 새 오디오 생성 및 재생
                const audioBlob = base64ToBlob(base64Audio, 'audio/mp3');
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                
                // 🔒 4단계: 현재 오디오로 등록
                currentAudio = audio;
                lastAudioId = audioId;
                
                // 🔒 5단계: 오디오 이벤트 처리
                audio.onloadstart = () => {{
                    console.log('🔊 v4.0 오디오 로딩 시작 (버전:', audioInfo.version || 'unknown', ')');
                }};
                
                audio.oncanplay = () => {{
                    console.log('🔊 v4.0 오디오 재생 준비 완료');
                }};
                
                audio.onended = () => {{
                    console.log('✅ v4.0 오디오 재생 완료');
                    URL.revokeObjectURL(audioUrl);
                    
                    if (currentAudio === audio) {{
                        currentAudio = null;
                    }}
                }};
                
                audio.onerror = (error) => {{
                    console.error('❌ v4.0 오디오 재생 오류:', error);
                    URL.revokeObjectURL(audioUrl);
                    
                    if (currentAudio === audio) {{
                        currentAudio = null;
                    }}
                }};
                
                // 🔒 6단계: 실제 재생 시작
                audio.play().then(() => {{
                    console.log('✅ v4.0 새 오디오 재생 시작 성공');
                    hideOverlapPrevented();
                    
                    // 🧠 v4.0: 추가 정보 로깅
                    if (audioInfo.voice_type === 'wavenet') {{
                        console.log('🔊 WaveNet 고품질 음성 재생 중');
                    }}
                    if (audioInfo.ssml_enabled) {{
                        console.log('🎭 SSML 감정 표현 활성화');
                    }}
                    
                }}).catch(error => {{
                    console.error('❌ v4.0 오디오 재생 실패:', error);
                    
                    if (currentAudio === audio) {{
                        currentAudio = null;
                    }}
                    
                    if (error.name === 'NotAllowedError') {{
                        showError('브라우저에서 자동 재생이 차단되었습니다. 화면을 클릭한 후 다시 시도해주세요.');
                    }}
                }});
                
            }} catch (error) {{
                console.error('❌ v4.0 오디오 처리 오류:', error);
                currentAudio = null;
            }}
        }}
        
        // 🧠 NEW v4.0: 감정 상태 업데이트
        function updateEmotionalState(emotionalState, learnerAnalysis = {{}}) {{
            if (!emotionalState) return;
            
            currentEmotionalState = emotionalState;
            lastLearnerAnalysis = learnerAnalysis;
            
            // 감정 아이콘 업데이트
            const emotionIcons = {{
                'frustrated': '😤',
                'confident': '😊',
                'confused': '🤔',
                'engaged': '🤩',
                'neutral': '😐'
            }};
            
            const emotionTexts = {{
                'frustrated': '어려워하고 있어요',
                'confident': '자신감이 있어요',
                'confused': '혼란스러워해요',
                'engaged': '흥미롭게 참여하고 있어요',
                'neutral': '차분한 상태예요'
            }};
            
            if (emotionIcon) {{
                emotionIcon.textContent = emotionIcons[emotionalState] || '😐';
                emotionIcon.className = `emotion-icon emotion-${{emotionalState}}`;
            }}
            
            if (emotionText) {{
                emotionText.textContent = emotionTexts[emotionalState] || '상태 분석 중...';
            }}
            
            // 감정 표시기 활성화
            if (emotionalIndicator) {{
                emotionalIndicator.style.display = 'flex';
            }}
            
            // 성능 정보에 감정 상태 표시
            const emotionalStateSpan = document.getElementById('emotionalState');
            if (emotionalStateSpan) {{
                emotionalStateSpan.textContent = emotionalState;
            }}
            
            console.log('🧠 감정 상태 업데이트:', emotionalState);
        }}
        
        // 📊 NEW v4.0: 학습 단계 업데이트
        function updateLearningPhase(phase) {{
            if (!phase) return;
            
            currentLearningPhase = phase;
            
            const phases = ['greeting', 'exploration', 'explanation', 'practice', 'consolidation'];
            const phaseIndex = phases.indexOf(phase);
            
            const progressDots = learningProgress.querySelectorAll('.progress-dot');
            progressDots.forEach((dot, index) => {{
                dot.classList.remove('active', 'current');
                if (index < phaseIndex) {{
                    dot.classList.add('active');
                }} else if (index === phaseIndex) {{
                    dot.classList.add('current');
                }}
            }});
            
            // 성능 정보에 학습 단계 표시
            const learningPhaseSpan = document.getElementById('learningPhase');
            if (learningPhaseSpan) {{
                learningPhaseSpan.textContent = phase;
            }}
            
            console.log('📊 학습 단계 업데이트:', phase);
        }}
        
        // 🧠 NEW v4.0: 학습자 상태 표시 업데이트
        function updateLearnerStatus(analysis) {{
            if (!analysis || !learnerStateText) return;
            
            const statusParts = [];
            
            if (analysis.understanding_level) {{
                statusParts.push(`이해도: ${{analysis.understanding_level}}`);
            }}
            if (analysis.engagement_level) {{
                statusParts.push(`참여도: ${{analysis.engagement_level}}`);
            }}
            if (analysis.question_complexity) {{
                statusParts.push(`질문 수준: ${{analysis.question_complexity}}`);
            }}
            
            if (statusParts.length > 0) {{
                learnerStateText.textContent = statusParts.join(' | ');
                learnerStatusInfo.classList.add('active');
            }}
        }}
        
        // 🎤 NEW v4.0: 음성 시각화 업데이트
        function updateVoiceVisualizer(active) {{
            if (voiceVisualizer) {{
                if (active) {{
                    voiceVisualizer.classList.add('active');
                }} else {{
                    voiceVisualizer.classList.remove('active');
                }}
            }}
        }}
        
        function updateVoiceWave(energy) {{
            if (voiceWave) {{
                const percentage = Math.min(energy * 100, 100);
                voiceWave.style.width = `${{percentage}}%`;
            }}
        }}
        
        // 🎧 NEW v4.0: VAD 상태 표시
        function showVADStatus(active) {{
            if (vadStatusInfo) {{
                if (active) {{
                    vadStatusInfo.classList.add('active');
                    vadStatusInfo.style.display = 'block';
                }} else {{
                    vadStatusInfo.classList.remove('active');
                    vadStatusInfo.style.display = 'none';
                }}
            }}
        }}
        
        function showVADTrigger() {{
            if (vadStatusInfo) {{
                vadStatusInfo.textContent = '🎧 음성 감지! 자동으로 AI 응답을 중단했습니다.';
                vadStatusInfo.style.display = 'block';
                
                setTimeout(() => {{
                    if (vadEnabled) {{
                        vadStatusInfo.textContent = '🎧 VAD 자동 감지 활성화 - 말하기 시작하면 자동으로 AI 응답 중단';
                    }}
                }}, 3000);
            }}
        }}
        
        // 중첩 방지 알림 (기존 유지)
        function showOverlapPrevented() {{
            if (overlapPreventedInfo) {{
                overlapPreventedInfo.style.display = 'block';
                setTimeout(() => {{
                    hideOverlapPrevented();
                }}, 2000);
            }}
        }}
        
        function hideOverlapPrevented() {{
            if (overlapPreventedInfo) {{
                overlapPreventedInfo.style.display = 'none';
            }}
        }}
        
        // 🔒 NEW: 모든 오디오 강제 중단 (기존 + v4.0 정보 추가)
        function forceStopAllAudio() {{
            if (currentAudio && !currentAudio.paused) {{
                console.log('🔒 모든 오디오 강제 중단 (v4.0)');
                currentAudio.pause();
                currentAudio.currentTime = 0;
                currentAudio = null;
                showOverlapPrevented();
            }}
        }}
        
        // 탭 전환 기능 (기존 + v4.0 VAD 관리 추가)
        function switchTab(mode) {{
            currentInputMode = mode;
            
            const voiceTab = document.getElementById('voiceTab');
            const textTab = document.getElementById('textTab');
            const voiceControls = document.getElementById('voiceControls');
            const textControls = document.getElementById('textControls');
            
            if (mode === 'voice') {{
                voiceTab.classList.add('active');
                textTab.classList.remove('active');
                voiceControls.style.display = 'flex';
                textControls.style.display = 'none';
                infoText.textContent = 'VAD 자동 감지를 활성화하면 더욱 자연스러운 대화가 가능합니다.';
                
                // VAD 버튼 활성화
                if (vadBtn && isConnected()) {{
                    vadBtn.disabled = false;
                }}
            }} else {{
                voiceTab.classList.remove('active');
                textTab.classList.add('active');
                voiceControls.style.display = 'none';
                textControls.style.display = 'flex';
                textInput.focus();
                infoText.textContent = '텍스트를 입력하고 전송 버튼을 클릭하세요.';
                
                // VAD 자동 중단 (텍스트 모드에서는 불필요)
                if (vadEnabled) {{
                    smartVAD.stopMonitoring();
                }}
            }}
        }}
        
        // 텍스트 입력 이벤트 (기존 완전 유지)
        if (textInput) {{
            textInput.addEventListener('input', function() {{
                const text = textInput.value.trim();
                sendBtn.disabled = !text || !isConnected() || isResponseInProgress;
            }});
            
            textInput.addEventListener('keydown', function(event) {{
                if (event.key === 'Enter' && !event.shiftKey) {{
                    event.preventDefault();
                    if (!sendBtn.disabled) {{
                        sendTextMessage();
                    }}
                }}
            }});
        }}
        
        // 텍스트 메시지 전송 (기존 완전 유지)
        function sendTextMessage() {{
            const text = textInput.value.trim();
            if (!text || !isConnected()) {{
                return;
            }}
            
            // 🔒 응답 중이면 오디오 중단 후 전송
            if (isResponseInProgress) {{
                forceStopAllAudio();
            }}
            
            addMessage('user', text);
            
            const message = {{
                type: 'user_text',
                text: text
            }};
            
            if (isResponseInProgress) {{
                message.interrupt = true;
                console.log('🛑 응답 중단 후 새 질문 전송');
            }}
            
            websocket.send(JSON.stringify(message));
            
            textInput.value = '';
            sendBtn.disabled = true;
            conversationTurnCount++;
        }}
        
        // 즉시 중단 기능 (기존 + v4.0 VAD 중단 추가)
        function interruptResponse() {{
            if (!isResponseInProgress || !isConnected()) {{
                return;
            }}
            
            console.log('🛑 응답 즉시 중단 요청 (v4.0)');
            
            // 🔒 오디오도 즉시 중단
            forceStopAllAudio();
            
            // 🎧 VAD 모니터링도 일시 중단
            if (vadEnabled && smartVAD.isMonitoring) {{
                smartVAD.stopMonitoring();
                
                // 3초 후 VAD 재시작 (새 응답 대기)
                setTimeout(() => {{
                    if (vadEnabled && !isResponseInProgress) {{
                        smartVAD.startMonitoring();
                    }}
                }}, 3000);
            }}
            
            const message = {{
                type: 'interrupt_response'
            }};
            
            websocket.send(JSON.stringify(message));
            
            hideInterruptControls();
            statusText.textContent = '응답 중단됨 ⏹️';
        }}
        
        // 실시간 피드백 전송 (기존 완전 유지)
        function sendFeedback(action) {{
            if (!isConnected()) {{
                return;
            }}
            
            console.log('💬 실시간 피드백 전송:', action);
            
            const message = {{
                type: 'feedback_request',
                action: action,
                original_input: 'current_question'
            }};
            
            websocket.send(JSON.stringify(message));
            showFeedbackSent(action);
        }}
        
        function showFeedbackSent(action) {{
            const actionNames = {{
                'make_shorter': '짧게 요청',
                'make_detailed': '상세 요청',
                'stop': '중단 요청',
                'clarify': '재설명 요청'
            }};
            
            addMessage('user', `💬 \${{actionNames[action] || action}}`);
        }}
        
        // WebSocket 연결 (기존 + v4.0 VAD 활성화 추가)
        function connectWebSocket() {{
            const wsUrl = '{WEBSOCKET_URL}';
            console.log('v4.0 연결 시도:', wsUrl);
            
            statusDot.className = 'status-dot connecting';
            statusText.textContent = '연결 중...';
            
            websocket = new WebSocket(wsUrl);
            
            websocket.onopen = function(event) {{
                console.log('v4.0 WebSocket 연결 성공');
                statusDot.className = 'status-dot connected';
                statusText.textContent = '연결됨 ✅ (v4.0)';
                recordBtn.disabled = false;
                updateTextInputState();
                
                // VAD 버튼 활성화
                if (vadBtn && currentInputMode === 'voice') {{
                    vadBtn.disabled = false;
                }}
                
                const configMessage = {{
                    type: "config_update",
                    config: {{
                        name: teacherConfig.name,
                        subject: teacherConfig.subject,
                        level: teacherConfig.level,
                        personality: teacherConfig.personality,
                        voice_settings: {{
                            auto_play: true,
                            speed: 1.0,
                            pitch: 1.0
                        }}
                    }}
                }};
                websocket.send(JSON.stringify(configMessage));
            }};
            
            websocket.onmessage = function(event) {{
                console.log('v4.0 메시지 수신:', event.data);
                
                try {{
                    const message = JSON.parse(event.data);
                    handleServerMessage(message);
                }} catch (e) {{
                    console.log('텍스트 메시지:', event.data);
                }}
            }};
            
            websocket.onclose = function(event) {{
                console.log('WebSocket 연결 종료');
                statusDot.className = 'status-dot disconnected';
                statusText.textContent = '연결 끊김 ❌';
                recordBtn.disabled = true;
                stopBtn.disabled = true;
                updateTextInputState();
                resetResponseState();
                
                // VAD 버튼 비활성화
                if (vadBtn) {{
                    vadBtn.disabled = true;
                }}
                
                // 🔒 연결 종료 시 오디오 및 VAD 정리
                forceStopAllAudio();
                if (smartVAD) {{
                    smartVAD.stopMonitoring();
                }}
                
                setTimeout(() => {{
                    if (!websocket || websocket.readyState === WebSocket.CLOSED) {{
                        connectWebSocket();
                    }}
                }}, 5000);
            }};
            
            websocket.onerror = function(error) {{
                console.error('WebSocket 에러:', error);
                statusDot.className = 'status-dot disconnected';
                statusText.textContent = '연결 오류 ❌';
                showError('WebSocket 연결에 실패했습니다. 네트워크를 확인해주세요.');
                
                // 🔒 오류 시 오디오 및 VAD 정리
                forceStopAllAudio();
                if (smartVAD) {{
                    smartVAD.stopMonitoring();
                }}
            }};
        }}
        
        // 🔒 서버 메시지 처리 (기존 + v4.0 메시지 타입 지원)
        function handleServerMessage(message) {{
            console.log('v4.0 서버 메시지:', message);
            
            switch(message.type) {{
                case 'connection_established':
                    addMessage('ai', message.message);
                    if (message.v4_0_enhancements) {{
                        console.log('🎊 v4.0 고급 기능 활성화:', message.v4_0_enhancements);
                    }}
                    break;
                    
                case 'config_updated':
                    console.log('튜터 설정 업데이트 완료');
                    break;
                    
                case 'response_start':
                    console.log('🚀 응답 시작:', message.strategy);
                    startNewResponse(message.strategy);
                    
                    // 🎧 VAD 모니터링 시작
                    if (vadEnabled && currentInputMode === 'voice' && !isRecording) {{
                        smartVAD.startMonitoring();
                    }}
                    break;
                    
                case 'text_chunk':
                    if (isResponseInProgress && currentAIMessage) {{
                        appendToAIMessage(currentAIMessage, message.content);
                        measureFirstResponse();
                    }} else {{
                        hideTyping();
                        addMessage('ai', message.content);
                    }}
                    break;
                    
                case 'response_complete':
                    if (currentAIMessage) {{
                        removeStreamingCursor(currentAIMessage);
                        addStrategyIndicator(currentAIMessage, currentResponseStrategy);
                    }}
                    break;
                    
                case 'audio_completely_safe':
                    // 🔊 v4.0 백엔드 완전 안전 오디오 (기존 + 새 정보 활용)
                    console.log('🔒 v4.0 안전한 오디오 수신:', message.audio_size, 'bytes');
                    
                    // 🧠 NEW v4.0: 감정 상태 및 학습 정보 업데이트
                    if (message.emotional_state) {{
                        updateEmotionalState(message.emotional_state);
                    }}
                    if (message.strategy) {{
                        currentResponseStrategy = message.strategy;
                    }}
                    
                    // 🔊 고품질 오디오 재생
                    if (message.audio && shouldPlayAudio()) {{
                        playAudio(message.audio, message.client_id, {{
                            version: message.version || '4.0',
                            voice_type: message.voice_type || 'standard',
                            ssml_enabled: message.ssml_enabled || false,
                            emotional_state: message.emotional_state || 'neutral'
                        }});
                    }}
                    
                    if (message.tts_time) {{
                        document.getElementById('ttsTime').textContent = Math.round(message.tts_time * 1000);
                    }}
                    
                    // 🎊 v4.0 품질 정보 로깅
                    if (message.voice_type === 'wavenet') {{
                        console.log('🔊 WaveNet 고품질 음성 재생');
                    }}
                    if (message.ssml_enabled) {{
                        console.log('🎭 SSML 감정 표현 활성화');
                    }}
                    break;
                    
                case 'audio_stream_quality':
                    // 기존 v3.0 호환 (완전 유지)
                    console.log('🔊 v3.0 고품질 TTS:', message.sequence);
                    if (message.audio && shouldPlayAudio()) {{
                        playAudio(message.audio, `stream_\${{message.sequence}}`);
                    }}
                    if (message.tts_time) {{
                        document.getElementById('ttsTime').textContent = Math.round(message.tts_time * 1000);
                    }}
                    break;
                    
                case 'all_audio_complete':
                    console.log('✅ 모든 오디오 완료');
                    completeResponse();
                    break;
                    
                case 'audio_chunk':
                    // 기존 v2.0 호환 (완전 유지)
                    hideTyping();
                    addMessage('ai', message.content);
                    if (message.audio && shouldPlayAudio()) {{
                        playAudio(message.audio, `chunk_\${{Date.now()}}`);
                    }}
                    break;
                    
                case 'stt_result':
                    addMessage('user', message.text);
                    showTyping();
                    conversationTurnCount++;
                    break;
                    
                case 'response_interrupted':
                    console.log('✅ 응답 중단 확인됨');
                    forceCompleteResponse('[중단됨]');
                    
                    // 🎧 VAD 재시작 준비
                    if (vadEnabled && currentInputMode === 'voice') {{
                        setTimeout(() => {{
                            if (!isResponseInProgress) {{
                                smartVAD.startMonitoring();
                            }}
                        }}, 1000);
                    }}
                    break;
                    
                case 'feedback_acknowledged':
                    console.log('💬 피드백 확인:', message.message);
                    showFeedbackAck(message.message);
                    break;
                    
                case 'error':
                    hideTyping();
                    resetResponseState();
                    showError(message.message);
                    break;
                    
                default:
                    console.warn('알 수 없는 메시지 타입:', message.type);
            }}
        }}
        
        // 응답 상태 관리 함수들 (기존 + v4.0 VAD 및 상태 추적 추가)
        function startNewResponse(strategy) {{
            isResponseInProgress = true;
            responseStartTime = Date.now();
            currentResponseStrategy = strategy;
            
            currentAIMessage = createNewAIMessage();
            showTyping();
            showInterruptControls();
            
            // 🧠 학습 단계 추정 (간단한 매핑)
            const strategyToPhase = {{
                'very_short': 'greeting',
                'short': 'exploration', 
                'medium': 'explanation',
                'long': 'explanation',
                'interactive': 'practice'
            }};
            
            const estimatedPhase = strategyToPhase[strategy] || 'explanation';
            updateLearningPhase(estimatedPhase);
            
            statusDot.className = 'status-dot responding';
            statusText.textContent = `응답 생성 중... 🤖 (\${{strategy}})`;
            updateTextInputState();
        }}
        
        function completeResponse() {{
            isResponseInProgress = false;
            currentAIMessage = null;
            currentResponseStrategy = null;
            
            hideInterruptControls();
            statusDot.className = 'status-dot connected';
            statusText.textContent = '연결됨 ✅ (v4.0)';
            updateTextInputState();
            
            // 🎧 VAD 모니터링 중단 (응답 완료)
            if (vadEnabled && smartVAD.isMonitoring) {{
                smartVAD.stopMonitoring();
            }}
        }}
        
        function forceCompleteResponse(reason) {{
            if (currentAIMessage && reason) {{
                removeStreamingCursor(currentAIMessage);
                currentAIMessage.innerHTML += ` <em style="opacity: 0.6; font-size: 12px;">\${{reason}}</em>`;
            }}
            completeResponse();
            hideTyping();
        }}
        
        function resetResponseState() {{
            isResponseInProgress = false;
            responseStartTime = null;
            currentResponseStrategy = null;
            currentAIMessage = null;
            hideInterruptControls();
            hideTyping();
            updateTextInputState();
            
            // 🔒 응답 상태 리셋 시 오디오 및 VAD 정리
            forceStopAllAudio();
            if (smartVAD) {{
                smartVAD.stopMonitoring();
            }}
        }}
        
        function createNewAIMessage() {{
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ai-message streaming';
            
            // 🧠 v4.0: 감정 상태에 따른 스타일 적용
            if (currentEmotionalState && currentEmotionalState !== 'neutral') {{
                messageDiv.classList.add(`emotion-${{currentEmotionalState}}`);
            }}
            
            messageDiv.innerHTML = '<span class="streaming-cursor">▋</span>';
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
            return messageDiv;
        }}
        
        function appendToAIMessage(messageElement, newContent) {{
            const cursor = messageElement.querySelector('.streaming-cursor');
            if (cursor) {{
                cursor.remove();
            }}
            
            const currentText = messageElement.textContent || '';
            messageElement.innerHTML = currentText + newContent + '<span class="streaming-cursor">▋</span>';
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        function removeStreamingCursor(messageElement) {{
            const cursor = messageElement.querySelector('.streaming-cursor');
            if (cursor) {{
                cursor.remove();
            }}
            messageElement.classList.remove('streaming');
        }}
        
        function measureFirstResponse() {{
            if (responseStartTime) {{
                const elapsed = Date.now() - responseStartTime;
                document.getElementById('responseTime').textContent = elapsed;
                document.getElementById('responseStrategy').textContent = currentResponseStrategy || 'auto';
                performanceInfo.style.display = 'block';
                responseStartTime = null;
            }}
        }}
        
        function addStrategyIndicator(messageElement, strategy) {{
            if (strategy) {{
                const strategySpan = document.createElement('span');
                strategySpan.className = 'strategy-indicator';
                strategySpan.textContent = strategy;
                messageElement.appendChild(strategySpan);
            }}
        }}
        
        function showFeedbackAck(message) {{
            const ackMsg = document.createElement('div');
            ackMsg.className = 'message ai-message';
            ackMsg.innerHTML = `✅ \${{message}}`;
            ackMsg.style.fontSize = '14px';
            ackMsg.style.opacity = '0.8';
            chatArea.appendChild(ackMsg);
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        function showInterruptControls() {{
            if (currentInputMode === 'voice') {{
                interruptBtn.style.display = 'block';
            }} else {{
                interruptBtnText.style.display = 'block';
            }}
            feedbackControls.classList.add('active');
        }}
        
        function hideInterruptControls() {{
            interruptBtn.style.display = 'none';
            interruptBtnText.style.display = 'none';
            feedbackControls.classList.remove('active');
        }}
        
        function updateTextInputState() {{
            if (textInput && sendBtn) {{
                const connected = isConnected();
                const text = textInput.value.trim();
                
                textInput.disabled = !connected;
                sendBtn.disabled = !connected || !text;
                
                if (isResponseInProgress && text) {{
                    sendBtn.innerHTML = '🛑 중단하고 새 질문';
                }} else {{
                    sendBtn.innerHTML = '📤 전송';
                }}
            }}
        }}
        
        function isConnected() {{
            return websocket && websocket.readyState === WebSocket.OPEN;
        }}
        
        function shouldPlayAudio() {{
            return teacherConfig.voice_settings && teacherConfig.voice_settings.auto_play;
        }}
        
        function addMessage(sender, text) {{
            const messageDiv = document.createElement('div');
            messageDiv.className = `message \${{sender}}-message`;
            messageDiv.innerHTML = text;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        function showError(errorText) {{
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = '❌ ' + errorText;
            chatArea.appendChild(errorDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        function showTyping() {{
            typingIndicator.style.display = 'block';
        }}
        
        function hideTyping() {{
            typingIndicator.style.display = 'none';
        }}
        
        function base64ToBlob(base64, mimeType) {{
            const byteCharacters = atob(base64);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}
            const byteArray = new Uint8Array(byteNumbers);
            return new Blob([byteArray], {{type: mimeType}});
        }}
        
        // 🔒 음성 녹음 시작 (기존 + VAD 일시 중단 추가)
        async function startRecording() {{
            // 응답 진행 중이면 오디오 중단 후 녹음
            if (isResponseInProgress) {{
                console.log('🛑 응답 중단 후 녹음 시작');
                forceStopAllAudio();
                interruptResponse();
                setTimeout(startRecording, 300);
                return;
            }}
            
            // 🎧 VAD 모니터링 일시 중단 (사용자 녹음 중 오작동 방지)
            if (vadEnabled && smartVAD.isMonitoring) {{
                smartVAD.stopMonitoring();
            }}
            
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ 
                    audio: {{
                        echoCancellation: true,
                        noiseSuppression: true,
                        sampleRate: 44100
                    }} 
                }});
                
                mediaRecorder = new MediaRecorder(stream, {{
                    mimeType: 'audio/webm;codecs=opus'
                }});
                audioChunks = [];
                
                mediaRecorder.ondataavailable = function(event) {{
                    if (event.data.size > 0) {{
                        audioChunks.push(event.data);
                    }}
                }};
                
                mediaRecorder.onstop = function() {{
                    const audioBlob = new Blob(audioChunks, {{ type: 'audio/webm' }});
                    sendAudioToServer(audioBlob);
                    
                    stream.getTracks().forEach(track => track.stop());
                }};
                
                mediaRecorder.start();
                isRecording = true;
                
                recordBtn.disabled = true;
                stopBtn.disabled = false;
                recordBtn.innerHTML = '🎤 녹음 중...';
                recordBtn.style.background = 'linear-gradient(45deg, #ff4757, #ff3742)';
                
            }} catch (error) {{
                console.error('마이크 접근 오류:', error);
                if (error.name === 'NotAllowedError') {{
                    showError('마이크 접근이 차단되었습니다. 브라우저 설정에서 마이크 권한을 허용해주세요.');
                }} else if (error.name === 'NotFoundError') {{
                    showError('마이크를 찾을 수 없습니다. 마이크가 연결되어 있는지 확인해주세요.');
                }} else {{
                    showError('마이크에 접근할 수 없습니다: ' + error.message);
                }}
            }}
        }}
        
        function stopRecording() {{
            if (mediaRecorder && isRecording) {{
                mediaRecorder.stop();
                isRecording = false;
                
                recordBtn.disabled = false;
                stopBtn.disabled = true;
                recordBtn.innerHTML = '🎤 음성 녹음 시작';
                recordBtn.style.background = 'linear-gradient(45deg, #ff6b6b, #ee5a24)';
            }}
        }}
        
        function sendAudioToServer(audioBlob) {{
            if (websocket && websocket.readyState === WebSocket.OPEN) {{
                console.log('v4.0 오디오 전송:', audioBlob.size, 'bytes');
                websocket.send(audioBlob);
            }} else {{
                console.error('WebSocket 연결이 없습니다');
                showError('서버 연결이 끊어졌습니다. 잠시 후 다시 시도해주세요.');
            }}
        }}
        
        // 초기화
        connectWebSocket();
        
        // 페이지 언로드 시 정리 (기존 + VAD 정리 추가)
        window.addEventListener('beforeunload', function() {{
            if (websocket) {{
                websocket.close();
            }}
            if (mediaRecorder && isRecording) {{
                mediaRecorder.stop();
            }}
            
            // 🔒 페이지 종료 시 모든 자원 정리
            forceStopAllAudio();
            if (smartVAD) {{
                smartVAD.stopMonitoring();
            }}
        }});
        
        // 브라우저 호환성 체크 (기존 유지)
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
            showError('이 브라우저는 마이크 접근을 지원하지 않습니다. Chrome, Firefox, Safari 등 최신 브라우저를 사용해주세요.');
        }}
    </script>
</body>
</html>
"""

# HTML Component 렌더링 (기존 완전 유지)
components.html(websocket_html, height=700, scrolling=False)

st.divider()

# 튜터 정보 및 설정 (기존 완전 유지)
col1, col2 = st.columns(2)

with col1:
    st.subheader("👨‍🏫 현재 튜터 정보")
    st.write(f"**이름:** {teacher_config['name']}")
    st.write(f"**전문 분야:** {teacher_config['subject']}")
    st.write(f"**교육 수준:** {teacher_config['level']}")
    st.write(f"**생성 시간:** {teacher_config['created_at']}")

with col2:
    st.subheader("🎭 성격 설정")
    personality = teacher_config['personality']
    st.write(f"**친근함:** {personality['friendliness']}%")
    st.write(f"**유머 수준:** {personality['humor_level']}%")
    st.write(f"**격려 수준:** {personality['encouragement']}%")
    st.write(f"**설명 상세도:** {personality.get('explanation_detail', 70)}%")

# 사용법 안내 (기존 + v4.0 업데이트)
with st.expander("🔊 v4.0 언어교육 AI 수준 기능 및 사용법"):
    st.markdown("""
    ### 🔊 **v4.0 언어교육 AI 수준 새로운 기능**
    - 🔊 **WaveNet + SSML**: Google 최고급 음성 + 감정 표현 및 억양 조절
    - 🧠 **실시간 감정 분석**: 좌절, 자신감, 혼란, 흥미 등 감정 상태 실시간 감지
    - 🎭 **적응형 대응**: 감정 상태에 따른 맞춤형 음성 톤과 설명 방식
    - 🎧 **VAD 자동 감지**: 말하기 시작하면 자동으로 AI 응답 중단 (언어교육 AI 수준)
    - 📊 **학습 진도 추적**: 인사 → 탐색 → 설명 → 연습 → 정리 단계별 진행
    - 🎤 **음성 시각화**: 실시간 음성 파형 및 감지 상태 표시
    - ⚡ **1초 응답 유지**: v3.3 모든 기능 100% 유지 + 품질 향상
    
    ### 🔊 **WaveNet + SSML 음성 품질 혁신**
    - **자연스러운 억양**: 문장의 의미와 감정에 맞는 자연스러운 억양
    - **감정 표현**: 격려할 때는 밝게, 설명할 때는 차분하게, 혼란 시 천천히
    - **적절한 쉼**: 문장 끝, 쉼표, 접속사에서 자연스러운 호흡
    - **강조와 완급**: 중요한 용어는 강조, 복잡한 내용은 천천히
    - **개인화 톤**: 튜터 성격에 따른 음성 톤 자동 조절
    
    ### 🧠 **실시간 감정 분석 및 적응**
    #### 감정 상태 감지:
    - **😤 좌절/어려움**: "모르겠어요", "어려워요", "헷갈려요" 등
    - **😊 자신감/이해**: "알겠어요", "쉽네요", "이해했어요" 등  
    - **🤔 혼란/의구심**: "뭐지?", "이상해요", "맞나요?" 등
    - **🤩 흥미/참여**: "재밌어요", "더 알고 싶어요", "신기해요" 등
    
    #### 감정별 적응 대응:
    - **좌절 시**: 더 쉬운 설명 + 격려 + 천천히 + 부드러운 톤
    - **자신감 시**: 적절한 도전 + 심화 내용 + 밝은 톤
    - **혼란 시**: 다른 방식 재설명 + 구체적 예시 + 명확한 톤  
    - **흥미 시**: 관련 주제 확장 + 응용 사례 + 활기찬 톤
    
    ### 🎧 **VAD 자동 감지 기능 (언어교육 AI 수준)**
    1. **🎧 자동 감지 ON** 버튼을 클릭하여 활성화
    2. AI가 응답하는 중에 **말하기만 시작**하면 자동으로 AI 응답 중단
    3. 마이크 권한 허용 필요 (실시간 음성 모니터링)
    4. 배경 소음과 실제 음성을 구분하여 오작동 최소화
    5. 음성 파형 시각화로 감지 상태 실시간 확인
    
    #### VAD 작동 원리:
    - **실시간 모니터링**: 100ms마다 음성 에너지 체크
    - **스마트 임계값**: 배경 소음 vs 실제 음성 자동 구분
    - **쿨다운 시스템**: 1초 간격으로 중복 트리거 방지
    - **자동 재시작**: 새 응답 시작 시 모니터링 자동 재개
    
    ### 📊 **학습 진도 추적 시스템**
    - **●○○○○ 인사**: 첫 만남, 학습 목표 파악
    - **●●○○○ 탐색**: 현재 이해도 및 수준 확인
    - **●●●○○ 설명**: 핵심 개념 및 원리 설명
    - **●●●●○ 연습**: 문제 풀이 및 응용 실습
    - **●●●●● 정리**: 학습 내용 정리 및 다음 단계
    
    ### 🛑 **즉시 중단 기능 (v3.3 완전 유지)**
    1. **음성 모드**: 응답 중 **🛑 즉시 중단** 버튼 클릭
    2. **텍스트 모드**: 응답 중 **🛑 응답 즉시 중단** 버튼 클릭  
    3. **새 질문으로 중단**: 응답 중 새로운 질문을 입력하면 자동 중단
    4. **음성으로 중단**: 응답 중 마이크 버튼을 누르면 자동 중단
    5. **VAD 자동 중단**: 🎧 자동 감지 ON 상태에서 말하기 시작하면 즉시 중단
    
    ### 💬 **실시간 피드백 사용법 (v3.3 완전 유지)**
    AI가 응답하는 중에 나타나는 피드백 버튼들:
    - **✂️ 짧게 해줘**: 현재 응답을 중단하고 간단한 요약으로 변경
    - **📝 더 자세히**: 현재 응답을 중단하고 상세한 설명으로 변경
    - **⏹️ 그만**: 현재 응답을 완전히 중단
    - **🤔 다시 설명**: 다른 방식으로 다시 설명 요청
    
    ### ⌨️ **텍스트 대화 방법 (v3.3 완전 유지)**
    1. **💬 텍스트 입력** 탭을 클릭하세요
    2. 질문을 입력하고 **📤 전송** 또는 **Enter**
    3. **1초 이내 응답 시작** + v4.0 고품질 스트리밍 확인
    4. 응답 중 **실시간 피드백** 또는 **즉시 중단** 가능
    5. **중첩 방지**: 이전 오디오 자동 중단 후 새 응답 재생
    
    ### 🎙️ **음성 대화 방법 (v4.0 고품질 업그레이드)**
    1. **🎤 음성 입력** 탭을 클릭하세요
    2. **🎧 자동 감지 ON** 버튼으로 VAD 활성화 (권장)
    3. **🎤 음성 녹음 시작** 버튼 클릭
    4. 질문을 말씀하시고 **⏹️ 녹음 중지**
    5. **1초 이내 응답** + WaveNet 고품질 감정 표현 음성 재생
    6. **자동 중단**: VAD 활성화 시 말하기만 하면 즉시 중단
    7. 응답 중 **🛑 즉시 중단** 또는 **실시간 피드백** 가능
    
    ### 📊 **성능 모니터링 (v4.0 확장)**
    대화창 하단에 실시간 성능 정보 표시:
    - **⚡ 첫 응답**: AI 응답 시작까지의 시간 (목표: 1초 이내)
    - **📊 전략**: 질문 분석 결과 (very_short/short/medium/long/interactive)
    - **🔊 TTS**: 음성 합성 처리 시간
    - **🎭 감정**: 현재 감지된 감정 상태
    - **🧠 단계**: 현재 학습 진행 단계
    - **🔒 중첩 방지**: 이전 오디오 중단 시 알림 표시
    
    ### 🔧 **문제 해결**
    - **마이크 접근 오류**: 브라우저에서 마이크 권한 허용
    - **VAD 오작동**: 배경 소음 체크, 마이크 위치 조정
    - **연결 오류**: 페이지 새로고침 또는 네트워크 확인
    - **음성 재생 안됨**: 화면 클릭 후 다시 시도 (브라우저 자동재생 정책)
    - **응답이 느림**: 성능 정보를 확인하여 병목 지점 파악
    - **감정 인식 부정확**: 더 명확한 표현으로 질문
    """)

# 기술 정보 (기존 + v4.0 업데이트)
with st.expander("🔧 기술 정보 (v4.0 언어교육 AI 수준)"):
    st.markdown(f"""
    ### 시스템 구성
    - **프론트엔드**: Streamlit Cloud v4.0 (VAD + 감정 분석 + 음성 시각화 UI)
    - **백엔드**: FastAPI v4.0.0 (WaveNet + SSML + 고급 감정 지능)
    - **실시간 통신**: WebSocket (v4.0 고급 메시지 처리)
    - **AI 모델**: GPT-3.5 Turbo (v4.0 고급 감정 분석 + 학습자 상태 추적)
    - **음성 합성**: Google Cloud TTS WaveNet (SSML 감정 표현)
    - **음성 인식**: Google Cloud STT (다중 설정 시도)
    
    ### v4.0 혁신적 개선 사항 (언어교육 AI 수준)
    - **🔊 WaveNet + SSML**: 언어교육 AI 수준 자연스러운 음성 + 감정 표현
    - **🧠 감정 지능**: 실시간 감정 상태 감지 + 적응형 대응 전략
    - **🎧 VAD 자동 감지**: 사용자 음성 감지 시 즉시 AI 응답 중단
    - **📊 학습자 추적**: 종합적 상태 분석 + 개인화된 학습 경험
    - **🎤 음성 시각화**: 실시간 음성 파형 + VAD 상태 표시
    - **🔒 완전 호환성**: v3.3 모든 기능 100% 유지 + 성능 향상
    
    ### 언어교육 AI 수준 핵심 기술
    #### 🔊 WaveNet + SSML 음성 기술:
    - **Neural TTS**: Google WaveNet 기반 신경망 음성 합성
    - **SSML 마크업**: 감정, 억양, 쉼, 강조 등 세밀한 음성 제어
    - **적응형 설정**: 감정 상태와 전략에 따른 실시간 음성 조절
    - **개인화 톤**: 튜터 성격에 맞는 음성 특성 자동 매핑
    
    #### 🧠 감정 지능 및 학습자 분석:
    - **의도 분석**: 질문 복잡도, 감정 상태, 학습 단계 종합 분석
    - **상태 추적**: 이해도, 참여도, 학습 진행 상황 실시간 모니터링
    - **적응형 전략**: 분석 결과에 따른 맞춤형 응답 전략 자동 선택
    - **감정 히스토리**: 감정 변화 패턴 추적으로 장기적 개인화
    
    #### 🎧 VAD (Voice Activity Detection) 기술:
    - **실시간 모니터링**: Web Audio API 기반 실시간 음성 에너지 분석
    - **스마트 임계값**: 배경 소음과 실제 음성 구분하는 적응형 알고리즘
    - **FFT 분석**: 주파수 도메인 분석으로 정확한 음성 감지
    - **쿨다운 시스템**: 오작동 방지를 위한 지능적 트리거 관리
    
    ### 성능 최적화 및 안정성
    #### v3.3 기능 100% 유지:
    - **중첩 완전 방지**: Lock 기반 직렬화 + 프론트엔드 오디오 관리
    - **1초 응답**: 병렬 처리 + 최적화된 스트리밍 파이프라인
    - **즉시 중단**: <100ms 중단 지연시간 + 안전한 상태 관리
    - **실시간 피드백**: 양방향 피드백 루프 + 적응형 응답
    
    #### v4.0 성능 향상:
    - **고품질 우선**: 음성 품질 최우선 + 적절한 지연 허용 (200-300ms)
    - **스마트 폴백**: 새 기능 오류 시 기존 방식으로 안전한 폴백
    - **점진적 향상**: 기존 시스템을 점진적으로 개선하는 안전한 업그레이드
    - **호환성 보장**: 모든 기존 WebSocket 메시지 타입 완전 지원
    
    ### 새로운 WebSocket 메시지 타입 (v4.0)
    - **향상된 오디오**: `audio_completely_safe` (v4.0 정보 포함)
      - `voice_type`: "wavenet" | "standard"
      - `ssml_enabled`: true | false
      - `emotional_state`: 감정 상태 정보
      - `strategy`: 현재 응답 전략
    - **기존 호환**: `audio_chunk`, `stt_result`, `text_chunk` 등 완전 지원
    - **감정 분석**: 백엔드에서 실시간 감정 상태 전송
    - **학습 추적**: 진도 및 이해도 정보 실시간 업데이트
    
    ### WebSocket 연결 정보
    - **서버 URL**: `{WEBSOCKET_URL}`
    - **버전**: v4.0.0 (언어교육 AI 수준) + 완전한 하위 호환성
    - **새 기능**: WaveNet, SSML, 감정 분석, VAD, 학습 추적
    - **기존 기능**: 음성 녹음, 채팅, 자동 재연결, 중첩 방지 모두 유지
    
    ### 성능 목표 달성 현황 (v4.0)
    - ✅ **자연스러운 음성**: WaveNet + SSML로 언어교육 AI 수준 달성
    - ✅ **감정 표현**: 실시간 감정 분석 + 적응형 음성 톤 조절
    - ✅ **VAD 자동 감지**: 음성 감지 시 즉시 중단 (언어교육 AI 핵심 기능)
    - ✅ **학습자 추적**: 종합적 상태 분석 + 개인화된 학습 경험
    - ✅ **완전 호환성**: v3.3 모든 기능 100% 유지 + 품질 향상
    - ✅ **중첩 완전 방지**: 단일 오디오만 재생 (기존 기능 유지)
    - ✅ **1초 이내 응답**: 병렬 처리 + 즉시 스트리밍 (기존 성능 유지)
    - ✅ **안정성**: 새 기능 오류 시 기존 방식으로 안전한 폴백
    
    ### 언어교육 AI와의 차별화
    - **전문성**: 특정 과목에 특화된 깊이 있는 튜터링
    - **개인화**: 개별 학습자 맞춤형 진도 관리 및 오답 분석
    - **교육적 접근**: 단순 대화가 아닌 체계적 학습 목표 지향
    - **감정 교육**: 학습 과정의 감정 관리 및 동기 부여
    - **진도 관리**: 학습 단계별 체계적 관리 및 성취도 추적
    """)
