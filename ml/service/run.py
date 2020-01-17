# 엔트리 포인트 : 진입로, 시작점, 모든 경로법은 엔트리로부터 따진다.
# 1. 모듈 가져오기 ----------------------------------------------------------------------
# 플라스크 관련 모듈 가져오기
from flask import Flask, render_template, request, jsonify, redirect
# 테스트 모듈 가져오기
from ml.mod import *
#언어 감지 및 번역 모듈 가져오기
from ml import detect_lang as dl, transfer_lang
#1. 모듈 가져오기 end --------------------------------------------------------------------

# 2. Flask 객체 생성
app = Flask( __name__ )\
# 3. 라우팅
@app.route('/')
def home():
    import os
    import sys
    import urllib.request
    import ml
    client_id = ml.CLIENT_ID # "YOUR_CLIENT_ID" # 개발자센터에서 발급받은 Client ID 값
    client_secret = ml.SECRET_KEY # "YOUR_CLIENT_SECRET" # 개발자센터에서 발급받은 Client Secret 값

    encText = urllib.parse.quote("반갑습니다") # 한글의 URL 인코딩 처리 => %2D..... 변환처리
    data = "source=ko&target=en&text=" + encText # 파라미터 구성
    url = "https://openapi.naver.com/v1/papago/n2mt" # 주소
    request = urllib.request.Request(url) # 요청객체 생성
    request.add_header("X-Naver-Client-Id",client_id) # 헤더 설정
    request.add_header("X-Naver-Client-Secret",client_secret) # 헤더 설정

    response = urllib.request.urlopen(request, data=data.encode("utf-8")) # 요청
    rescode = response.getcode() # 응답코드 획득
    if(rescode==200): # 응답 성공
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
    
    return render_template('index.html')
# restful
@app.route('/bsgo', methods=['GET', 'POST'])
def bsgo():
    if request.method == 'GET':
        return render_template('bsgo.html')
    else:
        # 전달된 데이터 획득
        # print(request.form.get['ol'])
        oriTxt = request.form.get('o') # 내용이 들어있고, 100글자 이상이다.
        # print(oriTxt)
        # print(request.form['ol']) # 만약 키가 틀리면 오류를 발생한다.
        # 언어감지
        na_code, na_str = dl( oriTxt )
        
        if na_code:# 예측 되었다
            res = {
                'code':na_code,
                'code_str':na_str
            }
        else:
            res = {
                'code':'0',
                'code_str':'언어 감지 실패'
            }
        # 결과를 응답
        return jsonify( res )
        # pass

#번역 처리
@app.route('/transfer', methods=['POST'])
def transfer():
    #데이터 획득
    oriTxt = request.form.get('o')
    na = request.form.get('na')

    #번역
    res = transfer_lang( oriTxt, na )
    #로그 처리
    #응답
    return jsonify(res)

# 4. 서버 가동
if __name__ == '__main__':
    app.run(debug=True)

else:
    print('작동 않됨')


