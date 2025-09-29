import os
from http import HTTPStatus
from dashscope import Application
def call_with_session():


    response = Application.call(
                api_key="sk-90426267f6844b9d815527ec5c210644",
                app_id='09927ed45026488e961c35d96fb4b5c4',
                prompt='你是什么东西',
                )
    session_id = response.output.session_id

    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')


    session_id = response.output.session_id
    print(response.output.text)

    while True:
        Input = input()
        response = Application.call(
            api_key="sk-90426267f6844b9d815527ec5c210644",
            app_id='09927ed45026488e961c35d96fb4b5c4',
            prompt=Input,
            session_id=session_id,
        )
        print(response.output.text)

        if response.status_code == HTTPStatus.OK:
            print(response.output.text)
        else:
            print(f"出错了：{response.message}")
if __name__ == '__main__':
    call_with_session()