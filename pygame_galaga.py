import pygame
# pygame.display.set_mode(resolution=0, 0)
# pygame.display.flip()
# pygame.event.get()
import random
import logging
import time
import os
from time import sleep

pygame.init() #파이게임 초기화

#이미지, 음향 파일 경로
img_path = os.path.dirname(os.path.realpath(__file__))+'\Image\\'
sound_path = os.path.dirname(os.path.realpath(__file__))+'\sound\\'

# 게임에 사용되는 전역 변수 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
pad_width = 480     #화면 넓이
pad_height = 640    #화면 높이
fight_width = 30    #갤럭시안 넓이
fight_height = 32   #갤럭시안 높이
enemy_width = 26    #적 넓이
enemy_height = 20   #적 높이
bullet_width = 4    #미사일 넓이
bullet_height = 20  #미사일 높이
scoreList = [10, 12, 12, 30, 15, 50, 10000]  #적, 보스 스코어
start_life = 3  #시작 생명
start_bQuantity = 1  #시작 미사일 수량
start_bSpeed = 10    #시작 미사일 속도
Item_width = 18 #아이템 높이
Item_height = 18    #아이템 넓이

enemy_bullet_speed = 10 #적5 미사일 속도
Restart = 0 # 재시작 여부

laser_width = 25  #레이저 넓이
laser_height = 640 #레이저 높이
boss_width = 42   #보스 넓이
boss_height = 45  #보스 높이
curtain_height = 200 #장막 높이
startTime = 0

# 스코어 화면에 띄우기
def drawScore(count):
    global gamepad

    font = pygame.font.SysFont(None, 20)
    text = font.render('Score: ' + str(count), True, WHITE)
    gamepad.blit(text, (0, 0))

