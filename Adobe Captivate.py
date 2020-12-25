#coding=utf-8

from time import *
import os
from datetime import datetime
import threading
import cv2
import pyaudio,wave
import numpy as np
from PIL import ImageGrab
from moviepy.editor import *

class ScreenRecord(object):
    def __init__(self):
        self.recording = True

    def record_audio(self):
        recordAudio = pyaudio.PyAudio()     #创建一个pyaudio（）.对象
        #创建一个输入流
        stream = recordAudio.open(format = pyaudio.paInt16,#表示使用量化位数16位来进行录音
        channels = 2,#通道的数量，2代表的是使用双声道
        rate = 44100,#采样频率，每秒采样48000个点
        input = True,#确定是输入流
        frames_per_buffer = 128#指定每个数据片段的帧数
        )

        waveFile = wave.open(self.audio_filename,'wb')
        waveFile.setnchannels(2)    #设置音频通道数
        waveFile.setsampwidth(recordAudio.get_sample_size(pyaudio.paInt16)) #设置量化位数
        waveFile.setframerate(44100)    #设置采样频率

        while self.recording:   #参数设置完毕，开始录制音频
            waveFile.writeframes(stream.read(128,exception_on_overflow=False))  #将数据写入到文件内

        waveFile.close()
        stream.stop_stream()    #停止输入
        stream.close()  #关闭输入流
        recordAudio.terminate()

    def video_record(self):
        screen = ImageGrab.grab()   #获取当前屏幕
        video = cv2.VideoWriter(self.video_record_filename,cv2.VideoWriter_fourcc(*'XVID'),20,screen.size)  #输出视频文件，帧数为20，大小为当前屏幕的大小
        while self.recording:
            screen = ImageGrab.grab()   #截取屏幕的内容
            screen = cv2.cvtColor(np.array(screen),cv2.COLOR_RGB2BGR)   #转换为bgr格式
            video.write(screen) #写入到视频文件中
        print(datetime.now())
        video.release()

    def run(self):
        print("3秒后开始录制屏幕，输入“q”结束录制")
        sleep(1)
        print(3)
        sleep(1)
        print(2)
        sleep(1)
        print(1)
        sleep(1)
        print("开始录屏")
        self.now = str(datetime.now())[:19].replace(':','_').replace('-','_').replace(' ','-')
        self.audio_filename = "{}.wav".format(self.now)
        self.video_record_filename = "{}_video.avi".format(self.now)
        self.video_filename = "{}.mp4".format(self.now)
        #开启两个线程，同时进行录音和屏幕录制
        t1 = threading.Thread(target = self.record_audio)
        t2 = threading.Thread(target = self.video_record)
        for t in [t1,t2]:
            t.start()
        while True:     #主程序一直保持等待模式，直到主程序输入“q”结束
            if(input() == 'q'):
                break
        self.recording = False
        for t in [t1,t2]:
            t.join()

        audio = AudioFileClip(self.audio_filename)      #采用moviepy读取视频
        video = VideoFileClip(self.video_record_filename)       #采用moviepy读取音频
        totalVideo = video.set_audio(audio)     #将音频附加到视频上去
        totalVideo.write_videofile(self.video_filename,codec = "libx264",fps = 25)      #将最终合成的视频保存到本地的avi视频文件中，图像编码为mp4格式，帧数为25
        os.remove(self.audio_filename)
        os.remove(self.video_record_filename)

if __name__ == '__main__':
    screenRecord = ScreenRecord()
    screenRecord.run()