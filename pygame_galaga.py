import pygame
# pygame.display.set_mode(resolution=0, 0)
# pygame.display.flip()
# pygame.event.get()
import random
import logging
import time
from time import sleep

# 게임에 사용되는 전역 변수 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
pad_width = 480     #화면 넓이
pad_height = 640    #화면 높이
fight_width = 36    #갤럭시안 넓이
fight_height = 38   #갤럭시안 높이
enemy_width = 26    #적 넓이
enemy_height = 20   #적 높이
score = [100, 120, 140, 160, 5000]  #적, 보스 스코어

#게임 오버 메세지
def gameover():
    global gamepad
    dispMessage('Game Over')

    #자동 재시작(제거예정)
    sleep(2)
    runGame()

# 적을 맞춘 개수 계산(제거 예정)
def drawScore(count):
    global gamepad

    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Kills: ' + str(count), True, WHITE)
    gamepad.blit(text, (0, 0))

#적을 보낸 개수 계산(제거 예정)
def drawPassed(count):
    global gamepad

    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Passed: ' + str(count), True, RED)
    gamepad.blit(text, (360, 0))


# 화면에 글씨 보이게 하기
def dispMessage(text):
    global gamepad

    textfont = pygame.font.Font('freesansbold.ttf', 80) #폰트 불러오기, 폰트 크기
    text = textfont.render(text, True, RED) #텍스트 생성(내용, Anti-aliasing 사용 여부, 텍스트 색상)
    textpos = text.get_rect()   #텍스트 위치 가져오기
    textpos.center = (pad_width/2, pad_height/2)    #텍스트 중앙 좌표 지정
    gamepad.blit(text, textpos) #텍스트 그리기(내용, 위치) 
    pygame.display.update() #전체 업데이트

#충돌 메세지(제거 예정)
def crash():
    global gamepad
    dispMessage('Crashed!')

    #자동 재시작
    sleep(2)
    runGame()    

# 게임에 등장하는 객체를 그려줌
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x,y))

#갤러리안 구동 함수
def playFighter():
    global x
    #갤러리안 좌표 이동
    #갤러리안이 벽에 충돌시 밖으로 나가지 않게 좌표 수정
    x += x_change
    if x < 0:
        x = 0
    elif x > pad_width - fight_width:
        x = pad_width - fight_width

    y += y_change
    if y < 0:
        y = 0
    elif y > pad_height - fight_height:
        y = pad_height - fight_height

    drawObject(fighter, x, y)   #갤러리안 그리기

#미사일 구동 함수
def playBullit():
    #갤러리안 무기 발사 구현
    if len(bullet_xy) != 0:
        #발사된 미사일 xy좌표를 차례로 가져와서 처리
        for i, bxy in enumerate(bullet_xy):
            #미사일 y좌표 변경
            bxy[1] -= 10
            bullet_xy[i][1] = bxy[1]
            
            #미사일이 화면을 벗어났을경우 제거
            if bxy[1] <= 0:
                try:
                    bullet_xy.remove(bxy)
                except:
                    pass
    
    #미사일 xy리스트의 요소가 0개가 아닐시 미사일 그리기
    if len(bullet_xy) != 0:
        for bx, by in bullet_xy:
            drawObject(bullet, bx, by)

# 적0 생성 함수
def createEnemy0():
    enemy_x = random.randrange(0, pad_width-enemy_width)    #적 위치 랜덤 x좌표로 지정
    enemy_y = 0 #적 y 지정
    for i in range(5):
        enemy_xy[0].append([enemy_x, enemy_y])  #적 xy좌표 리스트 적0 리스트 부분에 생성할 새로운 적의 xy 좌표 리스트 추가
        enemy_y += -(enemy_height+5)    #맨 앞 적 뒤에 따라 나오는 적들 y값 (바로 앞의 적 y값) - (적 세로 높이+간격)으로 설정, 더 큰 음수로 설정하는 좌표상 더 위에 생성해야해서

#적0 구동 함수
def playEnemy0(enemy0_speed, time_now):
    #현재 플레이 시간이 인자로 전달받은 적0의 다음 레벨로 넘어가는 기준값보다 크다면
    if time_now > nextLevel:
        enemy_persentage[0]+10 #적0 등장확률 증가
        nextLevel[0]+=10    #적0 다음 레벨로 넘어가는 기준값 증가

    if random.randrange(1, 100) > enemy_persentage[0]:  # 1~100 랜덤 돌려서 나온 숫자가 적0 퍼센테이지 값보다 높다면
        createEnemy0()  #적0 생성 함수 실행

    for i, exy in enumerate(enemy_xy[0]):   #i: 현재 접근중인 인덱스값, exy: 현재 접근중인 적 좌표 리스트 [x,y]
        #적0 y좌표 변경
                exy[1] += enemy0_speed #적0의 스피드만큼 y값 이동
                enemy_xy[0][i][1] = exy[1]  #전역변수 적 리스트에 변경된 y값 저장
                
                #적이 화면을 벗어났을경우 적0 리스트에서 제거
                if exy[1] >= pad_height:
                    try:
                        enemy_xy[0].remove(exy)
                    except:
                        pass
                #적0 xy리스트의 요소가 0개가 아닐시 적0 그리기
                if len(enemy_xy[0]) != 0:
                    drawObject(enemy[0], exy[0], exy[1])

