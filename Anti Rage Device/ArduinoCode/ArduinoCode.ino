#include <Wire.h>

const int16_t MPU_addr = 0x68;

int16_t acc_x, acc_y, acc_z;
void setup() {
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  Serial.begin(9600);
}

void loop() {
  // Start reading from accelerometer
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x43);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 6, true);

  // Read and store bytes into variables
  acc_x = Wire.read() << 8 | Wire.read();
  acc_y = Wire.read() << 8 | Wire.read();
  acc_z = Wire.read() << 8 | Wire.read();

  // Get magnitude of acceleration
  // The division is just to reduce the magnitude of the numbers
  float x = (float)acc_x/16384+0.04;
  float y = (float)acc_y/16384;
  float z = (float)acc_z/16384-0.8;
  float t = abs(x)+abs(y)+abs(z);

  // Send serial data over usb and let the python script listen for it
  Serial.println("hit " + String(t));

  // Give the sensor a delay
  delay(100);
}
