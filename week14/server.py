import asyncio
import websockets
import subprocess
import threading

async def handler(websocket):
    print("手机已连接!")
    async for message in websocket:
        print(f"收到指令: {message}")
        if message == "forward":
            cmd = "ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \"{linear: {x: 2.0}, angular: {z: 0.0}}\""
        elif message == "backward":
            cmd = "ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \"{linear: {x: -2.0}, angular: {z: 0.0}}\""
        elif message == "left":
            cmd = "ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \"{linear: {x: 0.0}, angular: {z: 2.0}}\""
        elif message == "right":
            cmd = "ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \"{linear: {x: 0.0}, angular: {z: -2.0}}\""
        else:
            continue
        subprocess.Popen(cmd, shell=True)

async def main():
    print("WebSocket服务启动，等待手机连接...")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())
