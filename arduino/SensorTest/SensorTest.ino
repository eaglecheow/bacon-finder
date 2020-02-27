const int pinAccX = A0;
const int pinAccY = A1;
const int pinAccZ = A2;
const int pinShockSensor = A3;

void setup()
{
  // put your setup code here, to run once:

  Serial.begin(9600);
  pinMode(pinAccX, INPUT);
  pinMode(pinAccY, INPUT);
  pinMode(pinAccZ, INPUT);
  pinMode(pinShockSensor, INPUT);
}

void loop()
{
  // put your main code here, to run repeatedly:

  // For Arduino Serial Plotter
  // Serial.print(analogRead(pinAccX));
  // Serial.print(" ");
  // Serial.print(analogRead(pinAccY));
  // Serial.print(" ");
  // Serial.print(analogRead(pinAccZ));
  // Serial.print(" ");
  // Serial.println(analogRead(pinShockSensor));

  // For Python Code
  Serial.print("X:");
  Serial.print(analogRead(pinAccX));
  Serial.print(";Y:");
  Serial.print(analogRead(pinAccY));
  Serial.print(";Z:");
  Serial.print(analogRead(pinAccZ));
  Serial.print(";V:");
  Serial.print(analogRead(pinShockSensor));
  Serial.println(";");
}
