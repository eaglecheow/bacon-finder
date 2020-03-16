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

let iothatMessageToSend = "";
let iothatIsMessageAvailable = false;

let accidentData = {
    sensor: "",
    location: "",
    camera: ""
}

net.createServer(socket => {

    socket.on("connect", () => {
        console.log(`Connected to ${socket.remoteAddress}`);
    });

    socket.on("data", data => {
        //TODO: Write data processing stuff
        let receivedData = data.toString();
        console.log(receivedData);
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
                    accidentData.sensor = receivedData;
                }
                break;

            case STATE.SENSOR_TRIGGER:
                console.log("Current State: Sensor triggered");
                if ((receivedData.indexOf("GPS") > -1) && (receivedData.indexOf("TRUE") > -1)) {
                    currentState = STATE.GPS_TRIGGER;
                    accidentData.location = receivedData;
                }
                break;

            case STATE.GPS_TRIGGER:
                console.log("Current State: GPS triggered");
                if ((receivedData.indexOf("CAMERA") > -1) && (receivedData.indexOf("TRUE") > -1)) {
                    currentState = STATE.CAMERA_TRIGGER;
                    accidentData.camera = receivedData;
                }
                break;

            case STATE.CAMERA_TRIGGER:
                console.log("Current State: Camera Triggered");

                iothatMessageToSend = `AD -> ${accidentData.sensor}|${accidentData.location}|${accidentData.camera}`;
                iothatIsMessageAvailable = true;

                currentState = STATE.ACCIDENT_REPORT;
                break;

            case STATE.ACCIDENT_REPORT:
                break;

            default:
                break;
        }

        if (receivedData.indexOf("GPS") > -1) {
            if (iothatIsMessageAvailable === true) {
                socket.write(iothatMessageToSend);
                iothatIsMessageAvailable = false;
                iothatMessageToSend = "";
            } else {
                socket.write("EMPTY");
            }
        }
    });

    socket.on("close", () => {
        console.log(`Connection closed: ${socket.remoteAddress}`);
    });

    socket.on("error", error => {
        console.log(`Error at ${socket.remoteAddress}`);
    });

}).listen(PORT, HOST);

console.log(`Raspi Process running at ${HOST}:${PORT}`);
