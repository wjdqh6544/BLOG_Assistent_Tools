from PIL import Image
import os
import sys
import time

def main():
    print("*" * 76)
    print("\nSelect the action You want.\n")
    print("1. Convert to .webp | 2. Image Optimization | 3. Insert Watermark | 4. Exit\n")
    print("*" * 76)
    select = input("Select: ")

    if (select == "1"):
        Convert()
    elif (select == "2"):
        Optimization()
    elif (select == "3"):
        Watermark()
    elif (select == "4"):
        print("\n\nShutting down...\n")
        time.sleep(1)
        sys.exit(0)
    else:
        print("\n*** Check your input value out whether the value is correct. ***\n\n")
        time.sleep(1)
        os.system('cls')
        main()
            
def getimglist(): # 실행 디렉토리에 있는 이미지 파일 (jpg, png) 이름을 목록으로 저장함.
    try:
        print("\nGetting image list...")
        list = os.listdir(os.getcwd()) # os.listdir -> 디렉토리에 위치한 모든 파일과 폴더를 목록으로 반환 / os.getcwd -> 현재 디렉토리의 절대경로를 반환
        img = []
        for i in list: # listdir 로 추출한 파일/폴더 목록에서 jpg 와 png 파일만 추출 (JPG / PNG 이외 파일들을 걸러냄)
            if (i[-4:].lower() == ".jpg"):
                img.append(i)
            elif (i[-4:].lower() == ".png"):
                img.append(i)
            else:
                pass
        time.sleep(0.3)
        print("Getting Completed!\n")
        time.sleep(0.5)
        return img
    except FileNotFoundError as e:
        print(" - ERROR: Image not found")
        time.sleep(1)
        input("\n\nPress Enter Key to Return Main...\n\n\n")
        os.system('cls')
        main()
    
def createFolder(directory): # 작업 (변환, 최적화, 워터마크) 결과물을 모아두는 폴더를 생성함. (폴더명: directory 매개변수를 통해 받아옴.)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print (' - ERROR: Creating directory - ' + directory)
        time.sleep(1)
        input("\n\nPress Enter Key to Return Main...\n\n\n")
        os.system('cls')
        main()
        
def Convert(): # 이미지 포맷 변환 (JPG/PNG -> webp)
    print("\n\n→  Convert image format to .webp")
    time.sleep(1)
    img = getimglist()
    success_cnt = pass_cnt = fail_cnt = status_convertedfile = 0
    total_cnt = len(img)
    print("Strat Converting...\n")
    print("-"*70)
    time.sleep(0.5)
    createFolder("00_convert-output")
    tmp = 1
    while tmp != 0:
        try:
            tmp_img_list = {}
            if (img[0][-4:].lower() == ".jpg"): # JPG 파일 작업 단계: jpg -> tmp.png -> png to webp -> tmp.png 삭제
                tmp_img = Image.open(img[0]).convert('RGB') # jpg 파일은 RGBA 로 변환될 수 없으므로, jpg 파일을 우선 png 파일로 변환함. (목적: png 이미지의 알파 채널 값 보존)
                tmp_img.save("tmp.png", "png") # 어차피 작업은 각 파일별로 이루어지므로, 변환하려는 jpg 파일을 tmp.png 로 저장해도 무방함.
                tmp_img_list["jpg"] = "tmp.png"
            else:
                tmp_img_list["png"] = img[0]
            image = Image.open(list(tmp_img_list.values())[0]).convert("RGBA") # png 이미지에 존재할 수 있는 알파 채널 값을 보존하기 위함.
            status = do_convert(img, image)
            if (status == 1): # 이미지 변환 후 1을 반환하였을 때 (덮어쓰지 않고 PASS)
                pass_cnt += 1
                status_convertedfile = success_cnt + pass_cnt + fail_cnt
                img.remove(img[0]) # img 리스트에서 작업한 파일을 삭제 (변환이 완료되었으므로)
                print("PASS... %d / %d" % (status_convertedfile, total_cnt)) # len(img) 를 사용하면, 그 수가 유동적으로 바뀜. (작업 완료 시 len(img)값이 변함.)
            elif (status == 0): # 이미지 변환 후 0을 반환하였을 때 (덮어씀)
                success_cnt += 1
                status_convertedfile = success_cnt + pass_cnt + fail_cnt
                img.remove(img[0])
                print("Converting... %d / %d" % (status_convertedfile, total_cnt))
            elif (status == 2): # 이미지 반환 후 2를 반환하였을 때 (덮어쓰기 여부를 선택할 때, 사용자가 잘못된 입력값을 제시함.)
                pass # img 리스트에 변화가 없으므로, while 문에 의해 다음 차례의 작업 또한 동일한 파일을 대상으로 함.
        except:
            print("ERROR: Cannot Convert to .webp | FileName: " + img[0])
            fail_cnt += 1 
            status_convertedfile = success_cnt + pass_cnt + fail_cnt
            img.remove(img[0])
        tmp = len(img) # 이미지 변환 후 img 리스트에 남아 있는 이미지 개수를 확인
        if (os.path.exists("tmp.png")): # 작업에 사용된 tmp.png 가 존재하는 경우, 삭제함.
            os.remove("tmp.png")
    print("_"*70)
    time.sleep(0.3)
    print("\nConverting Completed! | total: %d, success: %d, pass: %d, failure: %d" % (total_cnt, success_cnt, pass_cnt, fail_cnt))
    time.sleep(1)
    input("\n\nPress Enter Key to Return Main...\n\n\n")
    os.system('cls')
    main()

