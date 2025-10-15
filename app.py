import streamlit as st
import random
# import time  # <-- 🚫 time 모듈을 더 이상 사용하지 않으므로 주석 처리하거나 삭제합니다.
from collections import Counter

# ----------------------------------------------------------------------
# 1. 핵심 로직 함수들
# ----------------------------------------------------------------------

# 1-1. 최대공약수(GCD) 계산 (유클리드 호제법)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 1-2. 소인수분해 과정 시각화 함수
def get_prime_factors(n):
    factors = []
    d = 2
    temp_n = n
    while d * d <= temp_n:
        while temp_n % d == 0:
            factors.append(d)
            temp_n //= d
        d += 1
    if temp_n > 1:
        factors.append(temp_n)
    return factors

# 1-3. 두 수의 소인수분해 과정을 텍스트로 시각화 (수정됨: time.sleep 제거)
def visualize_prime_factorization(num1, num2):
    factors1 = get_prime_factors(num1)
    factors2 = get_prime_factors(num2)
    
    st.markdown("### 📝 소인수분해 과정")
    
    # 텍스트를 바로 출력합니다.
    output_text = ""
    
    output_text += f"**1. {num1} 소인수분해:**\n"
    factor_str1 = " \\times ".join(map(str, factors1))
    output_text += f"$$ {num1} = {factor_str1} $$ \n"
    
    output_text += f"**2. {num2} 소인수분해:**\n"
    factor_str2 = " \\times ".join(map(str, factors2))
    output_text += f"$$ {num2} = {factor_str2} $$ \n"

    # 공통 인수 찾기 및 GCD 계산
    c1, c2 = Counter(factors1), Counter(factors2)
    
    common_factors = []
    gcd_result = 1
    
    for p in set(c1.keys()) & set(c2.keys()):
        min_count = min(c1[p], c2[p])
        common_factors.extend([p] * min_count)
        gcd_result *= (p ** min_count)

    gcd_factor_str = " \\times ".join(map(str, common_factors))
    
    output_text += f"**3. 공통 소인수 찾기:**\n"
    output_text += f"공통 소인수의 곱: $${gcd_factor_str}$$ \n"
    
    st.markdown(output_text) # 최종 텍스트를 한 번에 출력
    st.markdown("---")
    
    return gcd_result

# 1-4. 나눗셈 (유클리드 호제법) 과정 시각화 (수정됨: time.sleep 제거)
def visualize_division(a, b):
    A, B = max(a, b), min(a, b)
    
    st.markdown("### 📝 나눗셈 (유클리드 호제법) 과정")
    
    output_text = ""
    
    while B:
        quotient = A // B
        remainder = A % B
        
        step_description = f"""
        - 나눗셈: $${A} = {B} \\times {quotient} + {remainder}$$ 
        - 다음 단계에서는 **{B}**와 **{remainder}**의 GCD를 찾습니다.
        """
        output_text += step_description + "\n"
        
        A, B = B, remainder

    output_text += f"**[최종]** 나머지가 0이 되었습니다. 마지막 나누는 수였던 **{A}**가 최대공약수(GCD)입니다."
    st.markdown(output_text) # 최종 텍스트를 한 번에 출력
    st.markdown("---")
    
    return A

# ----------------------------------------------------------------------
# 2. Streamlit UI (Main App)
# ----------------------------------------------------------------------

st.title("🔢 GCD 마스터 학습 앱")
st.markdown("원하는 두 수를 입력하고 풀이 방법을 선택하여 최대공약수 구하는 과정을 학습해 보세요!")

# --- 입력 섹션 ---
st.subheader("1. 숫자 입력")
col1, col2 = st.columns(2)

num1 = col1.number_input("첫 번째 수", min_value=1, value=12, step=1)
num2 = col2.number_input("두 번째 수", min_value=1, value=18, step=1)

# --- 방법 선택 섹션 ---
st.subheader("2. 풀이 방법 선택")
method = st.radio(
    "어떤 방법으로 풀이 과정을 보시겠어요?",
    ('소인수분해', '나눗셈 (유클리드 호제법)')
)

# --- 풀이 과정 보기 버튼 ---
if st.button("풀이 과정 시뮬레이션 시작"):
    if num1 < 1 or num2 < 1:
        st.error("두 수 모두 1 이상의 정수를 입력해 주세요.")
    else:
        # GCD 최종 계산
        final_gcd = gcd(num1, num2)
        
        st.markdown("## 3. 풀이 과정 시뮬레이션")
        
        if method == '소인수분해':
            visualize_prime_factorization(num1, num2)
        else:
            visualize_division(num1, num2)
            
        # --- 결과 섹션 ---
        st.balloons() # 풍선 효과
        st.header(f"✨ 최종 결과: {num1}과 {num2}의 최대공약수는 **{final_gcd}**입니다.")
        st.markdown("---")

# ----------------------------------------------------------------------
# 3. 퀴즈 섹션
# ----------------------------------------------------------------------

# 퀴즈 상태 초기화 함수 (에러 방지를 위해 분리)
def initialize_quiz_state():
    st.session_state.quiz_num1 = random.randint(10, 50)
    st.session_state.quiz_num2 = random.randint(10, 50)
    st.session_state.quiz_gcd = gcd(st.session_state.quiz_num1, st.session_state.quiz_num2)
    st.session_state.quiz_answered = False
    st.session_state.show_quiz_solution = False

st.markdown("## 4. 🧠 퀴즈 코너")

# 세션 상태 초기화 및 퀴즈 문제 생성 (더 안전한 초기화)
if 'quiz_answered' not in st.session_state or st.session_state.quiz_answered == True:
    initialize_quiz_state()

quiz_num1 = st.session_state.quiz_num1
quiz_num2 = st.session_state.quiz_num2

st.subheader(f"문제: {quiz_num1}과 {quiz_num2}의 최대공약수는 무엇일까요?")

# 퀴즈 정답 입력
user_quiz_answer = st.number_input("정답을 입력하세요:", min_value=1, value=1, step=1, key='quiz_input', disabled=st.session_state.quiz_answered)

# 퀴즈 확인 버튼
if st.button("정답 확인", disabled=st.session_state.quiz_answered):
    st.session_state.quiz_answered = True
    
    if user_quiz_answer == st.session_state.quiz_gcd:
        st.success("🎉 정답입니다! 다음 문제를 풀어보세요.")
        st.session_state.show_quiz_solution = False
    else:
        st.error("❌ 틀렸습니다. 다시 한 번 생각해볼까요?")
        st.session_state.show_quiz_solution = True
        
# 퀴즈 다음 문제 버튼 (수정됨: 에러 방지를 위해 재실행 전에 명시적 초기화)
if st.button("다음 퀴즈로 넘어가기"):
    st.session_state.quiz_answered = False # 재실행 전에 버튼 비활성 상태 해제
    initialize_quiz_state() # 새 문제 생성
    st.experimental_rerun() # 앱을 다시 실행하여 새 문제 표시

# 틀렸을 경우 풀이 과정 보여주기
if st.session_state.show_quiz_solution:
    if st.checkbox("풀이 과정 보기", key='show_quiz_sol_check'):
        st.markdown("---")
        st.subheader(f"✅ {quiz_num1}과 {quiz_num2}의 풀이 과정")
        visualize_division(quiz_num1, quiz_num2)
