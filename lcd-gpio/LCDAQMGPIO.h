//---------------------------------
// 2017/1/9

#ifndef LCDAQMGPIO_H
#define LCDAQMGPIO_H


//---------------------------------
// Constant



//---------------------------------
// Class

class LCDAQMGPIO{
private:
	//---------------------------------
	// Constant
	static const uint8_t i2cAdr = 0x3E;


	//---------------------------------
	// Variable

	uint8_t count;		// Character count in line
	uint8_t line;	// 1:1st line, 2:2nd line


	//---------------------------------
	// Function
	void writeData(uint8_t ctrl, uint8_t data);


public:
	//---------------------------------
	// Function
	LCDAQMGPIO();
	uint8_t init();
	void printStr(char*str);
	void clear();
	void home();
	void secLine();
};

#endif

