
'''\
This Simple program Demonstrates how to use G-Streamer and capture RTSP Frames in Opencv using Python
- Sahil Parekh
'''

import multiprocessing as mp
import time
import vid_streamv3 as vs
import cv2
import sys

'''
Main class
'''
class mainStreamClass:
    def __init__(self):

        #Current Cam
        self.camProcess = None
        self.cam_queue = None
        self.stopbit = None
        self.camlink = 'rtsp://admin:gazeme@192.168.178.37:554/h264Preview_07_main' #Add your RTSP cam link
        self.framerate = 20 
    
    def startMain(self):

        #set  queue size
        self.cam_queue = mp.Queue(maxsize=100)

        #get all cams
        time.sleep(3)

        self.stopbit = mp.Event()
        self.camProcess = vs.StreamCapture(self.camlink,
                             self.stopbit,
                             self.cam_queue,
                            self.framerate)
        self.camProcess.start()

        # calculate FPS
        lastFTime = time.time()

        try:
            while True:

                if not self.cam_queue.empty():
                    # print('Got frame')
                    cmd, val = self.cam_queue.get()

                    '''
                    #calculate FPS
                    diffTime = time.time() - lastFTime`
                    fps = 1 / diffTime
                    # print(fps)
                    
                    '''
                    lastFTime = time.time()

                    # if cmd == vs.StreamCommands.RESOLUTION:
                    #     pass #print(val)

                    if cmd == vs.StreamCommands.FRAME:
                        if val is not None:
                            cv2.imshow('Cam: ' + self.camlink, val)
                            cv2.waitKey(1)

        except KeyboardInterrupt:
            print('Caught Keyboard interrupt')

        except:
            e = sys.exc_info()
            print('Caught Main Exception')
            print(e)

        self.stopCamStream()
        cv2.destroyAllWindows()


    def stopCamStream(self):
        print('in stopCamStream')

        if self.stopbit is not None:
            self.stopbit.set()
            while not self.cam_queue.empty():
                try:
                    _ = self.cam_queue.get()
                except:
                    break
                self.cam_queue.close()

            self.camProcess.join()


if __name__ == "__main__":
    mc = mainStreamClass()
    mc.startMain()
