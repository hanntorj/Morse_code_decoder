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

  if(timeOff > 2*T && timeOff < 8*T){
    Serial.print(3);
  }

  if(timeOff > 8*T && timeOff < 50*T){
    Serial.print(4);
  }
  if(timeOff > 50*T) {
    Serial.print(5);
  }
  timeCountOff = currentTimeOff;
  delay(100);
 }

 if(digitalRead(switchPin) == HIGH) {
  int currentTimeOn = millis();
  int timeOn = currentTimeOn - timeCountOn;

  if(timeOn > wait){
    if(timeOn <= 1.5 * T){
      Serial.print(1);
      digitalWrite(ledPinDash, LOW);
      digitalWrite(ledPinDot, HIGH);
  }

  if(timeOn > 1.5*T && timeOn <= 4*T){
    Serial.print(2);
    digitalWrite(ledPinDot, LOW);
    digitalWrite(ledPinDash, HIGH);
  }
 }
 timeCountOn = currentTimeOn;
 delay(100);
 }
}
