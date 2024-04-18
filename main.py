# random move + prey + enemy
from picrawler import Picrawler
from robot_hat import TTS, Music
from robot_hat import Ultrasonic
from robot_hat import Pin
from time import sleep
import readchar
import os
import random
rand_num = random.randint(0, 3)
music = Music()
detect_distance = 50
crawler = Picrawler([10, 11, 12, 4, 5, 6, 1, 2, 3, 7, 8, 9 ])
# crawler.set_offset([0,0,0,0,0,0,0,0,0,0,0,0])
rand_list = ['forward', 'backward', 'turn left', 'turn right']
# rand_move = random.shuffle(rand_list)
stand = [[45, 45, -30],
         [45, 45, -30],
         [45, 45, -30],
         [45, 45, -30]]
sit = [[45, 45, -70],
       [45, 45, -70],
       [45, 45, -70],
       [45, 45, -70]]
# new_step1 = stand
# new_step2 = sit
sonar = Ultrasonic(Pin("D2"), Pin("D3"))
speed = 100
prey = 1
enem = 0
global prey_cnt
prey_cnt = 0
manual = '''
Press keys on keyboard to control PiCrawler!
    w: Forward
    a: Turn left
    s: Backward
    d: Turn right
    h : Back Home
    esc: Quit
'''
def main(prey_cnt):
    print("main 진입")
    while True:
        print("keyboard input")
        key = readchar.readkey()
        key = key.lower()
        if key in('wsadh'):
            if 'w' == key:
                crawler.do_action('forward',1,speed)
            elif 's' == key:
                crawler.do_action('backward',1,speed)
            elif 'a' == key:
                crawler.do_action('turn left',1,speed)
            elif 'd' == key:
                crawler.do_action('turn right',1,speed)
            elif 'h' == key:
                crawler.do_step('sit', speed)
                sleep(0.5)
                crawler.do_step('stand', speed)
                sleep(0.5)
                prey_cnt += 1
                break
            sleep(0.05)
        elif key == readchar.key.CTRL_C or key in readchar.key.ESCAPE_SEQUENCES:
            print("\n Quit")
            break
        sleep(0.02)
    return prey_cnt
def randomgo():
    distance = sonar.read()
    crawler.do_action(rand_list[0], rand_num, speed)
    distance = sonar.read()
    random.shuffle(rand_list)
def detect_sth(cnt=prey_cnt):
    if prey == 1 and enem == 0:  # 먹이 감지
        crawler.do_step('sit', speed)
        sleep(0.5)
        crawler.do_step('stand', speed)
        sleep(0.5)  # 원래는 이 사이에 키보드 제어 들어가서 집에서 앉았다가 일어나면 cnt += 1
        crawler.do_action('backward', 3, speed)
        sleep(0.5)
        crawler.do_action('turn left', 5, speed)
        sleep(0.5)
        prey_cnt += 1
        print(prey_cnt)
        cnt = main(cnt)
    elif prey == 0 and enem == 1:  # 천적 감지
        music.sound_effect_threading('./sounds/sign.wav')
        sleep(0.5)
        crawler.do_action('backward', 3, speed)
        sleep(0.5)
        crawler.do_action('turn left', 5, speed)
        sleep(0.5)
    else:  # 장애물/울타리 감지
        crawler.do_action('backward', 3, speed)
        sleep(0.5)
        crawler.do_action('turn_left', 5, speed)
        sleep(0.5)
    return cnt
while prey_cnt < 2:
    distance = sonar.read()
    if distance <= 0:
        randomgo()
    elif 0 < distance < detect_distance:  # detect_distance(50)보다 안에 있다.
        if distance > 30:  # 30보다 클 때
            while distance > 10:  # 10보다 작게 될 때까지 앞으로 직진
                crawler.do_action('forward', 1, speed)
                sleep(0.05)
                distance = sonar.read()
            sleep(0.5)
            prey_cnt = detect_sth()  # 먹이or천적or울타리 구별하는 함수
            if prey_cnt == 2:
                break
            randomgo()
        else:  # 첫판부터 10보다 작을 때
            sleep(0.5)
            prey_cnt = detect_sth(prey_cnt)  # 먹이or천적or울타리 구별하는 함수
            randomgo()
    else:  # distance > 30 # 30보다 멀어지면 랜덤하게 move
        crawler.do_action(rand_list[0], rand_num, speed)
        distance = sonar.read()
        random.shuffle(rand_list)