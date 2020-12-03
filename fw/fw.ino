/*
  Author: Burak Kakillioglu
  Website: bkakilli.github.io
*/

int set_value;
int sensor_value;
int increment_precision;
const int mute_toggle_pin = 13;
const int play_toggle_pin = 5;
const int next_toggle_pin = 6;
const int prev_toggle_pin = 7;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  increment_precision = 5;
  pinMode(mute_toggle_pin, INPUT);
  pinMode(play_toggle_pin, INPUT);
  pinMode(next_toggle_pin, INPUT);
  pinMode(prev_toggle_pin, INPUT);
}

void submit_value(int val) {
  Serial.println(val);
  set_value = 0;
}

void loop() {
  // read the input on analog pin 0:
  sensor_value = analogRead(A0);

  if (abs(sensor_value - set_value) > increment_precision) {
    submit_value(sensor_value);
    set_value = sensor_value;
  }
  
  if(digitalRead(mute_toggle_pin)) {
    submit_value(-10);
    delay(200);
  }
  
  if(digitalRead(play_toggle_pin)) {
    submit_value(-20);
    delay(200);
  }
  
  if(digitalRead(next_toggle_pin)) {
    submit_value(-30);
    delay(200);
  }
  
  if(digitalRead(prev_toggle_pin)) {
    submit_value(-40);
    delay(200);
  }

  delay(50);        // delay in between reads for stability
}