# 시간 화면에 띄우기
def drawTime(time):
    global gamepad
    
    min = str(int(time // 60)).zfill(2)
    second = str(int((time % 60)//1)).zfill(2)
    mSecond = str(int((time % 1) // 0.01)).zfill(2)
    text = min+":"+second+":"+mSecond

    font = pygame.font.SysFont(None, 20)
    text = font.render('Time: ' + text, True, WHITE)
    gamepad.blit(text, (385, 0))

# 시작 메시지 그리기
def startMessage(text, size, font, color):
    global gamepad

    textfont = pygame.font.Font('freesansbold.ttf', font) #폰트 불러오기, 폰트 크기
    text = textfont.render(text, True, color) #텍스트 생성(내용, Anti-aliasing 사용 여부, 텍스트 색상)
    textpos = text.get_rect()   #텍스트 위치 가져오기
    textpos.center = (pad_width/2, pad_height/2 + size)    #텍스트 중앙 좌표 지정
    gamepad.blit(text, textpos) #텍스트 그리기(내용, 위치) 
    pygame.display.update() #전체 업데이트

# 화면에 글씨 보이게 하기
def dispMessage(text):
    global gamepad

    textfont = pygame.font.Font('freesansbold.ttf', 80) #폰트 불러오기, 폰트 크기
    text = textfont.render(text, True, RED) #텍스트 생성(내용, Anti-aliasing 사용 여부, 텍스트 색상)
    textpos = text.get_rect()   #텍스트 위치 가져오기
    textpos.center = (pad_width/2, pad_height/2)    #텍스트 중앙 좌표 지정
    gamepad.blit(text, textpos) #텍스트 그리기(내용, 위치) 
    pygame.display.update() #전체 업데이트

#게임오버 메세지
def crash(count):
    global gamepad

    
    game_over.play()
    sleep(2.5)
    gamepad.fill(BLACK) #배경 검은색으로 채우기
    startMessage('GameOver!', -100, 80, RED)
    startMessage('Score: ' + str(count), 0, 45, WHITE)
    startMessage("press enter to start", 100, 45, WHITE)
    while True:

        key = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #화면 종료시
                    pygame.quit()   #게임 종료
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: #시작
                    runGame()
                elif event.key == pygame.K_ESCAPE: #종료
                    pygame.quit()
                

#시작 화면 함수
def start():
    global Restart, startTime
    if Restart == 0:
        key = False
        while True:
            startMessage("Galaga", -150, 80, RED)
            startMessage("press enter to start", 150, 45, WHITE)
            drawObject(fighter, pad_width/2, pad_height/2-50)
            drawObject(fighter, pad_width/2 - 50, pad_height/2-50)
            drawObject(fighter, pad_width/2 - 26, pad_height/2)
            drawObject(boss, pad_width/2-26, pad_height*0.1)
            ongame = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   #화면 종료시
                    pygame.quit()   #게임 종료
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: #시작
                        startTime = time.time()
                        key = True
                    elif event.key == pygame.K_ESCAPE: #종료
                        pygame.quit()
            if key:
                break
            elif ongame:
                return True
    else:
        return False
    
#게임 클리어
def clear(count, time):
    game_clear.play()
    sleep(2)
    min = str(int(time // 60)).zfill(2)
    second = str(int((time % 60)//1)).zfill(2)
    mSecond = str(int((time % 1) // 0.01)).zfill(2)

    text = min+":"+second+":"+mSecond
    gamepad.fill(BLACK) #배경 검은색으로 채우기
    startMessage("CLEAR!", -150, 80, BLUE)
    sleep(2)
    startMessage('Score: ' + str(count), -50, 45, WHITE)
    sleep(1)
    startMessage('Time: ' + text, 50, 45, WHITE)
    sleep(1)
    startMessage("press enter to restart", 150, 45, RED)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #화면 종료시
                pygame.quit()   #게임 종료
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: #재시작
                    runGame()
                elif event.key == pygame.K_ESCAPE: #종료
                    pygame.quit()

# 게임에 등장하는 객체를 그려줌
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x,y))

#갤러리안 구동 함수
def playFighter():
    global x, y, fPass, fCount
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

    if fPass == True:
        fCount += 1
        if 10 < fCount < 20:
            drawObject(fighter, x, y)
        elif fCount == 20:
            fCount = 0
    else:
        drawObject(fighter, x, y)   #갤러리안 그리기

#미사일 구동 함수
def playBullit():
    #갤러리안 무기 발사 구현
    if len(bullet_xy) != 0:
        #발사된 미사일 xy좌표를 차례로 가져와서 처리
        for i, bxy in enumerate(bullet_xy): #bullet_xy 리스트 가져와서 for문 돌리기 -> i: 현재 접근중인 인덱스 번호, bxy: 현재 접근중인 요소(bullet의 xy 좌표 리스트)
            #미사일 y좌표 변경
            bxy[1] -= bullet_speed
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

#적5 미사일 구동 함수
def enemyBullit():
    #적5 무기 발사 구현   
    if len(enemy_xy[6]) != 0:
        #발사된 미사일 xy좌표를 차례로 가져와서 처리
        for i, bxy in enumerate(enemy_xy[6]): #bullet_xy 리스트 가져와서 for문 돌리기 -> i: 현재 접근중인 인덱스 번호, bxy: 현재 접근중인 요소(bullet의 xy 좌표 리스트)
            #미사일 y좌표 변경
            bxy[1] += enemy_bullet_speed
            enemy_xy[6][i][1] = bxy[1]
            
            #미사일이 화면을 벗어났을경우 제거
            if bxy[1] >= pad_height:
                try:
                    enemy_xy[6].remove(bxy)
                except:
                    pass
            
    #미사일 xy리스트의 요소가 0개가 아닐시 미사일 그리기
    if len(enemy_xy[6]) != 0:
        for bx, by in enemy_xy[6]:
            drawObject(enemybullet, bx, by)

#미사일 속도 아이템 생성 함수
def createSpeedItem(): 
    bSpeed_xy[0] = random.randrange(0, pad_width-Item_width)    #미사일 속도 아이템 위치 랜덤 x좌표로 지정
    bSpeed_xy[1] = 0  #미사일 속도 아이템 y 지정

#미사일 속도 아이템 구동 함수
def playSpeedItem():
    global bSpeed_play, bullet_speed, x, y
    if bSpeed_xy[1]+Item_height >= pad_height:
        bSpeed_play = False   #미사일 속도 아이템이 화면 밖으로 나갔다면 속도 아이템 구동 중지
    elif((y+1 < bSpeed_xy[1] < y + fight_height-1) or (y+1 < bSpeed_xy[1] + Item_height < y + fight_height-1)) and\
        ((x+1 < bSpeed_xy[0] < x + fight_width-1) or (x+1 < bSpeed_xy[0] + Item_width < x + fight_width-1)):
        bullet_speed += 5 #미사일 속도 아이템이 전투기와 닿았다면 속도 증가
        speed_up.play()
        bSpeed_play = False   #미사일 속도 아이템 실행여부 거짓
        for i in range(len(enemy_persentage)):
            enemy_persentage[i] += 1
    else:
        bSpeed_xy[1] += item_speed    #미사일 속도 아이템의 이동 속도만큼 y값 이동
        drawObject(bSpeedItem, bSpeed_xy[0], bSpeed_xy[1])    #미사일 속도 아이템 그리기

#미사일 개수 아이템 생성 함수
def createQuantityItem(): 
    bQuantity_xy[0] = random.randrange(0, pad_width-Item_width)    #미사일 개수 아이템 위치 랜덤 x좌표로 지정
    bQuantity_xy[1] = 0  #미사일 개수 아이템 y 지정

#미사일 개수 아이템 구동 함수
def playQuantityItem():
    global bQuantity_play, bullet_quantity, x, y
    if bQuantity_xy[1]+Item_height >= pad_height:
        bQuantity_play = False   #미사일 개수 아이템이 화면 밖으로 나갔다면 개수 아이템 구동 중지
    elif((y+1 < bQuantity_xy[1] < y + fight_height-1) or (y+1 < bQuantity_xy[1] + Item_height < y + fight_height-1)) and\
        ((x+1 < bQuantity_xy[0] < x + fight_width-1) or (x+1 < bQuantity_xy[0] + Item_width < x + fight_width-1)):
        bullet_quantity += 1 #미사일 개수 아이템이 전투기와 닿았다면 개수 증가
        quantity_up.play()
        bQuantity_play = False   #미사일 개수 아이템 실행여부 거짓
        for i in range(len(enemy_persentage)):
            enemy_persentage[i] += 1
    else:
        bQuantity_xy[1] += item_speed    #미사일 개수 아이템의 이동 개수 y값 이동
        drawObject(bQuantityItem, bQuantity_xy[0], bQuantity_xy[1])    #미사일 개수 아이템 그리기

#생명 표시
def drawLife(n):
    global life
    #생명 크기 26x28
    paddingX = 0    #왼쪽에 표시된 생명 이미지 개수만큼 띄워야 하는 여백
    for i in range(n):  #매개변수로 받은 남은 생명만큼(n) 반복
        drawObject(life, paddingX, pad_height-28)   #생명 그리기
        paddingX += 26  #여백 추가

#생명 아이템 생성 함수
def createLifeItem(): 
    life_xy[0] = random.randrange(0, pad_width-Item_width)    #생명 아이템 위치 랜덤 x좌표로 지정
    life_xy[1] = 0  #생명 아이템 y 지정

#생명 아이템 구동 함수
def playLifeItem():
    global life_play, life_count, x, y
    if life_xy[1]+Item_height >= pad_height:
        life_play = False   #생명 아이템이 화면 밖으로 나갔다면 생명아이템 구동 중지
    elif((y+1 < life_xy[1] < y + fight_height-1) or (y+1 < life_xy[1] + Item_height < y + fight_height-1)) and\
        ((x+1 < life_xy[0] < x + fight_width-1) or (x+1 < life_xy[0] + Item_width < x + fight_width-1)):
        life_count += 1 #생명 아이템이 전투기와 닿았다면 생명 추가
        heart_up.play()
        life_play = False   #생명아이템 실행여부 거짓
    else:
        life_xy[1] += item_speed    #생명 아이템의 이동 속도만큼 y값 이동
        drawObject(lifeItem, life_xy[0], life_xy[1])    #생명아이템 그리기

# 적0 생성 함수
def createEnemy0():
    enemy_x = random.randrange(0, pad_width-enemy_width)    #적 위치 랜덤 x좌표로 지정
    enemy_y = 0 #적 y 지정
    for i in range(3):
        enemy_xy[0].append([enemy_x, enemy_y])  #적 xy좌표 리스트 적0 리스트 부분에 생성할 새로운 적의 xy 좌표 리스트 추가
        enemy_y += -(enemy_height+5)    #맨 앞 적 뒤에 따라 나오는 적들 y값 (바로 앞의 적 y값) - (적 세로 높이+간격)으로 설정, 더 큰 음수로 설정하는 좌표상 더 위에 생성해야해서

#적0 구동 함수
def playEnemy0(enemy0_speed, time_now):
    global enemy0_count_0, elimit
    #현재 플레이 시간이 인자로 전달받은 적0의 다음 레벨로 넘어가는 기준값보다 크다면
    if time_now > nextLevel[0]:
        enemy_persentage[0]+5 #적0 등장확률 증가
        nextLevel[0]+=20    #적0 다음 레벨로 넘어가는 기준값 증가
    #적 생성
    #if len(enemy_xy[0]) == 0:  #적 생성 후 생성한 적이 사라질때까지 새로운 시퀀스를 생성하지 않을시 이 코드 추가
    if random.randrange(0, 1000) < enemy_persentage[0] and elimit == False:  # 0~100 랜덤 돌려서 나온 숫자가 적0 퍼센테이지 값보다 높다면

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
            drawObject(enemy0, exy[0], exy[1]) #이후 각 적마다 이미지 추가후 이미지 변경 

# 적1 생성 함수
def createEnemy1():
    enemy_x = random.randrange(0, pad_width-enemy_width)    #적 위치 랜덤 x좌표로 지정
    enemy_y = 0 #적 y 지정
    enemy_z = 0 #적 방향 지정 (화면 좌측에선 1, 우측에선 -1)
    if enemy_x<=pad_width/2:
        enemy_z=1
    else:
        enemy_z=-1
    for i in range(3):
        enemy_xy[1].append([enemy_x, enemy_y, enemy_z])  #적 xy좌표 리스트 적1 리스트 부분에 생성할 새로운 적의 xy 좌표 리스트 추가
        enemy_y += -(enemy_height+5)    #맨 앞 적 뒤에 따라 나오는 적들 y값 (바로 앞의 적 y값) - (적 세로 높이+간격)으로 설정, 더 큰 음수로 설정하는 좌표상 더 위에 생성해야해서

#적1 구동 함수
def playEnemy1(enemy1_speed, time_now):
    global enemy1_count_0, elimit
    #현재 플레이 시간이 인자로 전달받은 적1의 다음 레벨로 넘어가는 기준값보다 크다면
    if time_now > nextLevel[1]:
        enemy_persentage[1]+2 #적1 등장확률 증가
        nextLevel[1]+=20    #적1 다음 레벨로 넘어가는 기준값 증가
    #적 생성
    #if len(enemy_xy[1]) == 0:  #적 생성 후 생성한 적이 사라질때까지 새로운 시퀀스를 생성하지 않을시 이 코드 추가
    if random.randrange(0, 1000) < enemy_persentage[1]:  # 0~100 랜덤 돌려서 나온 숫자가 적1 퍼센테이지 값보다 높다면
        if elimit == False:
            createEnemy1()  #적1 생성 함수 실행
        else:
            pass

    for i, exy in enumerate(enemy_xy[1]):   #i: 현재 접근중인 인덱스값, exy: 현재 접근중인 적 좌표 리스트 [x,y]
        exy[1] += enemy1_speed #적1의 스피드만큼 y값 이동
        if exy[1]>=3*pad_height/4:
            exy[0]+=enemy1_speed*2*exy[2] #3/4 위치에서 3차 방향 전환
        elif exy[1]>=pad_height/2:
            exy[0]+=enemy1_speed*exy[2] #1/2 위치에서 2차 방향 전환
        elif exy[1]>=pad_height/4:
            exy[0]+=enemy1_speed/2*exy[2] #1/4 위치에서 1차 방향 전환
        enemy_xy[1][i][1] = exy[1]  #전역변수 적 리스트에 변경된 y값 저장
                
        #적이 화면을 벗어났을경우 적1 리스트에서 제거
        if exy[1] >= pad_height or exy[0]<=0 or exy[0]>=pad_width-10:
            try:
                enemy_xy[1].remove(exy)
            except:
                pass
        #적1 xy리스트의 요소가 0개가 아닐시 적1 그리기
        if len(enemy_xy[1]) != 0:
            drawObject(enemy1, exy[0], exy[1])
        elif time_now >= boss_time:
            enemy1_count_0 = True

# 적2 생성 함수
def createEnemy2():
    enemy_x = random.randrange(2*enemy_width, pad_width-2*enemy_width)    #적 위치 랜덤 x좌표로 지정
    enemy_y = 0 #적 y 지정
    enemy_z = 0 #적 방향 지정 (화면 좌측에선 1, 우측에선 -1)
    if enemy_x<=pad_width/2:
        enemy_z=1
    else:
        enemy_z=-1
    for i in range(3):
        enemy_xy[2].append([enemy_x, enemy_y, enemy_z])  #적 xy좌표 리스트 적2 리스트 부분에 생성할 새로운 적의 xy 좌표 리스트 추가
        enemy_x += enemy_z*-(enemy_width+10)    #맨 앞 적 뒤에 따라 나오는 적들 x값 (바로 앞의 적 x값) - (적 넓이+간격)으로 설정
        enemy_y += -(enemy_height+5)    #맨 앞 적 뒤에 따라 나오는 적들 y값 (바로 앞의 적 y값) - (적 세로 높이+간격)으로 설정, 더 큰 음수로 설정하는 좌표상 더 위에 생성해야해서

#적2 구동 함수
def playEnemy2(enemy2_speed, time_now):
    global enemy2_count_0, elimit
    #현재 플레이 시간이 인자로 전달받은 적2의 다음 레벨로 넘어가는 기준값보다 크다면
    if time_now > nextLevel[2]:
        enemy_persentage[2]+=2 #적2 등장확률 증가
        nextLevel[2]+=30    #적2 다음 레벨로 넘어가는 기준값 증가
    #적 생성
    #if len(enemy_xy[2]) == 0:  #적 생성 후 생성한 적이 사라질때까지 새로운 시퀀스를 생성하지 않을시 이 코드 추가
    if random.randrange(0, 1000) < enemy_persentage[2]:  # 0~100 랜덤 돌려서 나온 숫자가 적2 퍼센테이지 값보다 높다면
        if elimit == False:
            createEnemy2()  #적0 생성 함수 실행
        else:
            pass

    for i, exy in enumerate(enemy_xy[2]):   #i: 현재 접근중인 인덱스값, exy: 현재 접근중인 적 좌표 리스트 [x,y]
        #적0 y좌표 변경
        exy[1] += enemy2_speed/5 #적2의 스피드만큼 y값 이동
        exy[0] += (4*enemy2_speed/5) * exy[2] #지정 방향으로 x값 이동

        if exy[0]<0 or exy[0]>pad_width-enemy_width:
            #화면 탈출로 인한 끼임현상 방지
            if exy[0]<0: exy[0]=0
            if exy[0]>pad_width-enemy_width: exy[0]=pad_width-enemy_width
            #벽에 닿으면 방향 반전
            exy[2]*=-1 
        enemy_xy[2][i][1] = exy[1]  #전역변수 적 리스트에 변경된 y값 저장
        enemy_xy[2][i][2] = exy[2]  #전역변수 적 리스트에 변경된 방향 저장
        
        #적이 화면을 벗어났을경우 적2 리스트에서 제거
        if exy[1] >= pad_height:
            try:
                enemy_xy[2].remove(exy)
            except:
                pass
        #적2 xy리스트의 요소가 0개가 아닐시 적2 그리기
        if len(enemy_xy[2]) != 0:
            drawObject(enemy2, exy[0], exy[1])
        elif time_now >= boss_time:
            enemy2_count_0 = True

# 적3 생성 함수
def createEnemy3():
    enemy_x = random.choice([0, pad_width-enemy_width])    #화면 양 끝 중 하나로 x좌표로 지정
    enemy_y = random.randrange(pad_height//2, pad_height-enemy_height)  #적 위치 범위 내 랜덤 y좌표로 지정
    enemy_z = 0 #적 방향 지정 (화면 좌측에선 1, 우측에선 -1)
    if enemy_x<=pad_width/2:
        enemy_z=1
    else:
        enemy_z=-1
    for i in range(3):
        enemy_xy[3].append([enemy_x, enemy_y, enemy_z])  #적 xy좌표 리스트 적3 리스트 부분에 생성할 새로운 적의 xy 좌표 리스트 추가
        enemy_x += enemy_z*(enemy_width+10) 
        enemy_y += -(enemy_height+5)    #맨 앞 적 뒤에 따라 나오는 적들 y값 (바로 앞의 적 y값) - (적 세로 높이+간격)으로 설정, 더 큰 음수로 설정하는 좌표상 더 위에 생성해야해서

#적3 구동 함수
def playEnemy3(enemy3_speed, time_now):
    global enemy3_count_0, elimit
    #현재 플레이 시간이 인자로 전달받은 적3의 다음 레벨로 넘어가는 기준값보다 크다면
    if time_now > nextLevel[3]:
        enemy_persentage[3]+=2 #적3 등장확률 증가
        nextLevel[3]+=20    #적3 다음 레벨로 넘어가는 기준값 증가
    #적 생성
    #if len(enemy_xy[3]) == 0:  #적 생성 후 생성한 적이 사라질때까지 새로운 시퀀스를 생성하지 않을시 이 코드 추가
    if random.randrange(0, 1000) < enemy_persentage[3]:  # 1~100 랜덤 돌려서 나온 숫자가 적3 퍼센테이지 값보다 높다면
        if elimit == False:
            createEnemy3()  #적3 생성 함수 실행
        else:
            pass

    for i, exy in enumerate(enemy_xy[3]):   #i: 현재 접근중인 인덱스값, exy: 현재 접근중인 적 좌표 리스트 [x,y]
        
        if exy[2]==1: #좌측에서 출발 시
            if exy[0]<pad_width/2: #화면 가운데까지 우측으로 이동
                exy[1] -= enemy3_speed/2
                exy[0] += enemy3_speed
            else: exy[2]=2
        elif exy[2]==2: #↗
            if exy[0]<3*pad_width/4:
                exy[1] -= enemy3_speed
                exy[0] += enemy3_speed
            else: exy[2]=3
        elif exy[2]==3: #↖
            if exy[0]>pad_width/2:
                exy[1] -= enemy3_speed
                exy[0] -= enemy3_speed
            else: exy[2]=4
        elif exy[2]==4: #↙
            if exy[0]>pad_width/4:
                exy[1] += enemy3_speed
                exy[0] -= enemy3_speed
            else: exy[2]=5
        elif exy[2]==5: #↘
            if exy[0]<pad_width/2:
                exy[1] += enemy3_speed
                exy[0] += enemy3_speed
            else: exy[2]=6
        elif exy[2]==6: #화면 우측 바깥으로 이동
            if exy[0]<pad_width-enemy_width:
                exy[1] += enemy3_speed/2
                exy[0] += enemy3_speed
            else:
                try:
                    enemy_xy[3].remove(exy) #적이 화면을 벗어났을경우 적3 리스트에서 제거
                except:
                    pass
        
        if exy[2]==-1: #우측에서 출발 시
            if exy[0]>pad_width/2: #화면 가운데까지 좌측으로 이동
                exy[1] -= enemy3_speed/2
                exy[0] -= enemy3_speed
            else: exy[2]=-2
        elif exy[2]==-2: #↖
            if exy[0]>pad_width/4:
                exy[1] -= enemy3_speed
                exy[0] -= enemy3_speed
            else: exy[2]=-3
        elif exy[2]==-3: #↗
            if exy[0]<pad_width/2:
                exy[1] -= enemy3_speed
                exy[0] += enemy3_speed
            else: exy[2]=-4
        elif exy[2]==-4: #↘
            if exy[0]<3*pad_width/4:
                exy[1] += enemy3_speed
                exy[0] += enemy3_speed
            else: exy[2]=-5
        elif exy[2]==-5: #↙
            if exy[0]>pad_width/2:
                exy[1] += enemy3_speed
                exy[0] -= enemy3_speed
            else: exy[2]=-6
        elif exy[2]==-6: #화면 좌측 바깥으로 이동
            if exy[0]>0:
                exy[1] += enemy3_speed/2
                exy[0] -= enemy3_speed
            else:
                try:
                    enemy_xy[3].remove(exy) #적이 화면을 벗어났을경우 적3 리스트에서 제거
                except:
                    pass
                
        #적이 화면을 벗어났을경우 적3 리스트에서 제거
        if exy[1] >= pad_height:
            try:
                enemy_xy[3].remove(exy)
            except:
                pass
        #적3 xy리스트의 요소가 0개가 아닐시 적3 그리기
        if len(enemy_xy[3]) != 0:
            drawObject(enemy3, exy[0], exy[1])
        elif time_now >= boss_time:
            enemy3_count_0 = True

# 적4 생성 함수
def createEnemy4():
    enemy_x = random.randrange(0, pad_width-enemy_width)    #적 위치 랜덤 x좌표로 지정
    enemy_y = 0 #적 y 지정
    enemy_z = 0 #적 방향 지정 (화면 좌측에선 1, 우측에선 -1)
    for i in range(1):
        enemy_xy[4].append([enemy_x, enemy_y, enemy_z])  #적 xy좌표 리스트 적4 리스트 부분에 생성할 새로운 적의 xy 좌표 리스트 추가
        enemy_y += -(enemy_height+5)    #맨 앞 적 뒤에 따라 나오는 적들 y값 (바로 앞의 적 y값) - (적 세로 높이+간격)으로 설정, 더 큰 음수로 설정하는 좌표상 더 위에 생성해야해서

#적4 구동 함수
def playEnemy4(enemy4_speed, time_now):
    global enemy4_count_0, elimit
    #현재 플레이 시간이 인자로 전달받은 적4의 다음 레벨로 넘어가는 기준값보다 크다면
    if time_now > nextLevel[4]:
        enemy_persentage[4]+=1 #적4 등장확률 증가
        nextLevel[4]+=20    #적4 다음 레벨로 넘어가는 기준값 증가
    #적 생성
    #if len(enemy_xy[4]) == 0:  #적 생성 후 생성한 적이 사라질때까지 새로운 시퀀스를 생성하지 않을시 이 코드 추가
    if random.randrange(0, 1000) < enemy_persentage[4]:  # 1~100 랜덤 돌려서 나온 숫자가 적4 퍼센테이지 값보다 높다면
        if elimit == False:
            createEnemy4()  #적0 생성 함수 실행
        else:
            pass

    for i, exy in enumerate(enemy_xy[4]):   #i: 현재 접근중인 인덱스값, exy: 현재 접근중인 적 좌표 리스트 [x,y]
        #적4 y좌표 변경
        #갤러리안과 떨어져 있다면 갤러리안의 x좌표를 향해 이동
        if y-exy[1]>pad_height/4:
            exy[1] += enemy4_speed #적4의 스피드만큼 y값 이동
            if exy[0]<x:
                exy[0] += enemy4_speed
            elif exy[0]>x:
                exy[0] -= enemy4_speed
            else: pass
        else:
            exy[1] += enemy4_speed*2 #돌진

        enemy_xy[4][i][1] = exy[1]  #전역변수 적 리스트에 변경된 y값 저장
                
        #적이 화면을 벗어났을경우 적4 리스트에서 제거
        if exy[1] >= pad_height or exy[0]<=0 or exy[0]>=pad_width-10:
            try:
                enemy_xy[4].remove(exy)
            except:
                pass
        #적4 xy리스트의 요소가 0개가 아닐시 적4 그리기
        if len(enemy_xy[4]) != 0:
            drawObject(enemy4, exy[0], exy[1])
        elif time_now >= boss_time:
            enemy4_count_0 = True

#적5 생성 함수
def createEnemy5():
    enemy_x = random.randrange(0, pad_width-enemy_width) # 적 위치 랜덤 x좌표로 지정
    enemy_y = pad_height*0.1 #적 y 지정
    enemy_z = -1
    enemy_t = 0
    enemy_xy[5].append([enemy_x, enemy_y, enemy_z, enemy_t])  #적 xy좌표 리스트 적5 리스트 부분에 생성할 새로운 적의 xy 좌표 리스트 추가

def playEnemy5(enemy5_speed, time_now):
    global enemy5_count_0, elimit
    #현재 플레이 시간이 인자로 전달받은 적5의 다음 레벨로 넘어가는 기준값보다 크다면
    if time_now > nextLevel[5]:
        enemy_persentage[5]+=0.5 #적5 등장확률 증가
        nextLevel[5]+=20 #적5 다음 레벨로 넘어가는 기준값 증가
    #적 생성
    #if len(enemy_xy[5]) == 0:  #적 생성 후 생성한 적이 사라질때까지 새로운 시퀀스를 생성하지 않을시 이 코드 추가
    if random.randrange(0, 1000) < enemy_persentage[5]:  # 1~100 랜덤 돌려서 나온 숫자가 적5 퍼센테이지 값보다 높다면
        if elimit == False:
            createEnemy5()
        else:
            pass

    for i, exy in enumerate(enemy_xy[5]):   #i: 현재 접근중인 인덱스값, exy: 현재 접근중인 적 좌표 리스트 [x,y]
        #적5 x값 변경
        if(pad_width-enemy_width <= exy[0] or 0 >= exy[0]):
            exy[2] *= -1
        exy[0] += enemy5_speed*exy[2]    
        exy[3] += 1
        if(exy[3]%150 == 0): #발사 딜레이를 위한 카운트
            enemy_xy[6].append([exy[0],exy[1]])

    
        #적5 xy리스트의 요소가 0개가 아닐시 적5 그리기
        if len(enemy_xy[5]) != 0:
            drawObject(enemy5, exy[0], exy[1])
        elif time_now >= boss_time:
            enemy5_count_0 = True



# 보스 구동 함수 (패턴 조정 역할)
def playboss():
    global boss, boss_hp, time_stamp, time_stamp2, enemy_xy, bp3
    bp3 = False
    boss_x = pad_width * 0.45       #보스의 x좌표
    boss_y = 50                     #보스의 y좌표
    enemy_xy[7].append([boss_x , boss_y]) #보스의 xy좌표 저장
    drawObject(boss , enemy_xy[7][0][0] , enemy_xy[7][0][1]) #보스 그리기
    bosspattern1()
    bosspattern2()
    bosspattern3()
    bosspattern4()



def bosspattern1():      #레이저 구동
    global enemy_xy, time_stamp1, laser_play, laser, pat1
    laser_x = random.randrange(0 , pad_width - laser_width)
    laser_y = 0
    if pat1 == False:
        time_stamp1 = time.time()
        #laser_x = random.randrange(0 , pad_width - laser_width)
        #laser_y = 0
        enemy_xy[8].append([laser_x, laser_y])
        pat1 = True
    if 1 < time.time() - time_stamp1 < 2:
        drawObject(pre_laser, enemy_xy[8][0][0], enemy_xy[8][0][1])
    if 2 <= time.time() - time_stamp1 <= 3:           #사전 경고 1초 후에 레이저 시작
        laser_play = True
        drawObject(laser , enemy_xy[8][0][0] , enemy_xy[8][0][1])
    if time.time() - time_stamp1 >= 3:            #2초동안 레이저 발사 후에 레이저 삭제
        laser_play = False
        enemy_xy[8].clear()
        pat1 = False

    
# 보스 패턴 2 (돌진 후 탄막 패턴)
def bosspattern2():
    global enemy_xy , boss, pat2, time_stamp, x, y, pad_height, boss_height, bp3
    boss_speed = 15
    if pat2 == False:
        time_stamp = time.time()
        pat2 = True
    if time.time() - time_stamp < 3:   #4초 동안 보스 x좌표가 갤러리안의 x좌표에 따라 움직임
        if enemy_xy[7][0][0] < x:
            enemy_xy[7][0][0] += boss_speed / 4    #뒤따라가는 식으로 구현하기 위해서 스피드 조절
        elif enemy_xy[7][0][0] > x:
            enemy_xy[7][0][0] -= boss_speed / 4
        else:
            enemy_xy[7][0][0] = x
    elif 3 <= (time.time() - time_stamp) < 4:      #4초동안 x좌표를 따라가서 3초동안 돌진
        enemy_xy[9].clear()
        if enemy_xy[7][0][1] >= pad_height - boss_height:
            enemy_xy[7][0][1] = pad_height - boss_height
        else:
            enemy_xy[7][0][1] += boss_speed * 3
        
    elif 4 <= (time.time() - time_stamp) <= 20:     #복귀 및 다음 패턴을 위한 딜레이
        if enemy_xy[7][0][1] > 50:
            enemy_xy[7][0][1] -= boss_speed/2
        else:
            enemy_xy[7][0][1] = 50
        if enemy_xy[7][0][0] < pad_width *0.45:
            enemy_xy[7][0][0] += boss_speed/4
        elif enemy_xy[7][0][0] > pad_width *0.45:
            enemy_xy[7][0][0] -= boss_speed/4
        else:
            enemy_xy[7][0][0] = pad_width *0.45
        if enemy_xy[7][0][0] == pad_width *0.45 and enemy_xy[7][0][1] == 50:
            bp3 = True
        else: 
            bp3 = False
    elif time.time() - time_stamp > 20:
        pat2 = False

    

# 보스 패턴 3 (벽에서 튕기는 탄막 난사)
def createbarrage():   #탄막 생성 함수
    global enemy_xy, time_stamp
    barrage_x = enemy_xy[7][0][0] + boss_width//2
    barrage_y = enemy_xy[7][0][1] + boss_height
    barrage_z = 0
    barrage_w = random.randrange(1, 10) #탄막 발사각 지정
    arrive_x = random.randrange(0 , pad_width)   #탄막이 좌로 갈지 우로 갈지 랜덤으로 정해줌
    
    if arrive_x <= barrage_x:
        barrage_z = 1
    else:
        barrage_z = -1
    for i in range(1):
        enemy_xy[9].append([barrage_x , barrage_y , barrage_z, barrage_w])
        #barrage_y += 30

def bosspattern3():    # 탄막 구동 함수
    global enemy_xy, barrage_radius, bp3, boss_bullet
    barrage_speed = 10        #탄막 속도
    barrage_radius = 15      #탄막 넓이(원의 넓이)

    if random.randrange(0 , 100) < 5 and bp3 == True:   #0부터 100까지 랜덤으로 돌린 수가 5보다 작을 때.
        createbarrage()                 #탄막 생성
    for i , bxy in enumerate(enemy_xy[9]):
        bxy[1] += barrage_speed    #탄막의 스피드만큼 y값 이동
        bxy[0] += ( bxy[3] - 1 ) * (barrage_speed / bxy[3]) * bxy[2] #지정 방향으로 x값 이동
        if bxy[0]<=0 or bxy[0]>=pad_width-10:
            bxy[2]*=-1                 #벽에 닿으면 방향 반전
        enemy_xy[9][i][1] = bxy[1]  #전역변수 탄막 리스트에 변경된 y값 저장

        #탄막이 화면을 벗어났을경우 리스트에서 제거
        if bxy[1] >= pad_height:
            try:
                enemy_xy[9].remove(bxy)
            except:
                pass
        if len(enemy_xy[9]) != 0:
            drawObject(boss_bullet, bxy[0], bxy[1])

# 보스 패턴 4 (화면 가리는 장막 설치) 
def bosspattern4():
    global curtain , boss_time, time_stamp2
    curtain_x = 0
    curtain_y = pad_height // 2
    enemy_xy[10].append([curtain_x , curtain_y])
    if int((time.time() - boss_time)) % 30 == 0 and (time.time() - boss_time) >= 30:     #30초마다 타임 스탬프 기록
        time_stamp2 = time.time()
    if (time.time() - time_stamp2) < 10:                           #10초동안 장막패턴 시전
        drawObject(curtain, enemy_xy[10][0][0], enemy_xy[10][0][1])
    if time.time() - time_stamp2 >= 10:
        enemy_xy[10].clear()



# 게임 실행 메인 함수
def runGame():
    global gamepad, fighter, clock, fPass, fCount, ongame, startTime
    global bullet, life, Restart
    global enemy_xy, enemy_persentage, nextLevel
    global x_change, y_change, x, y, bullet_xy
    global life_count, life_xy, item_speed, life_play
    global bullet_speed, bullet_quantity, bSpeed_xy, bQuantity_xy, bSpeed_play, bQuantity_play, iPersentage
    global boss, boss_play, boss_hp, boss_time
    global time_stamp, time_stamp1, time_stamp2, pat1, pat2, pat3, pat4, laser_play, elimit
    global count #격추한 수

    x = pad_width*0.45  #갤러리안의 X좌표(좌측)
    y = pad_height*0.9  #갤러리안의 Y좌표(상단)
    x_change = 0    #갤러리안의 x좌표 변화량
    y_change = 0    #갤러리안의 y좌표 변화량
    fPass = False   #무적 여부
    fCrash = 0  #적이랑 갤러리안이랑 부딪힌 시간
    fCount = 0  #무적시간 깜빡이는 프레임 조절용 카운트
    ebCrash = 0

    life_count = start_life #갤러리안 생명
    life_xy = [0, 0]   #생명 아이템 x,y 좌표 [x,y]
    life_play = False   #생명 아이템이 화면에 생성되었는지 여부

    bullet_xy = []  #미사일 xy 좌표
    bullet_speed = start_bSpeed #미사일 이동 속도
    bullet_quantity = start_bQuantity   #미사일 개수
    bSpeed_xy = [0, 0]  #미사일 속도 증가 아이템 xy 좌표
    bQuantity_xy = [0, 0]   #미사일 개수 증가 아이템 xy 좌표
    bSpeed_play = False #미사일 속도 증가 아이템이 화면에 생성되었는지 여부
    bQuantity_play = False  #미사일 개수 증가 아이템이 화면에 생성되었는지 여부

    item_speed = 2 #아이템 이동 속도
    iPersentage = 1  #미사일 속도, 개수 퍼센테이지 계산용, 초기값: 0.1%

    #적들 좌표, 속도, 확률, 다음레벨 리스트, 인덱스: 적0, 적1, 적2, 적3, 적4, 적5, 적5의 탄, 보스, 레이저, 탄막, 장막
    enemy_xy = [[], [], [], [], [], [], [], [], [], [], []] 
    enemy_speed = [5, 5, 5, 5, 5, 3] #적 스피드
    enemy_persentage = [5, 2, 2, 2, 2, 1]  #적 생성 확률 리스트
    nextLevel = [10, 10, 10, 10, 10, 10]    #적 생성 확률이 올라가는 다음번 시간 ex) 적n의 값이 60이라면 게임 시작 후 60초 후 적n 등장확률 올림

    #보스 관련 변수
    boss_hp = 300
    boss_play = False
    elimit = False
    time_stamp = 0
    time_stamp1 = 0
    time_stamp2 = 0
    pat1 = False
    pat2 = False
    pat3 = False
    pat4 = False
    laser_play = False
    boss_time = 120

    Stop = False    
    ongame = False
    onPause = False
    startTime = time.time()
    pauseTime = 0   # 일시정지 1회당 시간, 시작 시간에서 일시정지 되었던 시간만큼 추가하여 플레이 시간 관리

    ongame = start()# 시작화면 실행
    Restart = Restart + 1
    count = 0

    while not ongame:
        for event in pygame.event.get():    #키 이벤트 처리  
            if event.type == pygame.QUIT:   #화면 종료시
                pygame.quit()   #게임 종료
            #키가 눌렸을때
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if(Stop == False):
                        x_change -= 5
                    
                elif event.key == pygame.K_RIGHT:
                    if(Stop == False):    
                        x_change += 5

                elif event.key == pygame.K_UP:
                    if(Stop == False):
                        y_change -= 5

                elif event.key == pygame.K_DOWN:
                    if(Stop == False):
                        y_change += 5
                    
                elif event.key == pygame.K_SPACE:
                    if len(bullet_xy) < 100:    #미사일 xy좌표 저장값이 100개 이하라면
                        shot.play()
                        bullet_x = x + fight_width/2    #미사일의 x좌표를 갤러리안 이미지의 중앙으로 설정
                        bullet_y = y - fight_height     #미사일의 y좌표를 갤러리안의 y좌표로 설정
                        #미사일 개수에 따라 좌표 다르게 조정하여 미사일 개수대로 미사일 좌표 저장
                        match bullet_quantity:
                            case 1: bullet_xy.append([bullet_x, bullet_y])
                            case 2: bullet_xy.append([bullet_x-5, bullet_y]); bullet_xy.append([bullet_x+5, bullet_y])
                            case 3: bullet_xy.append([bullet_x, bullet_y]); bullet_xy.append([bullet_x-10, bullet_y]); bullet_xy.append([bullet_x+10, bullet_y])

                #ESC를 누르면 종료
                elif event.key == pygame.K_ESCAPE:
                    ongame = True

                #엔터를 누를시 게임 일시정지/해제
                elif event.key == pygame.K_RETURN:
                    if onPause == True:
                        pauseTime = time.time() - pauseTime
                        startTime += pauseTime
                        onPause = False
                    else :
                        dispMessage('Pause!')
                        pauseTime = time.time()
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

        #적 및 보스 구동 (현재 시각 - 시작시각이 보스 등장 시간보다 작을 때 적 소환, 클 때 보스 소환)
        if time.time()-startTime >= boss_time:
            elimit = True
            if(not enemy_xy[0] and not enemy_xy[1] and not enemy_xy[2] and not enemy_xy[3] and not enemy_xy[4] and not enemy_xy[5] and not enemy_xy[6]):
                boss_play = True
            
        if boss_play == True:
            playboss()    #보스 패턴 시작
        else:
            #적0 구동 (적0 스피드, 플레이타임(현재시각-시작시간))
            playEnemy0(enemy_speed[0], time.time()-startTime)

            #적1 구동 (적1 스피드, 플레이타임(현재시각-시작시간))
            playEnemy1(enemy_speed[1], time.time()-startTime)

            #적2 구동 (적2 스피드, 플레이타임(현재시각-시작시간))
            playEnemy2(enemy_speed[2], time.time()-startTime)
            
            #적3 구동 (적3 스피드, 플레이타임(현재시각-시작시간))
            playEnemy3(enemy_speed[3], time.time()-startTime)
        
            #적4 구동 (적4 스피드, 플레이타임(현재시각-시작시간))
            playEnemy4(enemy_speed[4], time.time()-startTime)
                
            #적5 구동 (적5 스피드, 플레이타임(현재시각-시작시간))
            playEnemy5(enemy_speed[5], time.time()-startTime)

        #적5 미사일 구동
        enemyBullit()

        #생명 아이템 구동
        if life_play == True:   #생명 아이템 실행여부가 참이라면
            playLifeItem()  #생명 아이템 구동

        #미사일 속도 아이템 구동
        if bSpeed_play == True: #속도 아이템 실행여부가 참이라면
            playSpeedItem() #속도 아이템 구동

        #미사일 개수 아이템 구동
        if bQuantity_play == True: #개수 아이템 실행여부가 참이라면
            playQuantityItem() #개수 아이템 구동
        
        #아이템 퍼센테이지 변화
        #미사일 속도 아이템은 확률*2
        match time.time()-startTime:
            case 20: iPersentage = 1  #게임 시작 20초 후에 0.5%
            case 40: iPersentage = 2  #게임 시작 40초 후에 1%
            case 60: iPersentage = 3  #게임 시작 60초 후에 1.5%
            case 80: iPersentage = 2  #게임 시작 80초 후에 1%
            case 100: iPersentage = 1  #게임 시작 100초 후에 0.5%
            case 120: iPersentage = 0  #게임 시작 120초 후에 0%

        #충돌 처리
        for i, eList in enumerate(enemy_xy):    #적 전체 xy 리스트에서 적0~3 xy 리스트 하나씩 가져오기, enumerate 설명은 97줄 참고
            for j, exy in enumerate(eList): #적n의 리스트에서 xy좌표 리스트 가져오기, exy:[적x,적y]
                #갤러리안이 적과 충돌했는지 체크
                if time.time()-fCrash > 1:  #갤러리안이 적이랑 충돌 후 1초가 지났다면 충돌 처리 진행
                    fPass = False   #무적시간 여부 거짓
                    if i == 10:
                        pass
                    else:
                        if i <= 6:
                            if exy[1] < y < exy[1] + enemy_height :
                                #적이 전투기에 접근하면
                                if ((y+1 < exy[1] < y + fight_height)-1 or (y+1 < exy[1] + enemy_height < y + fight_height-1)) and\
                                ((x+1 < exy[0] < x + fight_width-1) or (x+1 < exy[0] + enemy_width < x + fight_width-1)):
                                    try:   
                                        eList.remove(exy) #적 제거
                                    except:
                                        pass
                                    if(i == 6):
                                        ebCrash = time.time()
                                        Stop = True
                                    else:    
                                        fCrash = time.time()
                                        crash_sound.play()
                                        fPass = True    #무적시간 여부 참
                                        if life_count == 1:
                                            life_count -= 1
                                            ongame = True
                                        else:
                                            life_count -= 1
                        if i == 7:
                            if exy[1] < y < exy[1] + boss_height:
                                #보스가 전투기에 접근하면
                                if ((y+1 < exy[1] < y + fight_height)-1 or (y+1 < exy[1] + boss_height < y + fight_height-1)) and\
                                ((x+1 < exy[0] < x + fight_width-1) or (x+1 < exy[0] + boss_width//2 < x + fight_width-1)):
                                    fCrash = time.time()
                                    crash_sound.play()
                                    fPass = True
                                    if life_count == 1:
                                        life_count -= 1
                                        ongame = True
                                    else:
                                        life_count -= 1
                        if i == 8:
                            if laser_play == True:
                                if ((y+1 < exy[1] < y + fight_height)-1 or (y+1 < exy[1] + laser_height < y + fight_height-1)) and\
                                ((x+1 < exy[0] < x + fight_width-1) or (x+1 < exy[0] + laser_width < x + fight_width-1)):
                                    fCrash = time.time()
                                    crash_sound.play()
                                    fPass = True
                                    if life_count == 1:
                                        life_count -= 1
                                        ongame = True
                                    else:
                                        life_count -= 1
                        if i == 9:
                            if ((y+1 < exy[1] < y + fight_height) and (x+1 < exy[0] < x + fight_width-1)):
                                    fCrash = time.time()
                                    crash_sound.play()
                                    fPass = True
                                    if life_count == 1:
                                        life_count -= 1
                                        ongame = True
                                    else:
                                        life_count -= 1

                #미사일이 적과 충돌했는지 체크
                for k, bxy in enumerate(bullet_xy): #미사일 xy리스트에서 좌표 하나씩 가져오기, bxy:[미사일x,미사일y]
                    #미사일과 적이 충돌시 미사일 제거 // 보스와 충돌시 보스 체력 -1씩 감소
                    if i <= 6:
                        if ((exy[1]+1 < bxy[1] < exy[1] + enemy_width-1) or (exy[1]+1 < bxy[1]+bullet_width < exy[1] + enemy_width-1))and\
                            ((exy[0]+1 < bxy[0] < exy[0] + enemy_width-1) or (exy[0]+1 < bxy[0]+bullet_width < exy[0] + enemy_width-1))and\
                                (i != 6):
                            try:
                                eList.remove(exy) #적 제거
                                bullet_xy.remove(bxy)   #미사일 제거

                                #보스 타격시에는 아이템이 나오지 않게 조건 설정해야함
                                if boss_play == False:
                                    #생명 아이템 생성 (생명 아이템이 생성되지 않았을 때, 생명이 3개 미만일때, 확률 1%)
                                    if life_play == False and life_count < 3 and random.randrange(0, 200) < iPersentage:
                                        life_play = True    #생명 아이템 실행중으로 전환
                                        createLifeItem()    #생명아이템 생성
                                    #밑에다가 elif 문으로 다른 아이템 생성도 구현
                                    #미사일 속도 아이템 생성 (미사일 속도 아이템이 생성되지 않았을 때, 미사일 속도가 25 미만일때, 확률 1/iPersentage*100%)
                                    if bSpeed_play == False and bullet_speed < 25 and random.randrange(0, 200) < iPersentage:
                                        bSpeed_play = True  #미사일 속도 아이템 실행중으로 전환
                                        createSpeedItem()   #미사일 속도 아이템 생성
                                    #미사일 개수 아이템 생성 (미사일 개수 아이템이 생성되지 않았을 때, 미사일 개수 3개 미만일때, 확률 1/iPersentage*100%)
                                    elif bQuantity_play == False and bullet_quantity < 3 and random.randrange(0, 200) < iPersentage:
                                        bQuantity_play = True  #미사일 개수 아이템 실행중으로 전환
                                        createQuantityItem()   #미사일 개수 아이템 생성
                                else:
                                    life_play = False
                                    bSpeed_play = False
                                    bQuantity_play = False
                            except:
                                pass
                            count += scoreList[i]   #현재 접근중인 적의 타입에 따라 알맞은 점수를 추가
                    elif i == 7:
                        if ((exy[1]+1 < bxy[1] < exy[1] + boss_width-1) or (exy[1]+1 < bxy[1]+bullet_width < exy[1] + boss_width-1))and\
                            ((exy[0]+1 < bxy[0] < exy[0] + boss_width-1) or (exy[0]+1 < bxy[0]+bullet_width < exy[0] + boss_width-1)):
                            try:
                                boss_hp -= 1
                                bullet_xy.remove(bxy)
                                if boss_hp <= 0:
                                    ongame = True
                            except:
                                pass
                    else:
                        pass

        drawLife(life_count)
        drawScore(count)
        drawTime(time.time()-startTime)
        if time.time() - ebCrash > 3:
            Stop = False
        pygame.display.update() #화면 전체 업데이트
        if(ongame):
            break
        clock.tick(60)  #프레임 초당 60fps 설정
    if boss_hp <= 0:
        count += scoreList[6]
        clear(count, time.time()-startTime)
    else:
        crash(count)

#초기 설정
def initGame():
    global gamepad, clock
    global bullet, fighter, life, lifeItem, bSpeedItem, bQuantityItem
    global enemy0, enemy1,enemy2,enemy3,enemy4, enemybullet, enemy5
    global crash_sound, game_over, shot, heart_up, quantity_up, speed_up, game_clear
    global boss, laser, pre_laser, curtain, boss_bullet
    
    pygame.init()   #파이게임 라이브러리 초기화
    gamepad = pygame.display.set_mode((pad_width, pad_height))  #화면 크기 설정 및 생성
    pygame.display.set_caption('MyGalaga')  #게임 창 제목 설정
    crash_sound = pygame.mixer.Sound(sound_path+"ost_003_Flag_Appears.mp3") #피격 사운드
    game_over = pygame.mixer.Sound(sound_path+"ost_004_Alien_Flying.mp3") #게임 오버 사운드
    game_clear = pygame.mixer.Sound(sound_path+"ost_016_Imperfect_Result_in_the_Challenging_Stage.mp3") #게임 오버 사운드
    shot = pygame.mixer.Sound(sound_path+"ost_005_Shot.mp3") #발사 사운드
    heart_up = pygame.mixer.Sound(sound_path+"ost_008_Hit_on_Boss_(1).mp3") #체력 회복 사운드
    quantity_up = pygame.mixer.Sound(sound_path+"ost_015_Challenging_Stage_Start.mp3") #미사일 개수 증가 사운드
    speed_up = pygame.mixer.Sound(sound_path+"ost_018_Extend.mp3") #스피드 증가 사운드

    enemybullet = pygame.image.load(img_path+'enemybullet.png')  #적5 미사일 이미지 설정
    enemy5 = pygame.image.load(img_path+'enemy5.png')    #적5 이미지 설정
    fighter = pygame.image.load(img_path+'fighter.png')    #갤러리안 이미지 설정
    life = pygame.image.load(img_path+'life.png') #생명 이미지 설정
    lifeItem = pygame.image.load(img_path+'lifeitem.png') #생명 아이템 이미지 설정
    enemy0 = pygame.image.load(img_path+'enemy0.png')    #적0 이미지 설정
    enemy1 = pygame.image.load(img_path+'enemy1.png')    #적1 이미지 설정
    enemy2 = pygame.image.load(img_path+'enemy2.png')    #적2 이미지 설정
    enemy3 = pygame.image.load(img_path+'enemy3.png')    #적3 이미지 설정
    enemy4 = pygame.image.load(img_path+'enemy4.png')    #적4 이미지 설정
    bullet = pygame.image.load(img_path+'bullet.png')  #미사일 이미지 설정
    bSpeedItem = pygame.image.load(img_path+'speed.png')  #미사일 속도 아이템 이미지 설정
    bQuantityItem = pygame.image.load(img_path+'quantity.png')  #미사일 수량 아이템 이미지 설정

    boss = pygame.image.load(img_path+'boss.png') #보스 이미지 설정 (추가 해야됨)
    pre_laser = pygame.image.load(img_path+'pre_laser.png') #사전 레이저 이미지 설정 
    laser = pygame.image.load(img_path+'laser.png') #레이저 이미지 설정 
    boss_bullet = pygame.image.load(img_path+'boss_bullet.png') #보스 탄막 이미지
    curtain = pygame.image.load(img_path+'curtain.png') #장막 이미지

    clock = pygame.time.Clock()   #파이게임 시계 가져오기


initGame()  #게임 초기 설정 실행
runGame()   #게임 실행