import cv2


def videoInput1():
    # 设置视频捕获
    cap = cv2.VideoCapture(0)

    while True:
        ret, im = cap.read()
        cv2.imshow('video test', im)
        key = cv2.waitKey(10)
        if key == 27:
            break
        if key == ord(' '):
            cv2.imwrite('vid_result.jpg', im)


def videoInput2():
    # 设置视频捕获
    cap = cv2.VideoCapture(0)

    # 获取视频帧，应用高斯平滑，显示结果
    while True:
        ret, im = cap.read()
        blur = cv2.GaussianBlur(im, (0, 0), 5)
        cv2.imshow('camera blur', blur)
        if cv2.waitKey(10) == 27:
            break


if __name__ == '__main__':
    # videoInput1()
    videoInput2()