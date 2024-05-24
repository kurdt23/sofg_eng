#Библиотеки
import cv2
import numpy as np
import requests
from ultralytics import YOLO
"""Практическое
задание №3  лишние библиотеки и переменные """

# Это необходимо заполнить для работы с telegram ботом
# можно этим воспользоваться https://t.me/freeparkingcar_bot в нем же узнать chat_id
TOKEN = "6992030569:AAEMhDEOee66IsjvbQlVg_BF6w1s_GmtKu8"
chat_id = "1410176450"

# load yolov8 model
model = YOLO('yolov8n.pt')

# Тестовое видео
# если работаем с камерой, то необходимо передать cv2.VideoCapture(video_path) цифру ноль
video_path = './video.mp4'

def calculate_iou(box, boxes, box_area, boxes_area):
    #Считаем IoU
    y1 = np.maximum(box[0], boxes[:, 0])
    y2 = np.minimum(box[2]+box[0], boxes[:, 2]+boxes[:, 0])
    x1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[3]+box[1], boxes[:, 3]+boxes[:, 1])
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    union = box_area + boxes_area[:] - intersection[:]
    iou = intersection / union
    return iou

#Функция для расчета персечения всех со всеми через IoU
def compute_overlaps(boxes1, boxes2):
    #Areas of anchors and GT boxes
    area1 = boxes1[:, 2] * boxes1[:, 3]
    area2 = boxes2[:, 2] * boxes2[:, 3]
    overlaps = np.zeros((boxes1.shape[0], boxes2.shape[0]))
    for i in range(overlaps.shape[1]):
        box2 = boxes2[i]
        overlaps[:, i] = calculate_iou(box2, boxes1, area2[i], area1)
    return overlaps

def draw_bbox(x, y, w, h, parking_text, parking_color=(0, 255, 0)):
    start = (x, y)
    end = (x + w, y + h)
    color = parking_color
    width = 2
    final_image = cv2.rectangle(image_to_process, start, end, color, width)

    # Подпись BB
    start = (x, y - 10)
    font_size = 0.4
    font = cv2.FONT_HERSHEY_SIMPLEX
    width = 1
    text = parking_text
    final_image = cv2.putText(final_image, text, start, font, font_size, color, width, cv2.LINE_AA)
    return final_image

# Функция для отправки фото в телеграм
def send_photo_file(chat_id, img):
    files = {'photo': open(img, 'rb')}
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}', files=files)

# Функция для отправки сообщения в телеграм
def send_telegram_message(message):
    requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}').json()


#Парковочные места
first_frame_parking_spaces = None

free_parking_timer = 0
free_parking_timer_bag1 = 0
        # free_parking_count = 0
        # first_parking_timer = 0
free_parking_space = False
free_parking_space_box = None
check_det_frame = None
telegram_message = False

#Классы которые распознает YOLO
        # path_coco_names = "./coco.names.txt"





        # results = model.predict(image_to_process)
        # frame_ = results[0].plot()
        # print(results[0].boxes.conf)
        # print(results[0].boxes.cls)

        # for i in results[0].boxes.conf.numpy():
        #     print('conf: ',i)
