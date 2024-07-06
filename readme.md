前端apidemo文件夹，后端APIProject文件夹。前端使用vue3搭建项目作为界面，后端使用Flask框架，前后端使用websocket通信。

将调用两个AI接口用于车辆检测、车型识别。

在网页点击“开始监控”发送请求，后端路由接收请求后，会创建两个线程将本地的两个监控视频使用opencv打开，并转化为一帧帧图片。后端将这些图片发送到前端，在网页特定区域实现展示两个监控画面的效果。

每隔一定帧数，后端将每张图片通过post发送至车辆检测API，车辆检测API返回图片中每个车辆的类型（卡车、汽车、摩托车等等），以及该车辆在图片中的位置坐标（top、left、height、width），并对车辆数据进行统计。

后端程序接收到车辆检测API的响应结果后，将创建对应的车类识别线程。车类识别线程根据每个车辆在图片中的位置坐标，分别截取对应的车辆部分发送给车类识别API，在接收到车类识别API的响应结果后，将截取下的车辆图片与信息发送至前端，前端将截取到的车辆图片以走马灯形式在网页特定区域展示，并在图片下方标注其信息。

在网页点击“结束监控”发送请求，后端路由接收请求后，会通知两个线程停止监控，并等待线程完全结束。

在网页点击“统计数据”发送请求，后端路由接收请求后，会返回统计到的数据。前端接收到数据后，将在网页弹出一个界面，界面上将以表格形式展示各监控视频中的车辆数据，并展示总共的车流量。

