import streamlit as st
import streamlit.components.v1 as components
import json

# 페이지 설정
st.set_page_config(
    page_title="AI 튜터 실시간 음성 대화",
    page_icon="🎓",
    layout="wide"
)

# 튜터 설정 확인
if 'selected_teacher' not in st.session_state:
    st.error("⚠️ 튜터 설정이 없습니다. 먼저 AI 튜터를 생성해주세요.")
    if st.button("🏠 AI 튜터 팩토리로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

teacher_config = st.session_state.selected_teacher

# 헤더
st.title(f"🎓 {teacher_config['name']} 선생님과의 실시간 대화")
st.markdown(f"**전문 분야:** {teacher_config['subject']} | **수준:** {teacher_config['level']}")

# 서버 URL 설정
WEBSOCKET_URL = "wss://ai-teacher-611312919059.asia-northeast3.run.app/ws/tutor/user1"

# 상태 표시
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("튜터", teacher_config['name'], f"{teacher_config['subject']}")
with col2:
    st.metric("성격", f"친근함 {teacher_config['personality']['friendliness']}%", "")
with col3:
    st.metric("백엔드", "🟢 정상", "Cloud Run")
with col4:
    st.metric("AI 모델", "GPT-3.5", "비용 최적화")

st.divider()

# 대화 영역
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("💬 음성 + 텍스트 대화")

with col2:
    if st.button("🏠 튜터 변경"):
        st.switch_page("app.py")

# WebSocket HTML Component (텍스트 입력 기능 추가)
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
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        /* 탭 스타일 */
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
        
        /* 입력 방식별 컨트롤 */
        .input-controls {{
            margin-bottom: 30px;
        }}
        
        .voice-controls {{
            display: flex;
            justify-content: center;
            gap: 20px;
        }}
        
        .text-controls {{
            display: none;
            flex-direction: column;
            gap: 15px;
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
            justify-content: center;
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
        </div>
        
        <div class="status">
            <span class="status-dot disconnected" id="statusDot"></span>
            <span id="statusText">연결 중...</span>
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
        
        <!-- 입력 컨트롤들 -->
        <div class="input-controls">
            <!-- 음성 입력 컨트롤 -->
            <div class="voice-controls" id="voiceControls">
                <button class="btn btn-record" id="recordBtn" onclick="startRecording()" disabled>
                    🎤 음성 녹음 시작
                </button>
                <button class="btn btn-stop" id="stopBtn" onclick="stopRecording()" disabled>
                    ⏹️ 녹음 중지
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
            </div>
        </div>
        
        <div class="chat-area" id="chatArea">
            <div class="message ai-message">
                안녕하세요! 저는 {teacher_config['name']} 선생님입니다. 🎓<br>
                {teacher_config['subject']} 분야에 대해 무엇이든 물어보세요!<br>
                <small style="opacity: 0.8;">💡 음성 또는 텍스트로 질문할 수 있습니다.</small>
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
    </div>

    <script>
        let websocket = null;
        let mediaRecorder = null;
        let audioChunks = [];
        let isRecording = false;
        let currentInputMode = 'voice';
        
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        const recordBtn = document.getElementById('recordBtn');
        const stopBtn = document.getElementById('stopBtn');
        const textInput = document.getElementById('textInput');
        const sendBtn = document.getElementById('sendBtn');
        const chatArea = document.getElementById('chatArea');
        const typingIndicator = document.getElementById('typingIndicator');
        const infoText = document.getElementById('infoText');
        
        // 튜터 설정
        const teacherConfig = {json.dumps(teacher_config)};
        
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
        
        // 텍스트 입력 이벤트
        textInput.addEventListener('input', function() {{
            const text = textInput.value.trim();
            sendBtn.disabled = !text || !websocket || websocket.readyState !== WebSocket.OPEN;
        }});
        
        // Enter 키 이벤트 (Shift+Enter는 줄바꿈, Enter는 전송)
        textInput.addEventListener('keydown', function(event) {{
            if (event.key === 'Enter' && !event.shiftKey) {{
                event.preventDefault();
                if (!sendBtn.disabled) {{
                    sendTextMessage();
                }}
            }}
        }});
        
        // 텍스트 메시지 전송
        function sendTextMessage() {{
            const text = textInput.value.trim();
            if (!text || !websocket || websocket.readyState !== WebSocket.OPEN) {{
                return;
            }}
            
            // 사용자 메시지 표시
            addMessage('user', text);
            
            // 서버로 전송
            const message = {{
                type: 'user_text',
                text: text
            }};
            
            websocket.send(JSON.stringify(message));
            
            // 입력 필드 초기화
            textInput.value = '';
            sendBtn.disabled = true;
            
            // 타이핑 표시
            showTyping();
        }}
        
        // WebSocket 연결
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
                
                // 텍스트 입력 활성화
                const text = textInput.value.trim();
                sendBtn.disabled = !text;
                
                // 튜터 설정 전송
                const configMessage = {{
                    type: "config_update",
                    config: {{
                        name: teacherConfig.name,
                        subject: teacherConfig.subject,
                        level: teacherConfig.level,
                        personality: teacherConfig.personality
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
                sendBtn.disabled = true;
                
                // 5초 후 재연결 시도
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
        
        // 서버 메시지 처리
        function handleServerMessage(message) {{
            console.log('서버 메시지:', message);
            
            switch(message.type) {{
                case 'connection_established':
                    // 연결 메시지는 이미 화면에 표시되어 있으므로 업데이트하지 않음
                    break;
                    
                case 'config_updated':
                    console.log('튜터 설정 업데이트 완료');
                    break;
                    
                case 'stt_result':
                    addMessage('user', message.text);
                    showTyping();
                    break;
                    
                case 'audio_chunk':
                    hideTyping();
                    addMessage('ai', message.content);
                    if (message.audio && teacherConfig.voice_settings && teacherConfig.voice_settings.auto_play) {{
                        playAudio(message.audio);
                    }}
                    break;
                    
                case 'text_chunk':
                    hideTyping();
                    addMessage('ai', message.content);
                    break;
                    
                case 'error':
                    hideTyping();
                    showError(message.message);
                    break;
            }}
        }}
        
        // 메시지 추가
        function addMessage(sender, text) {{
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{sender}}-message`;
            messageDiv.innerHTML = text;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        // 에러 표시
        function showError(errorText) {{
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = '❌ ' + errorText;
            chatArea.appendChild(errorDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        // 타이핑 표시
        function showTyping() {{
            typingIndicator.style.display = 'block';
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        function hideTyping() {{
            typingIndicator.style.display = 'none';
        }}
        
        // 오디오 재생
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
        
        // Base64를 Blob으로 변환
        function base64ToBlob(base64, mimeType) {{
            const byteCharacters = atob(base64);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}
            const byteArray = new Uint8Array(byteNumbers);
            return new Blob([byteArray], {{type: mimeType}});
        }}
        
        // 녹음 시작
        async function startRecording() {{
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
        
        // 녹음 중지
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
        
        // 오디오를 서버로 전송
        function sendAudioToServer(audioBlob) {{
            if (websocket && websocket.readyState === WebSocket.OPEN) {{
                console.log('오디오 전송:', audioBlob.size, 'bytes');
                websocket.send(audioBlob);
            }} else {{
                console.error('WebSocket 연결이 없습니다');
                showError('서버 연결이 끊어졌습니다. 잠시 후 다시 시도해주세요.');
            }}
        }}
        
        // 페이지 로드 시 WebSocket 연결
        connectWebSocket();
        
        // 페이지 언로드 시 연결 정리
        window.addEventListener('beforeunload', function() {{
            if (websocket) {{
                websocket.close();
            }}
            if (mediaRecorder && isRecording) {{
                mediaRecorder.stop();
            }}
        }});
        
        // 브라우저 호환성 체크
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
            showError('이 브라우저는 마이크 접근을 지원하지 않습니다. Chrome, Firefox, Safari 등 최신 브라우저를 사용해주세요.');
        }}
    </script>
</body>
</html>
"""

# HTML Component 렌더링
components.html(websocket_html, height=700, scrolling=False)

st.divider()

# 튜터 정보 및 설정
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

# 사용법 안내 (업데이트)
with st.expander("📖 사용법 안내"):
    st.markdown("""
    ### 💬 텍스트 대화 방법
    1. **💬 텍스트 입력** 탭을 클릭하세요
    2. **텍스트 입력 필드**에 질문을 입력하세요
    3. **📤 전송** 버튼을 클릭하거나 **Enter 키**를 누르세요
    4. **AI 튜터의 답변**을 텍스트와 음성으로 받을 수 있습니다
    
    ### 🎙️ 음성 대화 방법
    1. **🎤 음성 입력** 탭을 클릭하세요
    2. **🎤 음성 녹음 시작** 버튼을 클릭하세요
    3. **마이크 권한을 허용**해주세요 (브라우저에서 요청 시)
    4. **질문을 말씀해주세요** (예: "미적분학에 대해 설명해주세요")
    5. **⏹️ 녹음 중지** 버튼을 클릭하세요
    6. **AI 튜터의 답변**을 텍스트와 음성으로 들으실 수 있습니다
    
    ### 💡 팁
    - **텍스트 입력**: 빠르고 정확한 질문, 긴 내용 입력에 적합
    - **음성 입력**: 자연스러운 대화, 발음 연습에 적합
    - **Shift + Enter**: 텍스트 입력에서 줄바꿈
    - **Enter**: 텍스트 전송
    
    ### 🔧 문제 해결
    - **마이크 접근 오류**: 브라우저 설정에서 마이크 권한을 허용해주세요
    - **연결 오류**: 페이지를 새로고침하거나 네트워크 상태를 확인해주세요
    - **음성 재생 안됨**: 브라우저에서 자동 재생이 차단된 경우, 화면을 클릭한 후 다시 시도해주세요
    """)

# 기술 정보
with st.expander("🔧 기술 정보"):
    st.markdown(f"""
    ### 시스템 구성
    - **프론트엔드**: Streamlit Cloud
    - **백엔드**: FastAPI (Google Cloud Run)
    - **실시간 통신**: WebSocket
    - **AI 모델**: GPT-3.5 Turbo Streaming
    - **음성 합성**: Google Cloud TTS Standard
    - **입력 방식**: 음성(STT) + 텍스트 동시 지원
    
    ### WebSocket 연결 정보
    - **서버 URL**: `{WEBSOCKET_URL}`
    - **연결 상태**: 실시간 표시
    - **자동 재연결**: 5초 후 재시도
    - **지원 메시지**: 음성(바이너리), 텍스트(JSON)
    """)
