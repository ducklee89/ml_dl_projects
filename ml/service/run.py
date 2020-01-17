# 엔트리 포인트 : 진입로, 시작점, 모든 경로법은 엔트리로부터 따진다.
# 1. 모듈 가져오기 ----------------------------------------------------------------------
# 플라스크 관련 모듈 가져오기
from flask import Flask, render_template, request, jsonify, redirect
# 테스트 모듈 가져오기
from ml.mod import PI
#언어 감지 및 번역 모듈 가져오기
from ml import detect_lang, transfer_lang
#1. 모듈 가져오기 end --------------------------------------------------------------------

# 2. Flask 객체 생성
app = Flask( __name__ )
# 3. 라우팅
@app.route('/')
def home():
    text_str = '''
...
'''
    print( detect_lang(text_str) )
    return render_template('index.html')
# restful
@app.route('/bsgo', methods=['GET', 'POST'])
def bsgo():
    if request.method == 'GET':
        return render_template('bsgo.html')
    else:
        # 전달된 데이터 획득
        print(request.form['o'])
        # 언어감지
        # 결과를 응답
        return ''
        # pass


# 4. 서버 가동
if __name__ == '__main__':
    app.run(debug=True)

else:
    print('작동 않됨')


