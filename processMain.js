const net = require("net");

const HOST = "127.0.0.1";
const PORT = 8080;

const STATE = {
    DETECT_INIT: 0,
    DETECT_START: 1,
    SENSOR_TRIGGER: 2,
    GPS_TRIGGER: 3,
    CAMERA_TRIGGER: 4,
    ACCIDENT_REPORT: 5
};

let currentState = STATE.DETECT_INIT;
let sensorInitStatus = [0, 0, 0];

let server = net.createServer(socket => {

    socket.on("connect", () => {
        console.log(`Connected to ${socket.remoteAddress}`);
    });

    socket.on("data", data => {
        //TODO: Write data processing stuff
        let receivedData = data.toString();
        switch (currentState) {
            case STATE.DETECT_INIT:
                console.log("Current State: Detect Init");
                if (receivedData.indexOf("SENSOR") > -1) {
                    sensorInitStatus[0] = 1;
                } else if (receivedData.indexOf("CAMERA") > -1) {
                    sensorInitStatus[1] = 1;
                } else if (receivedData.indexOf("GPS") > -1) {
                    sensorInitStatus[2] = 1;
                }

                let nextState = true;

                sensorInitStatus.forEach(value => {
                    if (value === 0) {
                        nextState = false;
                    }
                });

                if (nextState === true) {
                    currentState = STATE.DETECT_START;
                }

                break;

            case STATE.DETECT_START:
                console.log("Current State: Detection start");
                if ((receivedData.indexOf("SENSOR") > -1) && (receivedData.indexOf("TRUE") > -1)) {
                    currentState = STATE.SENSOR_TRIGGER;
                }
                break;

            case STATE.SENSOR_TRIGGER:
                console.log("Current State: Sensor triggered");
                if ((receivedData.indexOf("GPS") > -1) && (receivedData.indexOf("TRUE") > -1)) {
                    currentState = STATE.GPS_TRIGGER;
                }
                break;

            case STATE.GPS_TRIGGER:
                console.log("Current State: GPS triggered");
                if ((receivedData.indexOf("CAMERA") > -1) && (receivedData.indexOf("TRUE") > -1)) {
                    currentState = STATE.CAMERA_TRIGGER;
                }
                break;

            case STATE.CAMERA_TRIGGER:
                console.log("Current State: Camera Triggered");
                break;

            case STATE.ACCIDENT_REPORT:
                break;
        
            default:
                break;
        }
    });

    socket.on("close", () => {
        console.log(`Connection closed: ${socket.remoteAddress}`);
    });

    socket.on("error", error => {
        console.log(`Error at ${socket.remoteAddress}`);
    });

}).listen(PORT, HOST);