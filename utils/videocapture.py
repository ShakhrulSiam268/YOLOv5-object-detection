import cv2,threading, time
import queue 

# bufferless VideoCapture
class CustomVideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)
        
    def read(self):
        return self.q.get()

    def get_frame_info(self):
        frame_rate = self.cap.get(5)
        width  = self.cap.get(3)  # float `width`
        height = self.cap.get(4)
        return int(height),int(width)
        print('Camera FPS: {}'.format(frame_rate))
        print('Frame Dimension: {} x {}'.format(height,width))
   