def do_convert(img, image): # 이미지 (JPG/PNG) 파일을 webp 형식으로 변환함.
    if(os.path.exists(os.getcwd() + "/00_convert-output/" + img[0][:-4] + ".webp")): # 작업 결과물을 저장하는 디렉토리에, 현재 작업하는 이미지와 동일한 이름의 이미지가 있는 경우.
        print("\n ** A file with the same name exists. Do you Overwrite it? (Y/N)\n")
        print("    - File Name: %s\n"%(img[0][:-4] + ".webp"))
        select = input("    Select: ")
        print()
        if (select.lower() == "y"): # 덮어쓰기
            image.save("00_convert-output/" + img[0][:-4] + ".webp", "webp") # 동일한 파일 이름으로, 파일 포맷만 webp 로 변환하여 저장함.
            return 0
        elif (select.lower() == "yes"): # 덮어쓰기
            image.save("00_convert-output/" + img[0][:-4] + ".webp", "webp")
            return 0
        elif (select.lower() == "n"): # 덮어쓰지 않기 (PASS)
            pass
            return 1
        elif (select.lower() == "no"): # 덮어쓰지 않기 (PASS)
            pass
            return 1
        else: # yes/y/no/n 이외의 값을 입력받았을 때
            print("\n*** Check your input value out whether the value is correct. ***\n")
            time.sleep(0.5)
            return 2
    else: # 이미지 이름에 중복이 없는 경우.
        image.save("00_convert-output/"+img[0][:-4]+".webp", "webp")
        return 0

def Optimization(): # 이미지 최적화 (용량 줄이기)
    print("\n\n→  Optimization image\n")
    time.sleep(1)
    while True:
        try: # 이미지 퀄리티 입력
            quality = int(input("Enter Image Quality (Unit: %, 0 ~ 100): "))
            if ( 0 <= quality <= 100):
                break
            break
        except:
            print("\n*** Check your input value out whether the value is correct. ***\n")
            time.sleep(0.5)
    img = getimglist()
    success_cnt = pass_cnt = fail_cnt = status_optimizedfile = 0
    total_cnt = len(img)
    print("Start Optimizing...\n")
    print("-"*70)
    time.sleep(0.5)
    createFolder("00_optimizing-output")
    tmp = 1
    while tmp != 0:
        try:
            image = Image.open(img[0])
            status = do_optimization(img, image, quality)
            if (status == 1):
                pass_cnt += 1
                status_optimizedfile = success_cnt + pass_cnt + fail_cnt
                img.remove(img[0])
                print("PASS... %d / %d" % (status_optimizedfile, total_cnt))
            elif (status == 0):
                success_cnt += 1
                status_optimizedfile = success_cnt + pass_cnt + fail_cnt
                img.remove(img[0])
                print("Optimizing... %d / %d" % (status_optimizedfile, total_cnt))
            elif (status == 2):
                img.insert(1, img[0])
        except:
            print("ERROR: Cannot Optimize images | FileName: " + img[0])
            fail_cnt += 1
            status_optimizedfile = success_cnt + pass_cnt + fail_cnt
            img.remove(img[0])
        tmp = len(img)
    print("_"*70)
    time.sleep(0.3)
    print("\nOptimizaation Completed! | total: %d, success: %d, pass: %d, failure: %d" % (total_cnt, success_cnt, pass_cnt, fail_cnt))
    time.sleep(1)
    input("\n\nPress Enter Key to Return Main...\n\n\n")
    os.system('cls')
    main()

