//const int pinAccX = A0;
//const int pinAccY = A1;
//const int pinAccZ = A2;
//const int pinShockSensor = A3;
//
//float dataArray[5] = {0, 0, 0, 0, 0};
//
//float calculateSD(float val[])
//{
//    float sum = 0.0, mean, variance = 0.0, stdDeviation;
//    int i;
//    for (i = 0; i < 5; ++i)
//        sum += val[i];
//    mean = sum / 5;
//    for (i = 0; i < 5; ++i)
//        variance += pow(val[i] - mean, 2);
//    variance = variance / 5;
//    stdDeviation = sqrt(variance);
//
//    return stdDeviation;
//}
//
//void setup()
//{
//    Serial.begin(9600);
//    pinMode(pinAccX, INPUT);
//    pinMode(pinAccY, INPUT);
//    pinMode(pinAccZ, INPUT);
//    pinMode(pinShockSensor, INPUT);
//}
//
//void loop()
//{
//    float x = analogRead(pinAccX);
//    float y = analogRead(pinAccY);
//    float z = analogRead(pinAccZ);
//
//    float resultant = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
//    for (int i = 0; i < 5; i++)
//    {
//        if (i == 4)
//        {
//            dataArray[i] = resultant;
//            continue;
//        }
//        dataArray[i] = dataArray[i + 1];
//    }
//
//    float std = calculateSD(dataArray);
//
//    Serial.println(std);
//    // Serial.print(" ");
//    // Serial.println(resultant);
//}
