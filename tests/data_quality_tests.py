import unittest
import cv2


class TestDataQuality(unittest.TestCase):
    def test_video_readability(self):
        cap = cv2.VideoCapture('./video.mp4')
        ret, frame = cap.read()
        cap.release()
        self.assertTrue(ret)

    def test_frame_size(self):
        cap = cv2.VideoCapture('./video.mp4')
        ret, frame = cap.read()
        cap.release()
        if ret:
            height, width, _ = frame.shape
            self.assertGreater(height, 0)
            self.assertGreater(width, 0)

    def test_video_duration(self):
        cap = cv2.VideoCapture('./video.mp4')
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        duration = frame_count / fps
        self.assertGreater(duration, 1)