def do_optimization(img, image, quality): # 이미지를 최적화하여 저장하는 함수
    if(os.path.exists(os.getcwd() + "/00_optimizing-output/" + img[0])):
        print("\n ** A file with the same name exists. Do you Overwrite it? (Y/N)\n")
        print("    - File Name: %s\n"%(img[0]))
        select = input("    Select: ")
        print()
        if (select.lower() == "y"):
            image.save("00_optimizing-output/" + img[0], quality=quality)
            return 0
        elif (select.lower() == "yes"):
            image.save("00_optimizing-output/" + img[0], quality=quality)
            return 0
        elif (select.lower() == "n"):
            pass
            return 1
        elif (select.lower() == "no"):
            pass
            return 1
        else:
            print("\n*** Check your input value out whether the value is correct. ***\n")
            time.sleep(0.5)
            return 2
    else:
        image.save("00_optimizing-output/" + img[0], quality=quality)
        return 0

def Watermark(): # 이미지에 워터마크 추가
    print("\n\n→  Insert Watermark\n")
    time.sleep(1)
    while True:
        try: # 워터마크 불투명도 입력
            opacity = int(input("Enter Watermark opacity (Unit: %, 0 ~ 100): "))
            if ( 0 <= opacity <= 100):
                break
            else:
                print("\n*** Check your input value out whether the value is correct. ***\n")
                time.sleep(0.5)
        except:
            print("\n*** Check your input value out whether the value is correct. ***\n")
            time.sleep(0.5)
    while True:
        try: # 워터마크 이미지 파일 이름 입력
            watermark_img_name = input("Enter Watermark Image Name (In the same directory & ONLY PNG Format): ")
            if (watermark_img_name[:-4] == ".png"): #확장자까지 입력한 경우 -> pass
                break
            else: # 확장자 입력 안한 경우 -> 자동 확장자 추가
                watermark_img_name += ".png" 
                break
        except:
            print("\n*** Check your input value out whether the value is correct. ***\n")
            time.sleep(0.5)
    try:
        Watermark_img_origin = Image.open(watermark_img_name).convert("RGBA")
    except: # 워터마크 이미지 찾을 수 없는 경우
        time.sleep(1)
        print("\n\n - ERROR: Watermark Image doesn't exist.")
        print("\n*** Check the watermark name out whether the name is correct and the image is in same directory. ***")
        input("\n\nPress Enter Key to Return Main...\n\n\n")
        os.system('cls')
        Watermark()
    img = getimglist()
    img.remove(watermark_img_name) # img 리스트는 디렉토리의 모든 이미지를 목록에 추가하므로, 목록에서 워터마크 이미지는 제외하여야 함.
    total_cnt = len(img)
    success_cnt = pass_cnt = fail_cnt = status_insertfile = 0
    print("Start Inserting Watermark...")
    print("-"*70)
    time.sleep(0.5)
    createFolder("00_watermark-output")
    opacity = round((opacity/100) * 255) # pillow 라이브러리에서 불투명도를 0~255 사이의 값으로 받으므로, 입력받은 % 에 대응하도록 값을 변환.
    tmp = 1
    while tmp != 0:
        try:
            tmp_img_list = {}
            if (img[0][-4:].lower() == ".jpg"): # JPG 파일 작업 단계: jpg -> tmp.png -> png to webp -> tmp.png 삭제
                tmp_img = Image.open(img[0]).convert('RGB') # jpg 파일은 RGBA 로 변환될 수 없으므로, jpg 파일을 우선 png 파일로 변환함. (목적: png 이미지의 알파 채널 값 보존)
                tmp_img.save("tmp.png", "png") # 어차피 작업은 각 파일별로 이루어지므로, 변환하려는 jpg 파일을 tmp.png 로 저장해도 무방함.
                tmp_img_list["jpg"] = "tmp.png"
            else:
                tmp_img_list["png"] = img[0]
            image = Image.open(list(tmp_img_list.values())[0]).convert("RGB") # 원본 이미지를 RGB 로 변환. (RGBA 변환 시 삽입한 워터마크가 검게 변하는 문제 발생)
            Watermark_img = editWatermark(image, Watermark_img_origin, opacity) # 워터마크 이미지 수정 (크기, 투명도 조작)
            position = (round(image.width * 0.95 - Watermark_img.width), round(image.height * 0.95 - Watermark_img.height)) # 워터마크 이미지 삽입 위치 설정 (우측 하단)
            status = do_watermark(img, image, Watermark_img, position) # 이미지 삽입
            if (status == 1):
                pass_cnt += 1
                status_insertfile = success_cnt + pass_cnt + fail_cnt
                img.remove(img[0])
                print("PASS... %d / %d" % (status_insertfile, total_cnt))
            elif (status == 0):
                success_cnt += 1
                status_insertfile = success_cnt + pass_cnt + fail_cnt
                if (list(tmp_img_list.keys())[0] == "jpg"): # 원본이 jpg 파일인 경우, 최종 결과물을 png 에서 jpg 로 변환
                    tmp_img = Image.open(os.getcwd() + "/00_watermark-output/" + img[0][:-4] + ".png").convert("RGB")
                    os.remove("00_watermark-output/" + img[0][:-4] + ".png")
                    tmp_img.save("00_watermark-output/" + img[0])
                img.remove(img[0])
                print("Inserting Watermark... %d / %d" % (status_insertfile, total_cnt))
            elif (status == 2):
                img.insert(1, img[0])
        except:
            print("ERROR: Cannot Insert Watermark | FileName: " + img[0])
            fail_cnt += 1
            status_insertfile = success_cnt + pass_cnt + fail_cnt
            img.remove(img[0])
        tmp = len(img)
        if (os.path.exists("tmp.png")):
            os.remove("tmp.png")
    print("_"*70)
    time.sleep(0.3)
    print("\nInserting Watermark Completed! | total: %d, success: %d, pass: %d, failure: %d" % (total_cnt, success_cnt, pass_cnt, fail_cnt))
    time.sleep(1)
    input("\n\nPress Enter Key to Return Main...\n\n\n")
    os.system('cls')
    main()

