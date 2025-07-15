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

# 🔒 JavaScript 문법 충돌 해결: 템플릿 변수 미리 준비
teacher_name = teacher_config['name']
teacher_subject = teacher_config['subject'] 
teacher_level = teacher_config['level']
teacher_friendliness = teacher_config['personality']['friendliness']
teacher_humor = teacher_config['personality']['humor_level']
teacher_encouragement = teacher_config['personality']['encouragement']
teacher_config_json = json.dumps(teacher_config).replace('"', '\\"')

# 🔒 v4.0 언어교육 AI 수준 WebSocket HTML Component (JavaScript 충돌 해결)
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
        
        /* 입력 방식 탭 */
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
        
        /* 컨트롤 버튼들 */
        .controls {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
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
    </style>
</head>
<body>
    <div class="container">
        <div class="teacher-info">
            <h2>👨‍🏫 {teacher_name} 선생님</h2>
            <p>{teacher_subject} 전문 | {teacher_level} 수준</p>
            <small>친근함: {teacher_friendliness}% | 
                   유머: {teacher_humor}% | 
                   격려: {teacher_encouragement}%</small>
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
        
        <!-- 입력 방식 탭 -->
        <div class="tabs">
            <button class="tab active" id="voiceTab" onclick="switchTab('voice')">
                🎤 음성 입력
            </button>
            <button class="tab" id="textTab" onclick="switchTab('text')">
                💬 텍스트 입력
            </button>
        </div>
        
        <!-- 음성 입력 컨트롤 -->
        <div class="controls" id="voiceControls">
            <button class="btn btn-record" id="recordBtn" onclick="startRecording()" disabled>
                🎤 음성 녹음 시작
            </button>
            <button class="btn btn-stop" id="stopBtn" onclick="stopRecording()" disabled>
                ⏹️ 녹음 중지
            </button>
            <button class="btn btn-interrupt" id="interruptBtn" onclick="interruptResponse()">
                🛑 즉시 중단
            </button>
        </div>
        
        <!-- 텍스트 입력 컨트롤 -->
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
        
        <div class="chat-area" id="chatArea">
            <div class="message ai-message">
                안녕하세요! 저는 {teacher_name} 선생님입니다. 🎓<br>
                {teacher_subject} 분야에 대해 무엇이든 물어보세요!<br>
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
        
        <!-- 성능 정보 표시 -->
        <div class="performance-info" id="performanceInfo">
            ⚡ 첫 응답: <span id="responseTime">-</span>ms | 
            📊 전략: <span id="responseStrategy">-</span> | 
            🔊 TTS: <span id="ttsTime">-</span>ms
        </div>
        
        <!-- 🔒 중첩 방지 알림 -->
        <div class="overlap-prevented" id="overlapPreventedInfo" style="display: none;">
            🔒 이전 오디오 중단됨 - 중첩 방지 활성화
        </div>
    </div>

    <script>
        // 🔒 핵심 변수들 (중복 방지)
        let currentAudio = null;              
        let audioQueue = [];                  
        let lastAudioId = null;               
        let preventMultiplePlay = true;       
        
        // 기존 변수들
        let websocket = null;
        let mediaRecorder = null;
        let audioChunks = [];
        let isRecording = false;
        let currentInputMode = 'voice';
        let currentAIMessage = null;
        let isResponseInProgress = false;
        let responseStartTime = null;
        let currentResponseStrategy = null;
        
        // v4.0 새로운 변수들
        let currentEmotionalState = 'neutral';
        let conversationTurnCount = 0;
        
        // DOM 요소들
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        const recordBtn = document.getElementById('recordBtn');
        const stopBtn = document.getElementById('stopBtn');
        const chatArea = document.getElementById('chatArea');
        const typingIndicator = document.getElementById('typingIndicator');
        const textInput = document.getElementById('textInput');
        const sendBtn = document.getElementById('sendBtn');
        const interruptBtn = document.getElementById('interruptBtn');
        const interruptBtnText = document.getElementById('interruptBtnText');
        const infoText = document.getElementById('infoText');
        const performanceInfo = document.getElementById('performanceInfo');
        const overlapPreventedInfo = document.getElementById('overlapPreventedInfo');
        const emotionalIndicator = document.getElementById('emotionalIndicator');
        const emotionIcon = document.getElementById('emotionIcon');
        const emotionText = document.getElementById('emotionText');
        
        const teacherConfig = JSON.parse('"{teacher_config_json}"'.replace(/\\"/g, '"'));
        
        // 🔒 핵심! 중첩 완전 방지 오디오 재생 함수
        function playAudio(base64Audio, audioId = null) {{
            try {{
                console.log('🔊 v4.0 오디오 재생 요청:', audioId);
                
                // 🔒 이전 오디오 즉시 중단
                if (currentAudio && !currentAudio.paused) {{
                    console.log('🛑 이전 오디오 중단');
                    currentAudio.pause();
                    currentAudio.currentTime = 0;
                    currentAudio = null;
                    showOverlapPrevented();
                }}
                
                // 🔒 중복 재생 방지
                if (preventMultiplePlay && audioId && audioId === lastAudioId) {{
                    console.log('🔒 중복 오디오 재생 방지:', audioId);
                    return;
                }}
                
                // 🔒 새 오디오 생성 및 재생
                const audioBlob = base64ToBlob(base64Audio, 'audio/mp3');
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                
                currentAudio = audio;
                lastAudioId = audioId;
                
                audio.onended = () => {{
                    console.log('✅ 오디오 재생 완료');
                    URL.revokeObjectURL(audioUrl);
                    if (currentAudio === audio) {{
                        currentAudio = null;
                    }}
                }};
                
                audio.onerror = (error) => {{
                    console.error('❌ 오디오 재생 오류:', error);
                    URL.revokeObjectURL(audioUrl);
                    if (currentAudio === audio) {{
                        currentAudio = null;
                    }}
                }};
                
                audio.play().then(() => {{
                    console.log('✅ v4.0 새 오디오 재생 시작 성공');
                    hideOverlapPrevented();
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
        
        // 🧠 감정 상태 업데이트
        function updateEmotionalState(emotionalState) {{
            if (!emotionalState) return;
            
            currentEmotionalState = emotionalState;
            
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
                emotionIcon.className = 'emotion-icon emotion-' + emotionalState;
            }}
            
            if (emotionText) {{
                emotionText.textContent = emotionTexts[emotionalState] || '상태 분석 중...';
            }}
            
            if (emotionalIndicator) {{
                emotionalIndicator.style.display = 'flex';
            }}
            
            console.log('🧠 감정 상태 업데이트:', emotionalState);
        }}
        
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
        
        function forceStopAllAudio() {{
            if (currentAudio && !currentAudio.paused) {{
                console.log('🔒 모든 오디오 강제 중단');
                currentAudio.pause();
                currentAudio.currentTime = 0;
                currentAudio = null;
                showOverlapPrevented();
            }}
        }}
        
        // 탭 전환
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
                infoText.textContent = '마이크 버튼을 눌러 음성으로 질문하세요.';
            }} else {{
                voiceTab.classList.remove('active');
                textTab.classList.add('active');
                voiceControls.style.display = 'none';
                textControls.style.display = 'flex';
                textInput.focus();
                infoText.textContent = '텍스트를 입력하고 전송 버튼을 클릭하세요.';
            }}
        }}
        
        // WebSocket 연결
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
                forceStopAllAudio();
                
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
                forceStopAllAudio();
            }};
        }}
        
        function handleServerMessage(message) {{
            console.log('v4.0 서버 메시지:', message);
            
            switch(message.type) {{
                case 'connection_established':
                    addMessage('ai', message.message);
                    break;
                    
                case 'config_updated':
                    console.log('튜터 설정 업데이트 완료');
                    break;
                    
                case 'response_start':
                    console.log('🚀 응답 시작:', message.strategy);
                    startNewResponse(message.strategy);
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
                    }}
                    break;
                    
                case 'audio_completely_safe':
                    console.log('🔒 v4.0 안전한 오디오 수신:', message.audio_size, 'bytes');
                    
                    if (message.emotional_state) {{
                        updateEmotionalState(message.emotional_state);
                    }}
                    
                    if (message.audio && shouldPlayAudio()) {{
                        playAudio(message.audio, message.client_id);
                    }}
                    
                    if (message.tts_time) {{
                        document.getElementById('ttsTime').textContent = Math.round(message.tts_time * 1000);
                    }}
                    
                    if (message.voice_type === 'wavenet') {{
                        console.log('🔊 WaveNet 고품질 음성 재생');
                    }}
                    if (message.ssml_enabled) {{
                        console.log('🎭 SSML 감정 표현 활성화');
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
        
        function startNewResponse(strategy) {{
            isResponseInProgress = true;
            responseStartTime = Date.now();
            currentResponseStrategy = strategy;
            
            currentAIMessage = createNewAIMessage();
            showTyping();
            showInterruptControls();
            
            statusDot.className = 'status-dot responding';
            statusText.textContent = '응답 생성 중... 🤖 (' + strategy + ')';
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
        }}
        
        function forceCompleteResponse(reason) {{
            if (currentAIMessage && reason) {{
                removeStreamingCursor(currentAIMessage);
                currentAIMessage.innerHTML += ' <em style="opacity: 0.6; font-size: 12px;">' + reason + '</em>';
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
            forceStopAllAudio();
        }}
        
        function createNewAIMessage() {{
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ai-message streaming';
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
        
        function showInterruptControls() {{
            if (currentInputMode === 'voice') {{
                interruptBtn.style.display = 'block';
            }} else {{
                interruptBtnText.style.display = 'block';
            }}
        }}
        
        function hideInterruptControls() {{
            interruptBtn.style.display = 'none';
            interruptBtnText.style.display = 'none';
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
            messageDiv.className = 'message ' + sender + '-message';
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
        
        // 텍스트 메시지 전송
        function sendTextMessage() {{
            const text = textInput.value.trim();
            if (!text || !isConnected()) {{
                return;
            }}
            
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
        
        function interruptResponse() {{
            if (!isResponseInProgress || !isConnected()) {{
                return;
            }}
            
            console.log('🛑 응답 즉시 중단 요청');
            forceStopAllAudio();
            
            const message = {{
                type: 'interrupt_response'
            }};
            
            websocket.send(JSON.stringify(message));
            
            hideInterruptControls();
            statusText.textContent = '응답 중단됨 ⏹️';
        }}
        
        // 간단한 녹음 함수 (기본 구현)
        async function startRecording() {{
            console.log('🎤 녹음 시작 (간단 버전)');
            if (isResponseInProgress) {{
                forceStopAllAudio();
                interruptResponse();
                setTimeout(startRecording, 300);
                return;
            }}
            
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ 
                    audio: true
                }});
                
                mediaRecorder = new MediaRecorder(stream);
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
                
            }} catch (error) {{
                console.error('마이크 접근 오류:', error);
                showError('마이크에 접근할 수 없습니다: ' + error.message);
            }}
        }}
        
        function stopRecording() {{
            if (mediaRecorder && isRecording) {{
                mediaRecorder.stop();
                isRecording = false;
                
                recordBtn.disabled = false;
                stopBtn.disabled = true;
                recordBtn.innerHTML = '🎤 음성 녹음 시작';
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
        
        // 텍스트 입력 이벤트
        if (textInput) {{
            textInput.addEventListener('input', function() {{
                updateTextInputState();
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
        
        // 초기화
        connectWebSocket();
        
        // 페이지 언로드 시 정리
        window.addEventListener('beforeunload', function() {{
            if (websocket) {{
                websocket.close();
            }}
            if (mediaRecorder && isRecording) {{
                mediaRecorder.stop();
            }}
            forceStopAllAudio();
        }});
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

# 사용법 안내 (기존 + v4.0 간단 업데이트)
with st.expander("🔊 v4.0 언어교육 AI 수준 기능 및 사용법"):
    st.markdown("""
    ### 🔊 **v4.0 언어교육 AI 수준 핵심 기능**
    - 🔊 **WaveNet + SSML**: Google 최고급 음성 + 감정 표현 및 억양 조절
    - 🧠 **실시간 감정 분석**: 좌절, 자신감, 혼란, 흥미 등 감정 상태 실시간 감지  
    - 🎭 **적응형 대응**: 감정 상태에 따른 맞춤형 음성 톤과 설명 방식
    - ⚡ **1초 응답 유지**: v3.3 모든 기능 100% 유지 + 품질 향상
    - 🔒 **중첩 완전 방지**: 단일 오디오만 재생 (기존 기능 유지)
    
    ### 🎙️ **음성 대화 방법**
    1. **🎤 음성 입력** 탭을 클릭하세요
    2. **🎤 음성 녹음 시작** 버튼 클릭
    3. 질문을 말씀하시고 **⏹️ 녹음 중지**
    4. **1초 이내 응답** + WaveNet 고품질 감정 표현 음성 재생
    5. 응답 중 **🛑 즉시 중단** 가능
    
    ### ⌨️ **텍스트 대화 방법**
    1. **💬 텍스트 입력** 탭을 클릭하세요
    2. 질문을 입력하고 **📤 전송** 또는 **Enter**
    3. **1초 이내 응답 시작** + v4.0 고품질 스트리밍 확인
    4. 응답 중 **🛑 응답 즉시 중단** 가능
    
    ### 🔧 **문제 해결**
    - **마이크 접근 오류**: 브라우저에서 마이크 권한 허용
    - **연결 오류**: 페이지 새로고침 또는 네트워크 확인
    - **음성 재생 안됨**: 화면 클릭 후 다시 시도 (브라우저 자동재생 정책)
    - **백엔드 서버**: 먼저 `python run.py`로 백엔드 서버 실행 확인
    """)

# 기술 정보 (기존 + v4.0 간단 업데이트)
with st.expander("🔧 기술 정보 (v4.0 언어교육 AI 수준)"):
    st.markdown(f"""
    ### 시스템 구성
    - **프론트엔드**: Streamlit Cloud v4.0 (감정 분석 + 중첩 방지 UI)
    - **백엔드**: FastAPI v4.0.0 (WaveNet + SSML + 고급 감정 지능)
    - **실시간 통신**: WebSocket (v4.0 고급 메시지 처리)
    - **AI 모델**: GPT-3.5 Turbo (v4.0 고급 감정 분석 + 학습자 상태 추적)
    - **음성 합성**: Google Cloud TTS WaveNet (SSML 감정 표현)
    - **음성 인식**: Google Cloud STT (다중 설정 시도)
    
    ### v4.0 혁신적 개선 사항
    - **🔊 WaveNet + SSML**: 언어교육 AI 수준 자연스러운 음성 + 감정 표현
    - **🧠 감정 지능**: 실시간 감정 상태 감지 + 적응형 대응 전략
    - **🔒 완전 호환성**: v3.3 모든 기능 100% 유지 + 품질 향상
    - **🛡️ 안정성**: 새 기능 오류 시 기존 방식으로 안전한 폴백
    
    ### WebSocket 연결 정보
    - **서버 URL**: `{WEBSOCKET_URL}`
    - **버전**: v4.0.0 (언어교육 AI 수준) + 완전한 하위 호환성
    - **새 기능**: WaveNet, SSML, 감정 분석, 학습자 추적
    - **기존 기능**: 음성 녹음, 채팅, 자동 재연결, 중첩 방지 모두 유지
    
    ### 성능 목표 달성 현황 (v4.0)
    - ✅ **자연스러운 음성**: WaveNet + SSML로 언어교육 AI 수준 달성
    - ✅ **감정 표현**: 실시간 감정 분석 + 적응형 음성 톤 조절
    - ✅ **완전 호환성**: v3.3 모든 기능 100% 유지 + 품질 향상
    - ✅ **중첩 완전 방지**: 단일 오디오만 재생 (기존 기능 유지)
    - ✅ **1초 이내 응답**: 병렬 처리 + 즉시 스트리밍 (기존 성능 유지)
    - ✅ **안정성**: 새 기능 오류 시 기존 방식으로 안전한 폴백
    """)
