#include <xc.h>
#include "main.h"
//=============================================================================
// 7ROBOT
// Created by Alexandre Proux & Robin Beilvert
// Cube 8x8x8
//============================================================github=============
//
//
//=============================================================================

//****************************************************************************************
//                    CONFIGURATION BITS PIC18F25K80
//****************************************************************************************

// Configuration register

// CONFIG1L
#pragma config RETEN = OFF      // VREG Sleep Enable bit (Ultra low-power regulator is Disabled (Controlled by REGSLP bit))
#pragma config INTOSCSEL = HIGH // LF-INTOSC Low-power Enable bit (LF-INTOSC in High-power mode during Sleep)
#pragma config SOSCSEL = DIG    // SOSC Power Selection and mode Configuration bits (Digital (SCLKI) mode)
#pragma config XINST = OFF      // Extended Instruction Set (Disabled)

// CONFIG1H
#pragma config FOSC = INTIO2    // Oscillator (Internal RC oscillator)
#pragma config PLLCFG = ON    // PLL x4 Enable bit (Disabled)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor (Disabled)
#pragma config IESO = ON       // Internal External Oscillator Switch Over Mode (Disabled)

// CONFIG2L
#pragma config PWRTEN = OFF     // Power Up Timer (Disabled)
#pragma config BOREN = SBORDIS  // Brown Out Detect (Enabled in hardware, SBOREN disabled)
#pragma config BORV = 3         // Brown-out Reset Voltage bits (1.8V)
#pragma config BORPWR = ZPBORMV // BORMV Power level (ZPBORMV instead of BORMV is selected)

// CONFIG2H
#pragma config WDTEN = OFF      // Watchdog Timer (WDT disabled in hardware; SWDTEN bit disabled)
#pragma config WDTPS = 1048576  // Watchdog Postscaler (1:1048576)

// CONFIG3H
#pragma config CANMX = PORTB    // ECAN Mux bit (ECAN TX and RX pins are located on RB2 and RB3, respectively)
#pragma config MSSPMSK = MSK7   // MSSP address masking (7 Bit address masking mode)
#pragma config MCLRE = OFF      // Master Clear Enable (MCLR Disabled, RG5 Enabled)

// CONFIG4L
#pragma config STVREN = ON      // Stack Overflow Reset (Enabled)
#pragma config BBSIZ = BB2K     // Boot Block Size (2K word Boot Block size)

// CONFIG5L
#pragma config CP0 = OFF        // Code Protect 00800-01FFF (Disabled)
#pragma config CP1 = OFF        // Code Protect 02000-03FFF (Disabled)
#pragma config CP2 = OFF        // Code Protect 04000-05FFF (Disabled)
#pragma config CP3 = OFF        // Code Protect 06000-07FFF (Disabled)

// CONFIG5H
#pragma config CPB = OFF        // Code Protect Boot (Disabled)
#pragma config CPD = OFF        // Data EE Read Protect (Disabled)

// CONFIG6L
#pragma config WRT0 = OFF       // Table Write Protect 00800-03FFF (Disabled)
#pragma config WRT1 = OFF       // Table Write Protect 04000-07FFF (Disabled)
#pragma config WRT2 = OFF       // Table Write Protect 08000-0BFFF (Disabled)
#pragma config WRT3 = OFF       // Table Write Protect 0C000-0FFFF (Disabled)

// CONFIG6H
#pragma config WRTC = OFF       // Config. Write Protect (Disabled)
#pragma config WRTB = OFF       // Table Write Protect Boot (Disabled)
#pragma config WRTD = OFF       // Data EE Write Protect (Disabled)

// CONFIG7L
#pragma config EBTR0 = OFF      // Table Read Protect 00800-03FFF (Disabled)
#pragma config EBTR1 = OFF      // Table Read Protect 04000-07FFF (Disabled)
#pragma config EBTR2 = OFF      // Table Read Protect 08000-0BFFF (Disabled)
#pragma config EBTR3 = OFF      // Table Read Protect 0C000-0FFFF (Disabled)

// CONFIG7H
#pragma config EBTRB = OFF      // Table Read Protect Boot (Disabled)


// DEFINE LISTE
#define etage0  PORTCbits.RC0
#define etage1  PORTCbits.RC1
#define etage2  PORTCbits.RC2
#define etage3  PORTCbits.RC3
#define etage4  PORTCbits.RC4
#define etage5  PORTCbits.RC5
#define etage6  PORTCbits.RC6
#define etage7  PORTCbits.RC7

#define clock PORTAbits.RA0

// GLOBAL
char tampon = 0;
int compteur_isr = 0;
char compteur_clock = 0;
char flag_reception = 0;
char stockage_uart[140] = 0;

void interrupt low_priority high_isr(void) { // interruption de l'UART

    if (RC2IF /*&& PIE3bits.TX2IE*/) {
        tampon = RCREG2;
        if (compteur_isr == 128) {
            compteur_isr = 0;
        }
        stockage_uart[compteur_isr] = tampon;
        compteur_isr++;

    }
    RC2IF = 0; // On met le flag a 0
}


void main(void) {
    //char msg1[80] = "MASTER IS READY \n \r";
    char mux = 0;
    long i =0;
    initPorts(); // Initialize ports to startup state
    initComms(); // Initialize the serial port
    //init_timer();
    int delaimain = 0;

    while (1) {
        if (compteur_clock == 8) {
            compteur_clock = 0;
        }
        multiplexeur(compteur_clock);
        compteur_clock++;
    }
}

void multiplexeur(char n) {
    long d = 0;
    char a = 0;

    etage0 = 0;
    for (d = 0; d < 4; d++) {
    }
    etage1 = 0;
    for (d = 0; d < 4; d++) {
    }
    etage2 = 0;
    for (d = 0; d < 4; d++) {
    }
    etage3 = 0;
    for (d = 0; d < 4; d++) {
    }
    etage4 = 0;
    for (d = 0; d < 4; d++) {
    }
    etage5 = 0;
    for (d = 0; d < 4; d++) {
    }
    etage6 = 0;
    for (d = 0; d < 4; d++) {
    }
    etage7 = 0;
    for (d = 0; d < 4; d++) {
    }

    for (a = 0; a < 16; a++) {
        writeDataToUART(stockage_uart[a + 16 * n]);
    }

    switch (n) {

        case 0:
            etage0 = 1;
            break;

        case 1:
            etage1 = 1;
            break;

        case 2:
            etage2 = 1;
            break;

        case 3:
            etage3 = 1;
            break;

        case 4:
            etage4 = 1;
            break;

        case 5:
            etage5 = 1;
            break;

        case 6:
            etage6 = 1;
            break;

        case 7:
            etage7 = 1;
            break;
    }
    for (d = 0; d < 250; d++) {
    }
}
