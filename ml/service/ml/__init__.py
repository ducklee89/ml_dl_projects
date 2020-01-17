from sklearn.externals import joblib
import json
import re

# 1. python 3.3 이하 버전과 하위 호환을 위해서 사용
# 2. 패키지 자체를 지칭할때 사용

PI2=3.144

def a():

    print('구동')

# 0. 경로 -> 상수값 -> 환경변수 혹은 DB에서 획득
MODEL_PATH = './ml/service/ml/clf_model_202001161419.model'
MODEL_LABEL = './ml/service/ml/clf_labels.label'

# 1. 모델 로드 (1회만)-> 요청이 많아지던 컨트롤이 가능한지 체크
clf = joblib.load( MODEL_PATH )

# 2. 레이블 로드
with open(MODEL_LABEL, 'r') as f:
    clf_label = json.load(f)


# 3. 예측 함수 (In: 텍스트, out: 예측결과)
def detect_lang( text ):
    # A. text -> 빈도계산 -----------------------------------------------------------------
    # text -> 빈도계산 -> 알고리즘에 예측요청(데이터 주입) -> 그 결과를 리턴
    text = text.lower() # 1. 소문자 처리
    p = re.compile('[^a-z]') # 2. 정규식(알파벳 소문자만 제외)
    text = p.sub('' , text) # 소문자만 남는다
    counts = [0 for n in range(26) ] # 알파벳별 카운트를 담을 공간(리스트)
    limit_a = ord('a') # 매번 반복해서 작업하니까 그냥 최초 한번 변수로 받아서 사용
    for word in text:
        counts[ord(word)-limit_a] += 1 # 문자 1개당 카운트 추가 
    # 빈도수는 값이 너무 퍼져 있어서 0~1사이로 정규화를 하겠다=>학습효과가 뛰어나니까
    total_count = sum(counts)
    freq = list( map( lambda x:x/total_count , counts ) )    #정규화    

    #  B. 알고리즘 예측요청 (데이터 주입) ------------------------------------------------------
    predict = clf.predict( [freq] ) # 입력 형태를 개발했던 형태와 동일하게 차원을 맞춘다
    na_code = predict[0]                      # 'en' or 'fr' ...
    na_str = clf_label[ na_code ] #'영어', '프랑스어', ...
    #  C. 결과를 리턴 -------------------------------------------------------------------------
    return na_code, na_str
    # pass

# 4. 번역 함수 (현:파파고연동, 향후:RNN 구현)
def transfer_lang( text, na_input_code='en', na_output_code='ko' ):
    pass

#이 코드는 개발시 테스트 했던 코드이다.
#의도(개발시)될때만 작동해야 한다.

if __name__ == '__main__':

    print('테스트', PI2)
    a()