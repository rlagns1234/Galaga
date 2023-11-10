from PIL import Image

#이미지 확장자, 크기 조정 프로그램
im = Image.open('Image\\forward.png') #수정할 이미지 경로
print(im.size)  #수정할 이미지의 크기 출력

# Thumbnail 이미지 생성
size = (18, 18) #조정할 이미지 크기
im.thumbnail(size)  #설정한 크기의 새로운 이미지 생성

im.save('Image\\speed.png') #새로운 이미지 경로/이름 설정 및 저장
