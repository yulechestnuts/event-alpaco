import streamlit as st
import pandas as pd
import json
from streamlit.components.v1 import html

st.set_page_config(page_title="[하나은행] Digital Hana 路 데이터분석/서비스기획 4기 - 크리스마스 이벤트", layout="wide")

def example_excel():
    example_data = pd.DataFrame({"이름": ["홍길동", "김철수", "이영희"]})
    example_data.to_excel("example.xlsx", index=False)
    with open("example.xlsx", "rb") as file:
        st.download_button(
            label="예시 파일 다운로드",
            data=file,
            file_name="example.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# 입력 방식 선택
input_method = st.radio("참가자 입력 방식을 선택하세요:", 
                       ["직접 입력", "Excel 파일 업로드"],
                       horizontal=True)

if input_method == "직접 입력":
    participant_count = st.number_input("참가자 수를 입력하세요:", min_value=1, value=3)
    
    # 입력 필드들을 담을 컨테이너 생성
    participants = []
    for i in range(participant_count):
        name = st.text_input(f"참가자 {i+1} 이름:", key=f"participant_{i}")
        if name.strip():  # 빈 문자열이 아닌 경우만 추가
            participants.append(name)
    
    names_js_array = json.dumps(participants)
else:
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Excel 파일을 선택하세요", type=["xlsx"])
    with col2:
        example_excel()

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            if "이름" not in df.columns:
                st.error("Excel 파일에 '이름' 열이 없습니다. 예시 파일을 참고해주세요.")
                names_js_array = "[]"
            else:
                df = df[df['이름'].notna()]
                df = df[df['이름'].astype(str).str.strip() != '']
                df = df[~df['이름'].astype(str).str.match(r'^\d+$')]
                names = df["이름"].tolist()
                names_js_array = json.dumps(names)
        except Exception as e:
            st.error("파일 업로드에 실패했습니다. 올바른 Excel 파일을 선택해주세요.")
            st.write(e)
            names_js_array = "[]"
    else:
        names_js_array = "[]"

html_code = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[하나은행] Digital Hana 路 데이터분석/서비스기획 4기 <br> 크리스마스 이벤트</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Noto Sans KR', sans-serif;
        }}

        body {{
            background-color: #f5f5f7;
            color: #1d1d1f;
        }}

        .container {{
            max-width: 980px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }}

        .title {{
            font-size: 32px;
            font-weight: 500;
            line-height: 1.4;
            margin: 40px 0;
            color: #1d1d1f;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        @media (max-width: 768px) {{
            .title {{
                font-size: 24px;
                white-space: normal;
                text-align: center;
            }}
        }}

        .upload-section {{
            background: white;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 20px auto;
            max-width: 600px;
            transition: all 0.3s ease;
        }}

        .lottery-container {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}

        .lottery-content {{
            background: white;
            padding: 40px;
            border-radius: 24px;
            width: 90%;
            max-width: 800px;
            text-align: center;
            position: relative;
        }}

        .ball-container {{
            position: relative;
            width: 400px;
            height: 400px;
            margin: 30px auto;
            border-radius: 50%;
            background: linear-gradient(145deg, #f0f0f0, #e6e6e6);
            box-shadow: inset 0 8px 16px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .ball {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            position: absolute;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            font-weight: 500;
            color: white;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(145deg, #007aff, #0055ff);
        }}

        .winner-ball {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(145deg, #ff3b30, #ff2d55);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            margin: 20px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
            opacity: 0;
            transform: scale(0.5);
        }}

        @keyframes popIn {{
            to {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        .winner-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 30px;
        }}

        .start-button {{
            background: #007aff;
            color: white;
            border: none;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            font-size: 24px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            margin: 20px;
        }}

        .start-button:hover {{
            background: #0055ff;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }}

        .start-button:active {{
            transform: translateY(0);
        }}

        .reset-button {{
            background: #ff3b30;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }}

        .reset-button:hover {{
            background: #ff2d55;
            transform: translateY(-2px);
        }}

        .input-number {{
            width: 100%;
            max-width: 300px;
            padding: 15px;
            border: 3px solid #e6e6e6;
            border-radius: 12px;
            margin: 20px 0;
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            transition: all 0.3s ease;
        }}

        .input-number:focus {{
            border-color: #007aff;
            outline: none;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
        }}

        .result {{
            margin-top: 30px;
            font-size: 28px;
            font-weight: 700;
            color: #1d1d1f;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .result.show {{
            opacity: 1;
            transform: translateY(0);
        }}

        .close-button {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: transparent;
            border: none;
            color: #1d1d1f;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
            border-radius: 50%;
            transition: all 0.3s ease;
        }}

        .close-button:hover {{
            background: rgba(0,0,0,0.1);
        }}

        @media (max-width: 768px) {{
            .ball-container {{
                width: 300px;
                height: 300px;
            }}

            .lottery-content {{
                padding: 20px;
            }}

            .winner-ball {{
                width: 100px;
                height: 100px;
                font-size: 20px;
            }}

            .input-number {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2 class="title">[하나은행] Digital Hana 路 데이터분석/서비스기획 4기 <br> 크리스마스 이벤트</h2>
        
        <div class="upload-section">
            <input type="number" class="input-number" id="numWinners" placeholder="당첨자 수 입력" min="1" max="10">
            <button class="start-button" id="startLottery">추첨 시작!</button>
        </div>
    </div>

    <div class="lottery-container">
        <div class="lottery-content">
            <button class="close-button">&times;</button>
            <div class="ball-container"></div>
            <div class="winner-container"></div>
            <div class="result"></div>
            <button class="reset-button" id="resetLottery">다시 추첨하기</button>
        </div>
    </div>

    <script>
        const playerNames = {names_js_array};
        let isAnimating = false;
        let animationInterval;

        function getRandomPosition(radius) {{
            const angle = Math.random() * 2 * Math.PI;
            const r = Math.random() * radius;
            return {{
                x: r * Math.cos(angle),
                y: r * Math.sin(angle)
            }};
        }}

        function createSuperBallEffect() {{
            const ballContainer = document.querySelector('.ball-container');
            const balls = [];
            const containerWidth = ballContainer.offsetWidth;
            const containerHeight = ballContainer.offsetHeight;
            const centerX = containerWidth / 2;
            const centerY = containerHeight / 2;
            
            ballContainer.innerHTML = '';
            
            playerNames.forEach((name) => {{
                const ball = document.createElement('div');
                ball.className = 'ball';
                ball.textContent = name;
                const pos = getRandomPosition(150);
                ball.style.left = `${{centerX + pos.x}}px`;
                ball.style.top = `${{centerY + pos.y}}px`;
                ballContainer.appendChild(ball);
                balls.push({{
                    element: ball,
                    velocity: {{ x: (Math.random() - 0.5) * 4, y: (Math.random() - 0.5) * 4 }},
                    angle: Math.random() * 2 * Math.PI,
                    speed: 1 + Math.random() * 2
                }});
            }});

            return setInterval(() => {{
                balls.forEach(ball => {{
                    ball.angle += ball.speed * 0.02;
                    ball.velocity.x += (Math.random() - 0.5) * 0.5;
                    ball.velocity.y += (Math.random() - 0.5) * 0.5;
                    
                    let x = centerX + Math.cos(ball.angle) * 150 + ball.velocity.x;
                    let y = centerY + Math.sin(ball.angle) * 150 + ball.velocity.y;
                    
                    if (x < 50) x = 50;
                    if (x > containerWidth - 50) x = containerWidth - 50;
                    if (y < 50) y = 50;
                    if (y > containerHeight - 50) y = containerHeight - 50;
                    
                    ball.velocity.x *= 0.95;
                    ball.velocity.y *= 0.95;
                    
                    ball.element.style.left = `${{x}}px`;
                    ball.element.style.top = `${{y}}px`;
                }});
            }}, 16);
        }}

        function selectWinners(names, count) {{
            const shuffled = [...names].sort(() => Math.random() - 0.5);
            return shuffled.slice(0, count);
        }}

        function showWinners(winners) {{
            const winnerContainer = document.querySelector('.winner-container');
            const result = document.querySelector('.result');
            
            winnerContainer.innerHTML = '';
            winners.forEach((winner, index) => {{
                setTimeout(() => {{
                    const winnerBall = document.createElement('div');
                    winnerBall.className = 'winner-ball';
                    winnerBall.textContent = winner;
                    winnerContainer.appendChild(winnerBall);
                    
                    if (index === winners.length - 1) {{
                        setTimeout(() => {{
                            result.textContent = '축하합니다! 🎉';
                            result.classList.add('show');
                        }}, 500);
                    }}
                }}, index * 800);
            }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            const startButton = document.getElementById('startLottery');
            const resetButton = document.getElementById('resetLottery');
            const lotteryContainer = document.querySelector('.lottery-container');
            const closeButton = document.querySelector('.close-button');
            const numWinnersInput = document.getElementById('numWinners');

            function resetLottery() {{
                if (animationInterval) {{
                    clearInterval(animationInterval);
                }}
                const ballContainer = document.querySelector('.ball-container');
                const winnerContainer = document.querySelector('.winner-container');
                const result = document.querySelector('.result');
                
                ballContainer.innerHTML = '';
                winnerContainer.innerHTML = '';
                result.textContent = '';
                result.classList.remove('show');
                
                lotteryContainer.style.display = 'none';
                isAnimating = false;
            }}

            startButton.addEventListener('click', () => {{
                const numWinners = parseInt(numWinnersInput.value);
                if (!numWinners || numWinners < 1 || numWinners > playerNames.length) {{
                    alert(`당첨자 수는 1명에서 ${{playerNames.length}}명 사이로 입력해주세요.`);
                    return;
                }}

                lotteryContainer.style.display = 'flex';
                isAnimating = true;
                animationInterval = createSuperBallEffect();

                setTimeout(() => {{
                    if (animationInterval) {{
                        clearInterval(animationInterval);
                    }}
                    const winners = selectWinners(playerNames, numWinners);
                    showWinners(winners);
                }}, 3000);
            }});

            resetButton.addEventListener('click', resetLottery);
            closeButton.addEventListener('click', resetLottery);
        }});
    </script>
</body>
</html>
"""

html(html_code, height=800)