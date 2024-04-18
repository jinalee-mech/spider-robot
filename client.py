#client.py
import time
import cv2
import socket
import numpy as np
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("172.20.10.6", 8888))
print("client connected")
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
while True:
    try:
        ###frame server로 보내줌
        ret, frame = cam.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        send_data = np.array(frame)
        stringData = send_data.tostring()
        client_socket.sendall((str(len(stringData))).encode().ljust(16) + stringData)
        ###server에서 값 받아옴
        # recv_stringData = client_socket.recv(16)
        #
        # if (recv_stringData):
        #     recv_data = np.fromstring(recv_stringData, dtype='uint8')
        #     received_data = recv_data.tolist()
        #     if(received_data[0] == "bird"):
        #         # 카드집고 집에 가기
        #         speed = 100
        #
        #         while True:
        #             # 먹이(카드)저장
        #             crawler.do_step(stand, speed)
        #             print("stand")
        #             sleep(1)
        #             crawler.do_step(sit, speed)
        #             print("sit")
        #             sleep(1)
        #             crawler.do_step(stand, speed)
        #             print("stand")
        #             sleep(1)
        #             # 키보드로 집으로 조작
        #             keycontrol()
        #             # 먹이(카드) 떼놓으면서 보관
        #             crawler.do_step(sit, speed)
        #             print("sit")
        #             sleep(1)
        #             crawler.do_step(stand, speed)
        #             print("stand")
        #             sleep(1)
    except Exception as e:
        print("client-client Exception", e)
        continue
        # exit(0)
    except KeyboardInterrupt:
        cam.release()
        #거미로봇
        client_socket.close()
        exit(0)
        print("terminated..")