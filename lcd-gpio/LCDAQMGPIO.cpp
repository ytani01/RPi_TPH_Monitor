//---------------------------------
// 2017/1/9

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
#include <wiringPi.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include "LCDAQMGPIO.h"


//---------------------------------
// Private Class Function

// Write control and data by I2C
void LCDAQMGPIO::writeData(uint8_t ctrl, uint8_t data){
	digitalWrite(2, 0);
	digitalWrite(3, 0);
	pinMode(2, INPUT);		// SDA
	pinMode(3, INPUT);		// SCL
	delayMicroseconds(200);

	// Start
	pinMode(2, OUTPUT);
	delayMicroseconds(10);
	pinMode(3, OUTPUT);
	delayMicroseconds(10);

	// Address
	uint8_t buf = 0x7C;
	for(uint8_t i=0; i<8; i++){
		pinMode(3, OUTPUT);
		if(0==((buf>>(7-i))&1)){
			pinMode(2, OUTPUT);
		}else{
			pinMode(2, INPUT);
		}
		delayMicroseconds(10);
		pinMode(3, INPUT);
		delayMicroseconds(10);
	}
	pinMode(3, OUTPUT);
	pinMode(2, INPUT);
	delayMicroseconds(10);
	pinMode(3, INPUT);
	delayMicroseconds(10);

	// 1st Byte
	buf = ctrl;
	for(uint8_t i=0; i<8; i++){
		pinMode(3, OUTPUT);
		if(0==((buf>>(7-i))&1)){
			pinMode(2, OUTPUT);
		}else{
			pinMode(2, INPUT);
		}
		delayMicroseconds(10);
		pinMode(3, INPUT);
		delayMicroseconds(10);
	}
	pinMode(3, OUTPUT);
	pinMode(2, INPUT);
	delayMicroseconds(10);
	pinMode(3, INPUT);
	delayMicroseconds(10);

	// 2nd Byte
	buf = data;
	for(uint8_t i=0; i<8; i++){
		pinMode(3, OUTPUT);
		if(0==((buf>>(7-i))&1)){
			pinMode(2, OUTPUT);
		}else{
			pinMode(2, INPUT);
		}
		delayMicroseconds(10);
		pinMode(3, INPUT);
		delayMicroseconds(10);
	}
	pinMode(3, OUTPUT);
	pinMode(2, INPUT);
	delayMicroseconds(10);
	pinMode(3, INPUT);
	delayMicroseconds(10);

	// Stop
	pinMode(3, OUTPUT);
	pinMode(2, OUTPUT);
	delayMicroseconds(10);
	pinMode(3, INPUT);
	delayMicroseconds(10);
	pinMode(2, INPUT);
	return;
}



//---------------------------------
// Public Class Function

LCDAQMGPIO::LCDAQMGPIO(){
	count = 0;
	line = 1;
}


// Initialize LCD
//  Return 0 if success
uint8_t LCDAQMGPIO::init(){
	writeData(0, 0x38);
	writeData(0, 0x39);
	writeData(0, 0x14);
	writeData(0, 0x70);
	writeData(0, 0x56);
	writeData(0, 0x6C);
	delay(250);
	writeData(0, 0x38);
	writeData(0, 0x0C);
	clear();

	return 0;
}


void LCDAQMGPIO::printStr(char*str){
	for(uint8_t i=0; i<16; i++){
		// Null character
		if(str[i]==0){
			return;
		}
		count++;
		if(count>8){
			if(line==2){
				home();
			}else{
				secLine();
			}
		}
		writeData(0x40, str[i]);
	}
}

void LCDAQMGPIO::clear(){
	count = 0;
	line = 1;
	writeData(0, 0x01);
	delay(2);
}


void LCDAQMGPIO::home(){
	count = 0;
	line = 1;
	writeData(0, 0x02);
	delay(2);
}


void LCDAQMGPIO::secLine(){
	count = 0;
	line = 2;
	writeData(0, 0xC0);
}









