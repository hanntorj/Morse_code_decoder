const int ledPinDot = 2;
const int ledPinDash = 8;
const int switchPin = 7;
int timeCountOff = 0;
int timeCountOn = 0;
int T = 300;
int wait = 105;

void setup(){
  Serial.begin(9600);
  pinMode( ledPinDot, OUTPUT );
  pinMode( ledPinDash, OUTPUT );
  pinMode( switchPin, INPUT );
} 

void loop(){
 if (digitalRead(switchPin) == LOW){
  int currentTimeOff = millis();
  int timeOff = currentTimeOff - timeCountOff;

  if(timeOff > 3*T && timeOff < 7*T){
    Serial.println(2);
  }

  if(timeOff > 7*T && timeOff < 100*T){
    Serial.println(3);
  }
  else {
    Serial.println(4);
  }
  timeCountOff = currentTimeOff;
  delay(100);
 }

 if(digitalRead(switchPin) == HIGH) {
  int currentTimeOn = millis();
  int timeOn = currentTimeOn - timeCountOn;

  if(timeOn > wait){
    if(timeOn <= 1*T){
      Serial.println(0);
      digitalWrite(ledPinDash, LOW);
      digitalWrite(ledPinDot, HIGH);
  }

  if(timeOn > T && timeOn <= 4*T){
    Serial.println(1);
    digitalWrite(ledPinDot, LOW);
    digitalWrite(ledPinDash, HIGH);
  }
 }
 timeCountOn = currentTimeOn;
 delay(100);
 }
}
