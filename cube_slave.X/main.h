#include <xc.h>
#include <pic18f25k80.h>
#include <stdio.h>
#include <stdlib.h>
#include "port.h"
#include "usart.h"

#define TRUE    1
#define FALSE   0

#define ON      1
#define OFF     0

void decodage();
void init_timer(void);
void affichage();