video_capture = cv2.VideoCapture(video_path)
# Пока не нажата клавиша q функция будет работать
# isOpened() Возвращает true, если захват видео уже инициализирован.
while video_capture.isOpened():
    ret, image_to_process = video_capture.read()
    """Практическое
    задание №3  shape вызывает ошибку в конце"""
                # height, width, _ = image_to_process.shape
    if not ret:
        break

    results = model.predict(image_to_process)
    """Практическое
    задание №3  model.track хуже детектирует чем model.predict"""
                # results = model.track(image_to_process, persist=False)

                # frame_ = results[0].plot()
    detections = results[0].boxes

    class_indexes, class_scores, boxes = ([] for i in range(3))
    for class_index in detections:
        #print('cls: ', class_index)
        if class_index.cls.numpy() == 2:
            #print(class_index)
            #class_score = scores[class_index]
            box = class_index.xywh.numpy().astype(int)[0].tolist()
            box = [box[0] - box[2] // 2, box[1]  - box[3]  // 2,
                   box[2], box[3]]
            boxes.append(box)
            class_scores.append(float(class_index.conf ))
            # if class_score > 0:
    #first_frame_parking_spaces = boxes

    # print((boxes))
    # print((boxes[0]))
    # print((boxes[0][0]))
    # print(type(boxes))
    # print(type(boxes[0]))
    # print(type(boxes[0][0]))
    # print((boxes[0][0]))

    if not first_frame_parking_spaces:
        # Предполагаем, что под каждой машиной будет парковочное место
        first_frame_parking_spaces = boxes
        first_frame_parking_score = class_scores
        #print('first_frame_parking_spaces')


    else:
        chosen_cars_boxes = cv2.dnn.NMSBoxes(boxes, class_scores, 0.0, 0.4)
        cars_area = []
        ###МАШИНЫ
        for box_index in chosen_cars_boxes:

            car_box = boxes[box_index]
            cars_area.append(car_box)

            x, y, w, h = car_box
            parking_text = 'Car'
            final_image = draw_bbox(x, y, w, h, parking_text, (255, 255, 0))
        cars_boxes = cars_area

            ###IoU
        overlaps = compute_overlaps(np.array(parking_spaces), np.array(cars_boxes))

        for parking_space_one, area_overlap in zip(parking_spaces, overlaps):

            max_IoU = max(area_overlap)
            sort_IoU = np.sort(area_overlap[area_overlap > 0])[::-1]

            if free_parking_space == False:
                if 0.0 < max_IoU < 0.4:
                    # Количество паркомест по условию 1: 0.0 < IoU < 0.4
                    len_sort = len(sort_IoU)

                    # Количество паркомест по условию 2: IoU > 0.15
                    sort_IoU_2 = sort_IoU[sort_IoU > 0.15]
                    len_sort_2 = len(sort_IoU_2)

                    # Смотрим чтобы удовлятворяло условию 1 и условию 2
                    if (check_det_frame == parking_space_one) & (len_sort != len_sort_2):
                        # Начинаем считать кадры подряд с пустыми координатами
                        free_parking_timer += 1


                    elif check_det_frame == None:
                        check_det_frame = parking_space_one

                    else:
                        # Фильтр от чехарды мест (если место чередуется, то "скачет")
                        free_parking_timer_bag1 += 1
                        if free_parking_timer_bag1 == 2:
                            # Обнуляем счётчик, если паркоместо "скачет"
                            check_det_frame = parking_space_one
                            free_parking_timer = 0

                    # Если более 10 кадров подряд, то предполагаем, что место свободно
                    if free_parking_timer == 10:
                        # Помечаем свободное место
                        free_parking_space = True
                        free_parking_space_box = parking_space_one
                        # Отрисовываем рамку парковочного места
                        x_free, y_free, w_free, h_free = parking_space_one

            else:
                # Если место занимают, то помечается как отсутствие свободных мест
                overlaps = compute_overlaps(np.array([free_parking_space_box]), np.array(cars_boxes))
                for area_overlap in overlaps:
                    max_IoU = max(area_overlap)
                    if max_IoU > 0.6:

                        free_parking_space = False
                        telegram_message = False

                        # Отправка сообщения боту в телеграмм
                        if not telegram_message:
                            screenshot_parking_space = final_image
                            # отправим в телеграм
                            message_tel = 'Где ты ездишь??? Место уже занято :('
                            send_telegram_message(message_tel)
                            cv2.imwrite('./image_test_not_free.png', screenshot_parking_space)
                            send_photo_file(chat_id, './image_test_not_free.png')

                            telegram_message = True

    # ПАРКОВОЧНЫЕ МЕСТА
    # Отрисовка BB парковочных мест
    chosen_boxes = cv2.dnn.NMSBoxes(first_frame_parking_spaces,
                                    first_frame_parking_score, 0.0, 0.4)
    parking_spaces = []
    for box_index in chosen_boxes:
        box = first_frame_parking_spaces[box_index]
        # Если определилось пустое место, то отрисуем его в кадре
        if free_parking_space:
            if box == [x_free, y_free, w_free, h_free]:
                parking_text = 'FREE SPACE!!!'
                final_image = draw_bbox(x_free, y_free, w_free, h_free, parking_text, (0, 0, 255))
            else:
                x, y, w, h = box
                parking_text = 'No parking'
                final_image = draw_bbox(x, y, w, h, parking_text)

            # Отправка сообщения боту в телеграмм
            if not telegram_message:
                # Скриншот свободного места, отправим в телеграм
                screenshot_parking_space = final_image
                message_tel = 'Свободное место! Давай, жми скорее!!!'
                send_telegram_message(message_tel)
                cv2.imwrite('./image_test_free.png', screenshot_parking_space)
                send_photo_file(chat_id, './image_test_free.png')

                telegram_message = True

        else:
            # Координаты и размеры BB
            x, y, w, h = box
            parking_text = 'No parking'
            final_image = draw_bbox(x, y, w, h, parking_text)

        # Координаты парковочных мест с первого кадры
        parking_spaces.append(box)
    # Показать результат работы
    cv2.imshow("Parking Space", final_image)

    # Прерывание работы клавишей q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        # Очищаем всё после завершения.

"""Практическое задание №3  
video_capture.release() вынести вне цикла"""
video_capture.release()
cv2.destroyAllWindows()