# 게임 실행 메인 함수
def runGame():
    global gamepad, fighter, clock
    global bullet, enemy
    global enemy_xy, enemy_persentage, nextLevel
    global x_change, y_change, x, y, bullet_xy

    count = 0   #격추한 수

    x = pad_width*0.45  #갤러리안의 X좌표(좌측)
    y = pad_height*0.9  #갤러리안의 Y좌표(상단)
    x_change = 0    #갤러리안의 x좌표 변화량
    y_change = 0    #갤러리안의 y좌표 변화량

    bullet_xy = []  #미사일 xy 좌표
    enemy_xy = [[], [], [], []]
    enemy_speed = [3, 3, 3, 3] #적 스피드
    enemy_persentage = [10, 10, 10 ,10]
    nextLevel = [10, 10, 10, 10]
        
    ongame = False
    onPause = False
    startTime = time.time()
    while not ongame:
        for event in pygame.event.get():    #키 이벤트 처리  
            if event.type == pygame.QUIT:   #화면 종료시
                ongame = True   #게임 종료 트리거
            #키가 눌렸을때
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 5
                    
                elif event.key == pygame.K_RIGHT:
                    x_change += 5

                elif event.key == pygame.K_UP:
                    y_change -= 5

                elif event.key == pygame.K_DOWN:
                    y_change += 5
                    
                elif event.key == pygame.K_SPACE:
                    if len(bullet_xy) < 100:    #미사일 xy좌표 저장값이 100개 이하라면
                        bullet_x = x + fight_width/2    #미사일의 x좌표를 갤러리안 이미지의 중앙으로 설정
                        bullet_y = y - fight_height     #미사일의 y좌표를 갤러리안의 y좌표로 설정
                        bullet_xy.append([bullet_x, bullet_y])  #미사일의 xy좌표를 저장

                #ESC를 누르면 종료
                elif event.key == pygame.K_ESCAPE:
                    ongame = True

                #엔터를 누를시 게임 일시정지/해제
                elif event.key == pygame.K_RETURN:
                    if onPause == True:
                        onPause = False
                    else :
                        dispMessage('Pause!')
                        onPause = True
            #키가 눌리지 않았을때(키 누른거 풀음)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        #일시정지가 true일시 일시정지
        if onPause == True :
            clock.tick(60)  #프레임 초당 60fps 설정
            continue    #이 밑의 코드 모드 건너뛰기
        
        ###########################################################################
        #일시정지시 정지되어야하는 기능은 모두 이 밑에서 구현
            
        gamepad.fill(BLACK) #배경 검은색으로 채우기

        #갤러리안 구동
        playFighter()

        #미사일 구동
        playBullit()

        #적0 구동 (적0 스피드, 플레이타임(현재시각-시작시간))
        playEnemy0(enemy_speed[0], time.time()-startTime)

        #적 격추 구현
        #미사일과 적이 충돌시 미사일 제거
        if bxy[1] < enemy_y:
            if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                bullet_xy.remove(bxy)

        #갤러리안이 적과 충돌했는지 체크(적 격추부분으로 옮겨야함)
        if y < enemy_y + enemy_height:
            if (enemy_x > x and enemy_x < x + fight_width) or \
                (enemy_x + enemy_width > x and enemy_x+ enemy_width < x + fight_width):
                crash()
                
        pygame.display.update() #화면 전체 업데이트
        clock.tick(60)  #프레임 초당 60fps 설정

    pygame.quit()   #무한루프에서 탈출시 화면 삭제

#초기 설정
def initGame():
    global gamepad, fighter, clock
    global bullet, enemy

    pygame.init()   #파이게임 라이브러리 초기화
    gamepad = pygame.display.set_mode((pad_width, pad_height))  #화면 크기 설정 및 생성
    pygame.display.set_caption('MyGalaga')  #게임 창 제목 설정
    fighter = pygame.image.load('Galaga\\fighter.png')    #갤러리안 이미지 설정
    enemy = [pygame.image.load('Galaga\\enemy.png')]    #적 이미지 설정
    bullet = pygame.image.load('Galaga\\bullet.png')  #미사일 이미지 설정
        
    clock = pygame.time.Clock()   #파이게임 시계 가져오기


initGame()  #게임 초기 설정 실행
runGame()   #게임 실행
