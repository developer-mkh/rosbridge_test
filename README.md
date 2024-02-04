# rosbridge_test

[rosbridge](https://github.com/RobotWebTools/rosbridge_suite)の動作検証。

# led
- [ソースコード](./catkin_ws/src/led/led/src/led_test.py)  
- [参考ページ](https://wakky.tech/ros3-raspberry-pi-ds4-gpio-led/)

ROSノード。/ledをsubscribeし、RaspberryPiのGPIOに値を書き込む（Lチカを実現するノード）。

# client
- [ソースコード](./client/test.html)
- [参考ページ](https://yoshiaki-toyama.com/ros-web-interface/)

コントロールするPC上のブラウザで表示する。

# 操作方法
1. RaspberryPi上の操作
   1. rosbridgeを起動
   2. ledを起動
1. PC上の操作
   1. clientのHTMLをPCのブラウザで開く
   2. Server AddressにRaspberryPiのIPアドレス（ホスト名（FQDN）でも良い）、Server portにrosbridgeのリッスンポートを入力
   3. Push this button to connect ROSを押下
   4. ラジオボタンのどちらかを選択
   5. Push this button to publish /led topicを押下

[上記操作のデモ動画](./デモ.mp4)
