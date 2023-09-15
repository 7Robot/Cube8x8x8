# Gestion du port série (ftdi)
from serial import Serial

PORT = "/dev/ttyUSB0"
BAUDRATE = 115200


class LedCube:
    def __init__(self, nb_lignes, nb_colonnes, nb_etages, nb_pics=8):
        self.ser = None
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.nb_etages = nb_etages
        self.nb_pics = nb_pics
        # Matrice pour envoyer les infos de l'interface graphique au ftdi
        self.matrice_leds = None
        self.init_matrice_leds()

    def init_matrice_leds(self):
        self.matrice_leds = [
            [0] * self.nb_colonnes for _ in range(self.nb_lignes * self.nb_etages)
        ]

    def get_bytes(self):
        octets_rouges = [[0] * self.nb_lignes for _ in range(self.nb_etages)]
        octets_bleus = [[0] * self.nb_lignes for _ in range(self.nb_etages)]

        for k in range(self.nb_etages):
            for i in range(self.nb_lignes):
                for j in range(self.nb_colonnes):
                    if i % 2 == 0 and (j // 4) % 2 == 1:
                        l = 1
                        c = -4
                    elif i % 2 == 1 and (j // 4) % 2 == 0:
                        l = -1
                        c = 4
                    else:
                        l = 0
                        c = 0

                    if self.matrice_leds[i + l + 8 * k][j + c] == 1:
                        octets_rouges[k][i] = octets_rouges[k][i] + 2**j
                    elif self.matrice_leds[i + l + 8 * k][j + c] == 2:
                        octets_bleus[k][i] = octets_bleus[k][i] + 2**j
                    elif self.matrice_leds[i + l + 8 * k][j + c] == 3:
                        octets_rouges[k][i] = octets_rouges[k][i] + 2**j
                        octets_bleus[k][i] = octets_bleus[k][i] + 2**j

        return octets_rouges, octets_bleus

    def Envoyer(self):
        octets_rouges, octets_bleus = self.get_bytes()
        try:
            if self.ser is None:
                self.ser = Serial(PORT, BAUDRATE)
            # On envoie la sauce !
            for k in range(self.nb_etages):
                # each PIC controls 2x4 adjacent bicolor led columns
                for p in range(self.nb_pics):
                    self.ser.write(octets_bleus[k][p].to_bytes())
                    self.ser.write(octets_rouges[k][p].to_bytes())
        except Exception as error:
            print(f"Serial error: {error}")
