#include <ESP8266WiFi.h>
const char* ssid="Akram-PC";
const char* password="wifi_password";
int i = 0;
#define pin1 16 //D0
#define pin2 5 //D1
#define pin4 4 //D2
#define pin3 0 //D3
//#define enb1 12 //D6
//#define enb2 14 //D5

WiFiServer server(80);
void setup()
{
  pinMode(pin1,OUTPUT);
  pinMode(pin2,OUTPUT);
  pinMode(pin3,OUTPUT);
  pinMode(pin4,OUTPUT);
//  pinMode(enb1, OUTPUT);
//  pinMode(enb2, OUTPUT);
  Serial.begin(115200);  
  Serial.print("Connecting to.");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print("..");
   }
  Serial.println("Nodemcu(esp8266) is connected to the ssid");
  Serial.println(WiFi.localIP());
  server.begin();
  delay(1000);
}

void loop()
{
  WiFiClient client = server.available();
  String motion = client.readStringUntil('\n');
  client.flush();
  Serial.println(motion);
  if(i == 0)
  {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);
    digitalWrite(pin3, LOW);
    digitalWrite(pin4, LOW);
    i = 1;
  }
  if(motion.indexOf("left") != -1)
  {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, HIGH);
    digitalWrite(pin3, HIGH);
    digitalWrite(pin4, LOW);
  }
  else if (motion.indexOf("right") != -1)
  {
    digitalWrite(pin1, HIGH);
    digitalWrite(pin2, LOW);
    digitalWrite(pin3, LOW);
    digitalWrite(pin4, HIGH);
  }
  else if (motion.indexOf("stop") != -1)
  {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);
    digitalWrite(pin3, LOW);
    digitalWrite(pin4, LOW);
  }
  else if (motion.indexOf("front") != -1)
  {
    digitalWrite(pin1, HIGH);
    digitalWrite(pin2, LOW);
    digitalWrite(pin3, HIGH);
    digitalWrite(pin4, LOW);
  }
  else if (motion.indexOf("back") != -1)
  {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, HIGH);
    digitalWrite(pin3, LOW);
    digitalWrite(pin4, HIGH);
  }
}
