#include <xc.h>
#include "main.h"
//=============================================================================
// 7ROBOT
// Created by Alexandre Proux & Robin Beilvert
// Cube 8x8x8
//=============================================================================
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
#pragma config PLLCFG = ON     // PLL x4 Enable bit (Disabled)
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


// DEFINE LIST

#define slave 7

#define ledB1 PORTAbits.RA0
#define ledB2 PORTAbits.RA3
#define ledB3 PORTAbits.RA6
#define ledB4 PORTCbits.RC3
#define ledB5 PORTCbits.RC7
#define ledB6 PORTBbits.RB3
#define ledB7 PORTAbits.RA7
#define ledB8 PORTCbits.RC5

#define ledR1 PORTAbits.RA1
#define ledR2 PORTAbits.RA2
#define ledR3 PORTCbits.RC0
#define ledR4 PORTCbits.RC2
#define ledR5 PORTCbits.RC1
#define ledR6 PORTBbits.RB2
#define ledR7 PORTCbits.RC6
#define ledR8 PORTCbits.RC4


char tampon = 0;
char MASK[8] = {0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b00001000, 0b00000100, 0b00000010, 0b00000001};
char stock_led[20] = 0;
int compteur = 0;
char compteur_clock = 0;
char state_clock = 0;
char led_state[2][8] = 0; // Ligne 0 : Bleu, Ligne 1 : Rouge

void interrupt low_priority high_isr(void) {
    if (RC2IF) { // a chaque interruption on stock la valeur de RCREG2 dans un tableau
        tampon = RCREG2;
        if (compteur == 16) {
            compteur = 0;
        }
        stock_led[compteur] = tampon;
        compteur++;
    }
    RC2IF = 0; // On remet le flag a 0
}


void main(void) {
    initPorts(); // Initialize ports to startup state
    initComms(); // Initialize the serial port
    while (1) {
        decodage();
        affichage();
    }
}


void decodage() {
    char a = 0;
    for (a = 0; a < 8; a++) {
        if (MASK[a] & stock_led[2 * slave]) 
        {
            led_state[0][a] = 1;
        } else {
            led_state[0][a] = 0;
        }

        if (MASK[a] & stock_led[2 * slave + 1]) {
            led_state[1][a] = 1;
        } else {
            led_state[1][a] = 0;
        }
    }
}


void affichage() {
        ledB1 = led_state[0][0];
        ledB2 = led_state[0][1];
        ledB3 = led_state[0][2];
        ledB4 = led_state[0][3];
        ledB5 = led_state[0][4];
        ledB6 = led_state[0][5];
        ledB7 = led_state[0][6];
        ledB8 = led_state[0][7];

        ledR1 = led_state[1][0];
        ledR2 = led_state[1][1];
        ledR3 = led_state[1][2];
        ledR4 = led_state[1][3];
        ledR5 = led_state[1][4];
        ledR6 = led_state[1][5];
        ledR7 = led_state[1][6];
        ledR8 = led_state[1][7];
}