def do_watermark(img, image, Watermark_img, position): # 이미지에 워터마크를 삽입하는 함수
    if(os.path.exists(os.getcwd() + "/00_watermark-output/" + img[0])):
        print("\n ** A file with the same name exists. Do you Overwrite it? (Y/N)\n")
        print("    - File Name: %s\n"%(img[0]))
        select = input("    Select: ")
        print()
        if (select.lower() == "y"):
            image.paste(Watermark_img, position, Watermark_img) # jpg 는 RGBA 를 저장할 수 없어, 우선 png 로 이미지 파일 추출. (이후 png -> jpg 변환)
            image.save("00_watermark-output/" + img[0][:-4] + ".png", "png")
            return 0
        elif (select.lower() == "yes"):
            image.paste(Watermark_img, position, Watermark_img)
            image.save("00_watermark-output/" + img[0][:-4] + ".png", "png")
            return 0
        elif (select.lower() == "n"):
            pass
            return 1
        elif (select.lower() == "no"):
            pass
            return 1
        else:
            print("\n*** Check your input value out whether the value is correct. ***\n")
            time.sleep(0.5)
            return 2
    else:
        image.paste(Watermark_img, position, Watermark_img)
        image.save("00_watermark-output/" + img[0][:-4] + ".png", "png")
        return 0

def editWatermark(image, Watermark_img_origin, opacity): # 워터마크의 크기, 불투명도 조절
    try:
        Watermark_img = Watermark_img_origin.resize((image.width // 2, Watermark_img_origin.height * (image.width // 2) // Watermark_img_origin.width), Image.LANCZOS)
        Watermark_img.putalpha(opacity)
        newData = [] # 수정된 픽셀 값을 저장하는 리스트
        datas = Watermark_img.getdata() # 워터마크 이미지에서 픽셀 값을 추출.
        for value in datas:
            if value[0] <= 0 and value[1] <= 0 and value[2] <= 0: # R, G, B 값 모두 0 이하인 픽셀의 값을 (0, 0, 0, 0) 으로 만듦.
                newData.append((0, 0, 0, 0))
            else:
                newData.append(value)
        Watermark_img.putdata(newData)
        return Watermark_img
    except:
        print("ERROR: Cannot Edit Watermark Image")
        time.sleep(0.5)

main()