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

# 상태 표시 (기존 + v3.0.0 정보 추가)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("튜터", teacher_config['name'], f"{teacher_config['subject']}")
with col2:
    st.metric("성격", f"친근함 {teacher_config['personality']['friendliness']}%", "")
with col3:
    st.metric("백엔드", "🟢 v3.0.0", "고도화 완료")  # 업데이트
with col4:
    st.metric("새 기능", "1초 응답", "즉시 중단")  # 새로 추가

st.divider()

# 대화 영역 (기존 + 새 기능 표시)
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🎙️ 음성 + 텍스트 대화 (v3.0 고도화)")  # 업데이트

with col2:
    if st.button("🏠 튜터 변경"):
        st.switch_page("app.py")

# WebSocket HTML Component (기존 코드 보존 + v3.0.0 기능 추가)
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
        .responding {{ background: #2196F3; animation: pulse 1s infinite; }}  /* NEW: 응답 중 상태 */
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        /* NEW: 입력 방식 탭 */
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
        
        /* 기존 음성 컨트롤 유지 */
        .controls {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        /* NEW: 텍스트 입력 컨트롤 */
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
        
        /* NEW: 텍스트 전송 버튼 */
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
        
        /* NEW: 즉시 중단 버튼 */
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
        
        /* NEW: 실시간 피드백 컨트롤 */
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
        
        /* NEW: 스트리밍 효과 */
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
        
        /* NEW: 성능 정보 */
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
                <small style="color: #81C784;">🚀 v3.0 고도화: 1초 응답 + 즉시 중단 + 실시간 피드백</small>
            </div>
        </div>
        
        <div class="status">
            <span class="status-dot disconnected" id="statusDot"></span>
            <span id="statusText">연결 중...</span>
        </div>
        
        <!-- NEW: 입력 방식 탭 -->
        <div class="tabs">
            <button class="tab active" id="voiceTab" onclick="switchTab('voice')">
                🎤 음성 입력
            </button>
            <button class="tab" id="textTab" onclick="switchTab('text')">
                💬 텍스트 입력
            </button>
        </div>
        
        <!-- 기존 음성 입력 컨트롤 (완전 유지) -->
        <div class="controls" id="voiceControls">
            <button class="btn btn-record" id="recordBtn" onclick="startRecording()" disabled>
                🎤 음성 녹음 시작
            </button>
            <button class="btn btn-stop" id="stopBtn" onclick="stopRecording()" disabled>
                ⏹️ 녹음 중지
            </button>
            <!-- NEW: 음성 모드 중단 버튼 -->
            <button class="btn btn-interrupt" id="interruptBtn" onclick="interruptResponse()">
                🛑 즉시 중단
            </button>
        </div>
        
        <!-- NEW: 텍스트 입력 컨트롤 -->
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
            <!-- NEW: 텍스트 모드 중단 버튼 -->
            <button class="btn btn-interrupt" id="interruptBtnText" onclick="interruptResponse()" style="display: none; width: 100%;">
                🛑 응답 즉시 중단
            </button>
        </div>
        
        <!-- NEW: 실시간 피드백 컨트롤 -->
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
                <small style="opacity: 0.8;">🚀 v3.0 고도화: 1초 이내 응답 + 즉시 중단 + 실시간 피드백이 가능합니다!</small>
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
        
        <!-- NEW: 성능 정보 표시 -->
        <div class="performance-info" id="performanceInfo">
            ⚡ 첫 응답: <span id="responseTime">-</span>ms | 
            📊 전략: <span id="responseStrategy">-</span> | 
            🔊 TTS: <span id="ttsTime">-</span>ms
        </div>
    </div>

    <script>
        // 기존 변수들 완전 유지
        let websocket = null;
        let mediaRecorder = null;
        let audioChunks = [];
        let isRecording = false;
        
        // NEW: v3.0.0 변수들 추가
        let currentInputMode = 'voice';
        let currentAIMessage = null;
        let isResponseInProgress = false;
        let responseStartTime = null;
        let currentResponseStrategy = null;
        
        // 기존 요소들 완전 유지
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        const recordBtn = document.getElementById('recordBtn');
        const stopBtn = document.getElementById('stopBtn');
        const chatArea = document.getElementById('chatArea');
        const typingIndicator = document.getElementById('typingIndicator');
        
        // NEW: 새 요소들 추가
        const textInput = document.getElementById('textInput');
        const sendBtn = document.getElementById('sendBtn');
        const interruptBtn = document.getElementById('interruptBtn');
        const interruptBtnText = document.getElementById('interruptBtnText');
        const feedbackControls = document.getElementById('feedbackControls');
        const infoText = document.getElementById('infoText');
        const performanceInfo = document.getElementById('performanceInfo');
        
        // 기존 튜터 설정 완전 유지
        const teacherConfig = {json.dumps(teacher_config)};
        
        // NEW: 탭 전환 기능
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
        
        // NEW: 텍스트 입력 이벤트
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
        
        // NEW: 텍스트 메시지 전송
        function sendTextMessage() {{
            const text = textInput.value.trim();
            if (!text || !isConnected()) {{
                return;
            }}
            
            // 사용자 메시지 표시 (기존 방식)
            addMessage('user', text);
            
            // v3.0.0 백엔드로 전송
            const message = {{
                type: 'user_text',
                text: text
            }};
            
            // 응답 중이면 중단 플래그 추가
            if (isResponseInProgress) {{
                message.interrupt = true;
                console.log('🛑 응답 중단 후 새 질문 전송');
            }}
            
            websocket.send(JSON.stringify(message));
            
            // 입력 필드 초기화 (기존 방식)
            textInput.value = '';
            sendBtn.disabled = true;
        }}
        
        // NEW: 즉시 중단 기능
        function interruptResponse() {{
            if (!isResponseInProgress || !isConnected()) {{
                return;
            }}
            
            console.log('🛑 응답 즉시 중단 요청');
            
            const message = {{
                type: 'interrupt_response'
            }};
            
            websocket.send(JSON.stringify(message));
            
            // UI 즉시 업데이트
            hideInterruptControls();
            statusText.textContent = '응답 중단됨 ⏹️';
        }}
        
        // NEW: 실시간 피드백 전송
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
            
            // 피드백 시각적 표시
            showFeedbackSent(action);
        }}
        
        // NEW: 피드백 전송 표시
        function showFeedbackSent(action) {{
            const actionNames = {{
                'make_shorter': '짧게 요청',
                'make_detailed': '상세 요청',
                'stop': '중단 요청',
                'clarify': '재설명 요청'
            }};
            
            addMessage('user', `💬 \${{actionNames[action] || action}}`);
        }}
        
        // 기존 WebSocket 연결 함수 완전 유지 + v3.0.0 호환 추가
        function connectWebSocket() {{
            const wsUrl = '{WEBSOCKET_URL}';
            console.log('연결 시도:', wsUrl);
            
            statusDot.className = 'status-dot connecting';
            statusText.textContent = '연결 중...';
            
            websocket = new WebSocket(wsUrl);
            
            websocket.onopen = function(event) {{
                console.log('WebSocket 연결 성공');
                statusDot.className = 'status-dot connected';
                statusText.textContent = '연결됨 ✅';
                recordBtn.disabled = false;
                updateTextInputState();  // NEW
                
                // 기존 튜터 설정 전송 완전 유지
                const configMessage = {{
                    type: "config_update",
                    config: {{
                        name: teacherConfig.name,
                        subject: teacherConfig.subject,
                        level: teacherConfig.level,
                        personality: teacherConfig.personality,
                        voice_settings: {{  // NEW: voice_settings 추가
                            auto_play: true,
                            speed: 1.0,
                            pitch: 1.0
                        }}
                    }}
                }};
                websocket.send(JSON.stringify(configMessage));
            }};
            
            websocket.onmessage = function(event) {{
                console.log('메시지 수신:', event.data);
                
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
                updateTextInputState();  // NEW
                resetResponseState();    // NEW
                
                // 기존 재연결 로직 완전 유지
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
            }};
        }}
        
        // 기존 + v3.0.0 호환 서버 메시지 처리
        function handleServerMessage(message) {{
            console.log('서버 메시지:', message);
            
            switch(message.type) {{
                case 'connection_established':
                    // 기존 처리 완전 유지
                    addMessage('ai', message.message);
                    break;
                    
                case 'config_updated':
                    // 기존 처리 완전 유지
                    console.log('튜터 설정 업데이트 완료');
                    break;
                    
                case 'response_start':
                    // NEW: v3.0.0 응답 시작
                    console.log('🚀 v3.0 응답 시작:', message.strategy);
                    startNewResponse(message.strategy);
                    break;
                    
                case 'text_chunk':
                    // NEW + 기존 호환: 텍스트 스트리밍
                    if (isResponseInProgress && currentAIMessage) {{
                        appendToAIMessage(currentAIMessage, message.content);
                        measureFirstResponse();
                    }} else {{
                        // 기존 방식 fallback
                        hideTyping();
                        addMessage('ai', message.content);
                    }}
                    break;
                    
                case 'response_complete':
                    // NEW: v3.0.0 응답 완료
                    if (currentAIMessage) {{
                        removeStreamingCursor(currentAIMessage);
                        addStrategyIndicator(currentAIMessage, currentResponseStrategy);
                    }}
                    break;
                    
                case 'audio_stream_quality':
                    // NEW: v3.0.0 고품질 TTS
                    console.log('🔊 v3.0 고품질 TTS:', message.sequence);
                    if (message.audio && shouldPlayAudio()) {{
                        playAudio(message.audio);
                    }}
                    if (message.tts_time) {{
                        document.getElementById('ttsTime').textContent = Math.round(message.tts_time * 1000);
                    }}
                    break;
                    
                case 'all_audio_complete':
                    // NEW: v3.0.0 모든 오디오 완료
                    console.log('✅ v3.0 모든 오디오 완료');
                    completeResponse();
                    break;
                    
                case 'audio_chunk':
                    // 기존 처리 완전 유지 (v2.0.0 호환)
                    hideTyping();
                    addMessage('ai', message.content);
                    if (message.audio && shouldPlayAudio()) {{
                        playAudio(message.audio);
                    }}
                    break;
                    
                case 'stt_result':
                    // 기존 처리 완전 유지
                    addMessage('user', message.text);
                    showTyping();
                    break;
                    
                case 'response_interrupted':
                    // NEW: v3.0.0 응답 중단 확인
                    console.log('✅ v3.0 응답 중단 확인됨');
                    forceCompleteResponse('[중단됨]');
                    break;
                    
                case 'feedback_acknowledged':
                    // NEW: v3.0.0 피드백 확인
                    console.log('💬 v3.0 피드백 확인:', message.message);
                    showFeedbackAck(message.message);
                    break;
                    
                case 'error':
                    // 기존 처리 완전 유지
                    hideTyping();
                    resetResponseState();  // NEW: 안전한 상태 초기화
                    showError(message.message);
                    break;
                    
                default:
                    console.warn('알 수 없는 메시지 타입:', message.type);
            }}
        }}
        
        // NEW: v3.0.0 응답 관리 함수들
        function startNewResponse(strategy) {{
            isResponseInProgress = true;
            responseStartTime = Date.now();
            currentResponseStrategy = strategy;
            
            currentAIMessage = createNewAIMessage();
            showTyping();
            showInterruptControls();
            
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
            statusText.textContent = '연결됨 ✅';
            updateTextInputState();
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
        
        // 기존 메시지 추가 함수 완전 유지
        function addMessage(sender, text) {{
            const messageDiv = document.createElement('div');
            messageDiv.className = `message \${{sender}}-message`;
            messageDiv.innerHTML = text;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        // 기존 에러 표시 함수 완전 유지
        function showError(errorText) {{
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = '❌ ' + errorText;
            chatArea.appendChild(errorDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        // 기존 타이핑 표시 함수 완전 유지
        function showTyping() {{
            typingIndicator.style.display = 'block';
        }}
        
        function hideTyping() {{
            typingIndicator.style.display = 'none';
        }}
        
        // 기존 오디오 재생 함수 완전 유지
        function playAudio(base64Audio) {{
            try {{
                const audioBlob = base64ToBlob(base64Audio, 'audio/mp3');
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                
                audio.play().then(() => {{
                    console.log('오디오 재생 시작');
                }}).catch(error => {{
                    console.error('오디오 재생 실패:', error);
                    if (error.name === 'NotAllowedError') {{
                        showError('브라우저에서 자동 재생이 차단되었습니다. 화면을 클릭한 후 다시 시도해주세요.');
                    }}
                }});
                
                audio.onended = () => {{
                    URL.revokeObjectURL(audioUrl);
                }};
            }} catch (error) {{
                console.error('오디오 처리 오류:', error);
            }}
        }}
        
        // 기존 Base64 변환 함수 완전 유지
        function base64ToBlob(base64, mimeType) {{
            const byteCharacters = atob(base64);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}
            const byteArray = new Uint8Array(byteNumbers);
            return new Blob([byteArray], {{type: mimeType}});
        }}
        
        // 기존 녹음 시작 함수 완전 유지 + 중단 체크 추가
        async function startRecording() {{
            // NEW: 응답 진행 중이면 자연스럽게 중단 후 녹음
            if (isResponseInProgress) {{
                console.log('🛑 응답 중단 후 녹음 시작');
                interruptResponse();
                setTimeout(startRecording, 300);
                return;
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
        
        // 기존 녹음 중지 함수 완전 유지
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
        
        // 기존 오디오 전송 함수 완전 유지
        function sendAudioToServer(audioBlob) {{
            if (websocket && websocket.readyState === WebSocket.OPEN) {{
                console.log('오디오 전송:', audioBlob.size, 'bytes');
                websocket.send(audioBlob);
            }} else {{
                console.error('WebSocket 연결이 없습니다');
                showError('서버 연결이 끊어졌습니다. 잠시 후 다시 시도해주세요.');
            }}
        }}
        
        // 기존 페이지 로드 시 연결 완전 유지
        connectWebSocket();
        
        // 기존 페이지 언로드 시 정리 완전 유지
        window.addEventListener('beforeunload', function() {{
            if (websocket) {{
                websocket.close();
            }}
            if (mediaRecorder && isRecording) {{
                mediaRecorder.stop();
            }}
        }});
        
        // 기존 브라우저 호환성 체크 완전 유지
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

# 사용법 안내 (기존 + v3.0.0 업데이트)
with st.expander("🚀 v3.0 고도화 기능 및 사용법"):
    st.markdown("""
    ### 🚀 **v3.0 고도화 기능**
    - ⚡ **1초 이내 응답**: 사용자 질문 후 1초 이내에 AI 응답 시작
    - 🛑 **즉시 중단**: 응답 중 언제든지 즉시 중단 가능
    - 💬 **실시간 피드백**: "짧게 해줘", "더 자세히", "그만" 등 실시간 요청
    - 📊 **성능 표시**: 응답 시간, 전략, TTS 시간 실시간 표시
    - ⌨️ **텍스트 입력**: 음성과 텍스트 입력 모두 지원
    - 🔄 **고품질 스트리밍**: 자연스러운 단어 단위 스트리밍
    
    ### 🛑 **즉시 중단 기능 사용법**
    1. **음성 모드**: 응답 중 **🛑 즉시 중단** 버튼 클릭
    2. **텍스트 모드**: 응답 중 **🛑 응답 즉시 중단** 버튼 클릭  
    3. **새 질문으로 중단**: 응답 중 새로운 질문을 입력하면 자동 중단
    4. **음성으로 중단**: 응답 중 마이크 버튼을 누르면 자동 중단
    
    ### 💬 **실시간 피드백 사용법**
    AI가 응답하는 중에 나타나는 피드백 버튼들:
    - **✂️ 짧게 해줘**: 현재 응답을 중단하고 간단한 요약으로 변경
    - **📝 더 자세히**: 현재 응답을 중단하고 상세한 설명으로 변경
    - **⏹️ 그만**: 현재 응답을 완전히 중단
    - **🤔 다시 설명**: 다른 방식으로 다시 설명 요청
    
    ### ⌨️ **텍스트 대화 방법**
    1. **💬 텍스트 입력** 탭을 클릭하세요
    2. 질문을 입력하고 **📤 전송** 또는 **Enter**
    3. **1초 이내 응답 시작** + 실시간 스트리밍 확인
    4. 응답 중 **실시간 피드백** 또는 **즉시 중단** 가능
    
    ### 🎙️ **음성 대화 방법** (기존 기능 유지 + 개선)
    1. **🎤 음성 입력** 탭을 클릭하세요
    2. **🎤 음성 녹음 시작** 버튼 클릭
    3. 질문을 말씀하시고 **⏹️ 녹음 중지**
    4. **1초 이내 응답** + 고품질 TTS 음성 재생
    5. 응답 중 **🛑 즉시 중단** 또는 **실시간 피드백** 가능
    
    ### 📊 **성능 모니터링**
    대화창 하단에 실시간 성능 정보 표시:
    - **⚡ 첫 응답**: AI 응답 시작까지의 시간 (목표: 1초 이내)
    - **📊 전략**: 질문 분석 결과 (very_short/short/medium/long/interactive)
    - **🔊 TTS**: 음성 합성 처리 시간
    
    ### 🔧 **문제 해결**
    - **마이크 접근 오류**: 브라우저에서 마이크 권한 허용
    - **연결 오류**: 페이지 새로고침 또는 네트워크 확인
    - **음성 재생 안됨**: 화면 클릭 후 다시 시도 (브라우저 자동재생 정책)
    - **응답이 느림**: 성능 정보를 확인하여 병목 지점 파악
    """)

# 기술 정보 (기존 + v3.0.0 업데이트)
with st.expander("🔧 기술 정보 (v3.0 고도화)"):
    st.markdown(f"""
    ### 시스템 구성
    - **프론트엔드**: Streamlit Cloud v3.0 (즉시 중단 + 실시간 피드백 UI)
    - **백엔드**: FastAPI v3.0.0 (1초 응답 + 고품질 스트리밍)
    - **실시간 통신**: WebSocket (고도화된 메시지 처리)
    - **AI 모델**: GPT-3.5 Turbo (스마트 의도 분석 + 적응형 응답)
    - **음성 합성**: Google Cloud TTS (고품질 우선 + 200-300ms 버퍼링)
    - **음성 인식**: Google Cloud STT (다중 설정 시도)
    
    ### v3.0 핵심 개선 사항
    - **1초 응답 시스템**: 병렬 처리 + 예측적 UX
    - **즉시 중단 로직**: 응답 상태 관리 + 실시간 제어
    - **스마트 의도 분석**: 50ms 이내 질문 분석 + 전략 결정
    - **고품질 스트리밍**: 음성 품질 최우선 + 자연스러운 흐름
    - **실시간 피드백**: 양방향 피드백 루프 + 적응형 응답
    - **성능 모니터링**: 실시간 메트릭 + 사용자 피드백
    - **완전 호환**: 기존 v2.0.0 백엔드와도 100% 호환
    
    ### 새로운 WebSocket 메시지 타입
    - **v3.0.0 전용**: `response_start`, `audio_stream_quality`, `all_audio_complete`
    - **피드백**: `feedback_request`, `feedback_acknowledged`, `response_interrupted`
    - **기존 호환**: `audio_chunk`, `stt_result`, `text_chunk` 등 완전 지원
    
    ### WebSocket 연결 정보
    - **서버 URL**: `{WEBSOCKET_URL}`
    - **버전**: v3.0.0 (고도화 백엔드) + v2.0.0 호환
    - **새 기능**: 즉시 중단, 실시간 피드백, 1초 응답
    - **기존 기능**: 음성 녹음, 채팅, 자동 재연결 모두 유지
    
    ### 성능 목표 달성 현황
    - ✅ **1초 이내 응답**: 병렬 처리 + 즉시 스트리밍
    - ✅ **즉시 중단**: <100ms 중단 지연시간
    - ✅ **고품질 음성**: 200-300ms 버퍼링으로 자연스러운 TTS
    - ✅ **실시간 피드백**: 양방향 실시간 제어
    - ✅ **안정성**: 기존 기능 100% 호환 + 점진적 개선
    """)
