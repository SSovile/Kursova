#include <LiquidCrystal.h>
LiquidCrystal lcd(A0,A1,A2,A3,A4,A5);
  int count = 0;
  const String password = "1234";
  String entered_password;
  int redLed = 13;
  int motor = 12;

void setup() {
  Serial.begin(9600);
  pinMode(redLed,OUTPUT);
  pinMode(motor,OUTPUT);
  lcd.begin(20,4);
  lcd.setCursor(0,0);
  lcd.print("welcome to: ");
  lcd.setCursor(0,1);
  lcd.print("vlada");
  delay(1000);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("press [*] to start");
}

void loop() {
  String key = Serial.readString();
  if(key){
    lcd.setCursor(count, 1);
    lcd.println(key);
    count++;
    if(key =="*"){
      lcd.clear();
      lcd.print("enter the pass:");
       digitalWrite(motor,LOW);
        digitalWrite(redLed,LOW);
        count = 0;
    }
    else if(key=="#"){
      if(password == entered_password){
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("Correct");
        digitalWrite(motor,100);
        delay(1000);
        digitalWrite(motor,0);
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("press [*]");
        sendToDb(entered_password);
      }
      else{
        lcd.clear(); 
        lcd.print("incorrect");
        lcd.setCursor(0,1);
        lcd.print("press [*]");
         digitalWrite(redLed,HIGH);
         delay(2000);
        digitalWrite(redLed,LOW);
      }
      entered_password="";
    }
    else{
      entered_password+=key;
    }
  }
}

void sendToDb(String password) { 
  Serial.print(password);
}
