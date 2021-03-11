import cv2, os

def framecap(title:str):
    cap= cv2.VideoCapture(f"videos/{title}.mp4")
    i=0
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = int(frame_count/fps)
    if duration > 45 and duration < 65:
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            if i == 1190:
                cv2.imwrite(f"Screenshots/{title}.jpg",frame)
                print("Screenshot Saved")
                cap.release()
                os.remove(f"videos/{title}.mp4")
                return True
            i+=1
    elif duration > 65 :
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            if i == 2600:
                cv2.imwrite(f"Screenshots/{title}.jpg",frame)
                print("Screenshot Saved")
                cap.release()
                os.remove(f"videos/{title}.mp4")
                return True
            i+=1
    else:
        cap.release()
        os.remove(f"videos/{title}.mp4")
        
        return False
    


def screenS(str_list):
    signal = {}
    for i in str_list:
        if ("Technical" in i):
            i = i.replace("60 Seconds ", '')
            i = i.replace(" Technical Analysis", '')
            signal["TC"] = i
        elif ("BUY :" in i):
            b = "".join(v for v in i if v in "0123456789.")
            signal["BS"] = b
            signal["BS_type"] = "BUY"
        elif "SL" in i:
            b = "".join(v for v in i if v in "0123456789.")
            signal["SL"] = b
        elif ("Trading" in i):
            b = "".join(v for v in i if v in "0123456789.")
            signal["TR"] = b
        elif "ТР" in i or "TP" in i:
            b = "".join(v for v in i if v in "0123456789.")
            signal["TP"] = b
        elif ("SELL :" in i):
            b = "".join(v for v in i if v in "0123456789.")
            signal["BS"] = b
            signal["BS_type"] = "SELL"
    print(signal)
    if len(signal) == 6:
        return signal
    else:
        return False
