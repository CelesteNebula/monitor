from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import cv2
import threading
import time
import requests
import base64
import numpy as np
from flask_cors import CORS  # 引入Flask-CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化视频流
video_stream_1 = cv2.VideoCapture(r'resources/vd1.mp4')
video_stream_2 = cv2.VideoCapture(r'resources/vd2.mp4')

# 访问令牌
access_token = '24.616137c62e6332b42435f68f1c720531.2592000.1722739901.282335-89991653'
vehicle_detection_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
car_recognition_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"

# 全局变量用于存储车辆统计信息
vehicle_stats = {
    'video1': {'car': 0, 'truck': 0, 'motorbike': 0, 'bus': 0, 'tricycle': 0, 'carplate': 0},
    'video2': {'car': 0, 'truck': 0, 'motorbike': 0, 'bus': 0, 'tricycle': 0, 'carplate': 0}
}

# 全局变量用于控制线程
monitoring_threads = {}
monitoring_flags = {}

def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def vehicle_detection(image):
    try:
        img_base64 = encode_image(image)
        params = {"image": img_base64}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(vehicle_detection_url + "?access_token=" + access_token, data=params, headers=headers)
        print("调用车辆检测API")
        if response:
            print("车辆检测API响应：", response.json())
            return response.json()
        return None
    except Exception as e:
        print(f"Vehicle detection error: {e}")
        return None

def car_recognition(image):
    try:
        img_base64 = encode_image(image)
        params = {"image": img_base64, "top_num": 5}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(car_recognition_url + "?access_token=" + access_token, data=params, headers=headers)
        print("调用车型识别API")
        if response:
            print("车型识别API响应：", response.json())
            return response.json()
        return None
    except Exception as e:
        print(f"Car recognition error: {e}")
        return None

def process_vehicle_info(vehicle_info, frame, stream_name):
    last_request_time = time.time()
    for vehicle in vehicle_info:

        vehicle_type = vehicle['type']
        location = vehicle['location']
        top, left, height, width = location['top'], location['left'], location['height'], location['width']

        # 控制车辆检测请求频率
        current_time = time.time()
        if current_time - last_request_time < 1:
            time.sleep(1 - (current_time - last_request_time))
        last_request_time = current_time

        # 截取车辆部分并进行车型识别
        cropped_vehicle = frame[top:top + height, left:left + width]
        recognition_result = car_recognition(cropped_vehicle)
        if recognition_result:
            top_result = recognition_result['result'][0]
            model_info = {
                'image': encode_image(cropped_vehicle),
                'name': top_result['name'],
                'year': top_result['year'],
                'color': recognition_result['color_result'],
                'score': top_result['score'],
                'type': vehicle_type
            }
            # 发送识别结果给前端
            socketio.emit(f'{stream_name}_recognized', model_info)
        else:
            print(f"Recognition failed for vehicle in {stream_name}")

def process_video(video_stream, stream_name):
    last_request_time = time.time()
    print(f"Starting video processing for {stream_name}")
    monitoring_flags[stream_name] = True
    count_flag = 0
    while monitoring_flags[stream_name]:
        ret, frame = video_stream.read()
        if not ret:
            print(f"Failed to read from video stream: {stream_name}")
            break

        # 控制车辆检测请求频率
        current_time = time.time()
        if current_time - last_request_time < 1:
            time.sleep(1 - (current_time - last_request_time))
        last_request_time = current_time

        # 发送帧给前端
        try:
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            socketio.emit(f'{stream_name}_frame', {'frame': frame_base64})
            count_flag += 1
        except Exception as e:
            print(f"Error encoding or emitting frame: {e}")

        if count_flag >= 10:
            # 车辆检测
            detection_result = vehicle_detection(frame)
            if detection_result and 'vehicle_num' in detection_result:
                vehicle_num = detection_result['vehicle_num']
                vehicle_info = detection_result['vehicle_info']

                for vehicle_type, count in vehicle_num.items():
                    vehicle_stats[stream_name][vehicle_type] += count

                # 创建一个新的线程进行车型识别
                recognition_thread = threading.Thread(target=process_vehicle_info, args=(vehicle_info, frame, stream_name))
                recognition_thread.start()
            else:
                print(f"No vehicle_num in response for {stream_name}")

            time.sleep(0.1)
    print(f"Finished video processing for {stream_name}")

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    try:
        print("启动监控")
        if 'video1' not in monitoring_threads:
            monitoring_threads['video1'] = threading.Thread(target=process_video, args=(video_stream_1, 'video1'))
            monitoring_threads['video1'].start()
        if 'video2' not in monitoring_threads:
            monitoring_threads['video2'] = threading.Thread(target=process_video, args=(video_stream_2, 'video2'))
            monitoring_threads['video2'].start()
        return jsonify({'status': 'started'})
    except Exception as e:
        print(f"启动监控错误：{e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    try:
        print("结束监控")
        monitoring_flags['video1'] = False
        monitoring_flags['video2'] = False
        monitoring_threads['video1'].join()
        monitoring_threads['video2'].join()
        del monitoring_threads['video1']
        del monitoring_threads['video2']
        return jsonify({'status': 'stopped'})
    except Exception as e:
        print(f"结束监控错误：{e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(vehicle_stats)

@app.route('/traffic', methods=['GET'])
def get_traffic():
    # 假设车流量是所有车辆类型的总和
    total_traffic = sum(sum(vehicle_stats[stream].values()) for stream in vehicle_stats)
    return jsonify({'traffic': total_traffic})

if __name__ == '__main__':
    socketio.run(app, debug=True)
