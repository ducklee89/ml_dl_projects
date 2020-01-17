from sklearn.externals import joblib 
import json, re 
# 1. python 3.3 이하 버전과 하위 호환을 위해서 사용
# 2. 패키지 자체를 지칭할때 사용

# 0. 경로 -> 상수값 -> 환경변수 혹은 DB에서 획득
MODEL_PATH  = './ml/service/ml/clf_mdoel_202001161419.model'
MODEL_LABEL = './ml/service/ml/clf_labels.label'

if __name__ != '__main__':
    # 1. 모델 로드 (1회만)->요청이 많아지면 컨트롤이 가능한지 체크
    clf = joblib.load( MODEL_PATH )
    # 2. 레이블 로드
    with open(MODEL_LABEL, 'r') as f:
        clf_label = json.load(f)

# 3. 예측 함수 (in:텍스트, out:예측결과)
def detect_lang( text ):
  # A. text -> 빈도계산 ---------------------------------------------------------------
  text = text.lower()           # 1. 소문자 처리
  p    = re.compile('[^a-z]')   # 2. 정규식(알파벳소문자만제외)
  text = p.sub( '' , text )     # 3. 소문자만 남는다
  counts  = [ 0 for n in range(26) ] # 알파벳별 카운트를 담을 공간(리스트)
  limit_a = ord('a')            # 매번 반복해서 작업하니까 그냥 최초 한번 변수로 받아서 사용
  for word in text:
      counts[ord(word)-limit_a] += 1 # 문자 1개당 카운트 추가   
  total_count = sum(counts)
  freq = list( map( lambda x:x/total_count , counts ) )  # 정규화     
  
  # B. 알고리즘에 예측요청(데이터 주입) ------------------------------------------------
  predict = clf.predict( [freq]  )  # 입력 형태를 개발했던 형태와 동일하게 차원을 맞춘다
  na_code = predict[0]              # 'en' or 'fr' ...
  na_str  = clf_label[ na_code ]    # '영어', '프랑스어', ...
  # C. 결과를 리턴 -------------------------------------------------------------------
  return na_code, na_str
  #pass

# 개인별로 신청한 키
CLIENT_ID = 'DG9a4VLy9OS7dxqBvQFO'
SECRET_KEY = 'WZj8dJt7b2'

'''
curl "https://openapi.naver.com/v1/papago/n2mt" \
-H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
-H "X-Naver-Client-Id: DG9a4VLy9OS7dxqBvQFO" \
-H "X-Naver-Client-Secret: WZj8dJt7b2" \
-d "source=ko&target=en&text=만나서 반갑습니다." -v
'''
# 4. 번역 함수 (현:파파고연동, 향후:RNN 구현)
def transfer_lang( text, na_input_code='en', na_output_code='ko' ):
    print('파파고와 연동한 번역 처리 시작')
    return {}

# 이 코드는 개발시 테스트 했던 코드이다. 
# 의도(개발시)될때만 작동해야 한다 
if __name__ == '__main__':
#  print('테스트', PI2)
  test_str ='Bong Joon-ho (en coréen : 봉준호 prononcé en coréen : /poːŋ tɕuːnho → poːŋdʑunho/), né le 14 septembre 1969 à Daegu, est un réalisateur et scénariste sud-coréen.'
  transfer_lang( test_str )