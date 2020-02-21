const int pinX = A0;
const int pinY = A1;
const int pinZ = A2;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  pinMode(pinX, INPUT);
  pinMode(pinY, INPUT);
  pinMode(pinZ, INPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:

  // For Arduino Serial Plotter
  Serial.print(analogRead(pinX));
  Serial.print(" ");
  Serial.print(analogRead(pinY));
  Serial.print(" ");
  Serial.println(analogRead(pinZ));

  // For Python Code
//  Serial.print("X:");
//  Serial.print(analogRead(pinX));
//  Serial.print(";Y:");
//  Serial.print(analogRead(pinY));
//  Serial.print(";Z:");
//  Serial.print(analogRead(pinZ));
//  Serial.println(";");
}
