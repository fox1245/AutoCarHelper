import cv2
import os
import glob
from pathlib import Path
from tkinter import *





def setPoint(path):
        # 이미지 파일 리스트
    file_list = os.listdir(path)
    file_list.sort()
    
    print(f"총 {len(file_list)}장의 이미지가 준비되었습니다.")
    os.makedirs(f'{path}/output', exist_ok=True)
    # 라벨링 루프
    for file in file_list:
        if file.endswith(f'.jpg'):
            print(file)
            destination = f'{path}/output'
            
            file_ = f'{path}/{file}'
            print(destination)
            label_image(file_ , destination)


def label_image(file_path, destination):
    img = cv2.imread(file_path)
    if img is None:
        print(f"이미지 로드 실패: {file_path}")
        return

    window_name = "Click to label X (r: reset, esc: skip)"
    temp_img = img.copy()
    temp_img2 = temp_img.copy()
    backup = img.copy()
    clicked = [False]  # 리스트로 감싸서 콜백에서 수정 가능

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"클릭한 x좌표: {x}")
            cv2.circle(temp_img, (x, y), 5, (0, 255, 0), -1)

            file_name = os.path.basename(file_path)
            new_name = f"{x}_{y}_{file_name}"
            #save_path = os.path.join(destination, new_name)
            save_path = f'{destination}/{new_name}'
            #cv2.imwrite(save_path, temp_img) #초록 원 찍힌채로 저장
            cv2.imwrite(save_path, backup) #그냥 사진으로 저장
            
            print(f"저장 완료: {save_path}")
            clicked[0] = True  # 클릭 플래그 설정
    while True:
        temp_img = img.copy()
        
        cv2.putText(temp_img2, "ESC for next, R for reset", (10,10), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,0,0), 2,cv2.LINE_8)
        cv2.imshow(window_name, temp_img2)
        cv2.setMouseCallback(window_name, click_event); 
        #cv2.imshow(window_name, temp_img2)
        #cv2.setMouseCallback(window_name, click_event)
        
        key = cv2.waitKey(0) & 0xFF
        
       
        if key == 27:
            print("이미지 건너뜀 (ESC)")
            break
        
        if key == ord('r'):
            print("이미지 reset (r)")
            temp_img = backup
            clicked[0] = False
                
        elif clicked[0] == True:
            break
            
    cv2.destroyAllWindows()
        







def SaveFrame(path, ex = 'mp4', skip_unit = 1, resizeParam = (300,300)):
    video_path = f'{path}'      #영상 파일 받은거
    output_folder = './frames_output'       #영상 파일 있는 폴더
    os.makedirs(f'{path}/{output_folder}', exist_ok=True)
    skip_count = int(skip_unit)
    print('skip_count' + str(skip_count))

    for file in os.listdir(path):
        if file.endswith(f'.{ex}'): 
            print(str(file) + " 찾음")   
            cap = cv2.VideoCapture(f'{path}/{file}')
            frame_count = 1
            saved_count = 0
            os.makedirs(f'{path}/{output_folder}/{file}_editted_', exist_ok=True)
            
            while cap.isOpened():
                #print("현재 프레임 카운트" +  str(frame_count))
                ret, frame = cap.read()
                if not ret:
                    break
                
                
                if frame_count % skip_count == 0:
                    frame = cv2.resize(frame, resizeParam)

                    filename = f'{path}/{output_folder}/{file}_editted_/frame_{saved_count:04d}.jpg' #frame_0000형태로 저장
                    cv2.imwrite(filename, frame)
                    saved_count += 1

                #frame_count += 10
                frame_count += 1

            cap.release()
            print(f"총 {saved_count}장의 이미지를 저장했습니다.")
    return f'{path}/{output_folder}'
            
            
def starter1():
    param1 = str(id_ent.get())
    param2 = str(ext_ent.get())
    param3 = str(skip_ent.get())
    vertical = str(vertical_ent.get())
    horizontal = str(horizontal_ent.get())
    param4 = ( int(horizontal),int(vertical))
    
    print(param1)
    starter2(param1, param2, param3, param4)
    
            
def starter2(mp4path, ext = "mp4", skip_unit = 1, resizeParams = (300, 300)):
    #ext = "mp4"
    workPath = SaveFrame(mp4path, ext, skip_unit, resizeParams)
    print("통과")
    print("현재 경로" + mp4path)
    entries =  os.listdir(workPath)
    print("현재 작업할 디렉토리들을 표시합니다" + str(entries))
    for subdir in entries:
        print(subdir)
        setPoint(f'{workPath}/{subdir}')
        
            
            
root = Tk()
root.title("AutoCar Helper")
root.geometry("400x200")
root.resizable(True, True)

#label = Label(root, text = "오토카의 좌표를 찍어주는 자동화 도구")

id_lbl = Label(root, text = '경로' , width = 10)
id_lbl.grid(row = 0, column = 0)
id_ent = Entry(root, width = 20)
id_ent.grid(row = 0, column = 1)


ext_lbl = Label(root, text = "확장자", width = 10)
ext_lbl.grid(row = 1, column = 0)
ext_ent = Entry(root, width = 20)
ext_ent.grid(row = 1, column = 1)

skip_lbl = Label(root, text = "프레임 스킵", width = 10)
skip_lbl.grid(row = 2, column = 0)
skip_ent = Entry(root, width = 20)
skip_ent.grid(row = 2, column = 1)

horizontal_lbl = Label(root, text = "가로", width = 10)
horizontal_lbl.grid(row = 3, column = 0)
horizontal_ent = Entry(root, width = 20)
horizontal_ent.grid(row = 3, column = 1)


vertical_lbl = Label(root, text = "세로", width = 10)
vertical_lbl.grid(row = 4, column = 0)
vertical_ent = Entry(root, width = 20)
vertical_ent.grid(row = 4, column = 1)



btn = Button(root, text = '확인', width = 6, height = 6, command = starter1)
btn.grid(row = 0, column = 2, rowspan = 5)
 



root.mainloop()   
            







#setPoint("D:/Coding/20250509/_editted_/dataset_mp4/frames_output/dataset_rgb.mp4_editted_")
