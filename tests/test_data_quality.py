import unittest
import cv2
import os
import subprocess


class TestDataQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Убедитесь, что видеофайл загружен из DVC перед запуском тестов"""
        if not os.path.exists('./video.mp4'):
            subprocess.run(['dvc', 'pull', 'video.mp4.dvc'], check=True)

    def test_video_readability(self):
        """Тест считывание файла с видео"""
        cap = cv2.VideoCapture('./video.mp4')
        ret, frame = cap.read()
        cap.release()
        self.assertTrue(ret)

    def test_frame_size(self):
        """Проверка размеров кадров видео"""
        cap = cv2.VideoCapture('./video.mp4')
        ret, frame = cap.read()
        cap.release()
        if ret:
            height, width, _ = frame.shape
            self.assertGreater(height, 0)
            self.assertGreater(width, 0)

    def test_video_duration(self):
        """Проверка длительности видео (больше 1 секунды)"""
        cap = cv2.VideoCapture('./video.mp4')
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        duration = frame_count / fps
        self.assertGreater(duration, 1)


if __name__ == '__main__':
    unittest.main()
