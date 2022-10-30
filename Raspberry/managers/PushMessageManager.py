from pyfcm import FCMNotification

# Firebase에서 얻은 server key. 알맞게 수정할 것 https://console.firebase.google.com/project/smartmirror-4bf14/settings/cloudmessaging/android:com.example.smartmirror
APIKEY = "AAAAQd5Gkn0:APA91bHRUsewNt-cjQzmOPgqVB0Vs1BhMXCP2QcN3TRe1zybSMI178SOY6grOSMGogAtiWCgSq5i2Iwft75WeI36es5wjSyf1_t1yRJRL__TlsNxroRxGAjTFLiSFsEPUxqPA4j8z5fT"

# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)

def sendMessage(message, title):
    # 메시지 (data 타입)
    data_message = {
        "message": message,
        "title": title
    }
    # topic을 이용해 다수의 구독자에게 푸시알림을 전송함
    result = push_service.notify_topic_subscribers(topic_name="motion", data_message=data_message)

    # 전송 결과 출력
    print(result)


if __name__ == "__main__":
    sendMessage("motion", "click")
