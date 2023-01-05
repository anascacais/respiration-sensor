int f = 10, dt = 0;
unsigned long t = 0, lt = 0; 
const int buttonPin = 3;  // the number of the pushbutton pin

void setup() {
  pinMode(buttonPin, INPUT);
  Serial.begin(115200);
  dt = int(1000*1/(float)f);
}

void loop() {
  t = millis();
  if ((t-lt) >= dt) {
    Serial.print(digitalRead(buttonPin));
    Serial.print("\n");
    lt = t;
  }
}
