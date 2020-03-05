import socket
import logging
import time

def main():
    print("Starting Sensor Process")

    host = "127.0.0.1"
    port = 8080

    sensorSocket = socket.socket()
    sensorSocket.connect((host, port))

    while True:
        message = "CAMERA:TRUE\n\r"
        sensorSocket.send(message.encode())
        time.sleep(1)


if __name__ == "__main__":
    main()