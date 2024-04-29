from builtins import input

class Tilanne:
    def __init__(self):
        self.nykytilanne = 'Nalle Puhin koti'
        self.alkutarina ()

    def alkutarina(self):
        print("Tervetuloa puolenhehtaarin metsään, haluat nallepuhilta kartan jotta pääset kotiin (ja voitat pelin).")
        print("Sinun pitää viedä kaikille asukkaille tavarat joita he haluavat, jotta saat kartan.")
        print("Puolenhehtaarinmetsän kartta on seuraava:")
        print("Kanin kolo    Nasun koti")
        print(".         XXXX         .")
        print("Pöllön maja    Nalle Puhin koti")


    def vaihda_tilanne(self, uusi_tilanne):
        self.nykytilanne = uusi_tilanne

class Huone:
    def __init__(self, kuvaus):
        self.kuvaus = kuvaus
        self.esineet = []
        self.yhdistetyt_huoneet = {}
        self.esinetuotu = False




    def yhdista_huone(self, huone, suunta):
        self.yhdistetyt_huoneet[suunta] = huone

    def aseta_esine(self, esine):
        self.esineet.append(esine)

    def hae_esineet(self):
        return self.esineet

    def hae_tiedot(self):
        print(self.kuvaus)


class Reppu:
    def __init__(self):
        self.esineet = []

    def lisaa_esine(self, esine):
        self.esineet.append(esine)
        print(f"{esine} on lisätty reppuun")

    def hae_esineet(self):
            print(self.esineet)
            
    def palauta_kartta(self):
        if not self.esineet:
            return ""
        else:
            return self.esineet[0]
    

    def kayta_esine(self, esine):
    
        if esine in self.esineet:
            self.esineet.remove(esine)
            print(f"Käytit {esine}.")
        else:
            print("Sinulla ei ole kyseistä esinettä repussasi")

class Peli:
    def __init__(self):
        self.tilanne = Tilanne()
        self.repunsisalto = Reppu()
        self.huoneet = {
        'Nalle Puhin koti': Huone("Olet Nalle Puhin kotona. Nalle Puhilla on kartta, mutta saat sen kun tuot hunajaa(saa pöllöltä)"),
        'Nasun koti': Huone("Olet nasun kodissa täältä löytyy porkkanoita"),
        'Kanin kolo': Huone("Olet kanin kolossa! Kani haluaisi porkkanoita, kanilta löytyy kirja"),
        'Pöllön maja': Huone("Olet pöllön majassa! Haluan kirjan, sitten voin antaa hunajaa"),
        }
    #Huoneiden riippuvuudet toisistansa karttana se näyttäisi:
    #Kanin kolo Nasun koti
    # XXXX
    #Pöllön maja Nalle Puhin koti
    #ei voi liikkua vinottain
        self.huoneet['Nalle Puhin koti'].yhdista_huone(self.huoneet['Nasun koti'], 'ylös')
        self.huoneet['Nasun koti'].yhdista_huone(self.huoneet['Nalle Puhin koti'], 'alas')

        self.huoneet['Nasun koti'].yhdista_huone(self.huoneet['Kanin kolo'], 'vasen')
        self.huoneet['Kanin kolo'].yhdista_huone(self.huoneet['Nasun koti'], 'oikea')

        self.huoneet['Kanin kolo'].yhdista_huone(self.huoneet['Pöllön maja'], 'alas')
        self.huoneet['Pöllön maja'].yhdista_huone(self.huoneet['Kanin kolo'], 'ylös')

        self.huoneet['Pöllön maja'].yhdista_huone(self.huoneet['Nalle Puhin koti'], 'oikea')
        self.huoneet['Nalle Puhin koti'].yhdista_huone(self.huoneet['Pöllön maja'], 'vasen')


        # huoneissa olevat esineet
        self.huoneet['Nalle Puhin koti'].aseta_esine("Kartta")
        self.huoneet['Nasun koti'].aseta_esine("Porkkanoita")
        self.huoneet['Kanin kolo'].aseta_esine("Kirja")
        self.huoneet['Pöllön maja'].aseta_esine("Hunajaa")

    def liiku(self, suunta):
        nykyinen_huone = self.huoneet[self.tilanne.nykytilanne]
        if suunta in nykyinen_huone.yhdistetyt_huoneet:
            uusi_huone = nykyinen_huone.yhdistetyt_huoneet[suunta]
            self.tilanne.vaihda_tilanne(list(self.huoneet.keys())[list(self.huoneet.values()).index(uusi_huone)])
            uusi_huone.hae_tiedot()
        else:
            print("Et voi mennä tuohon suuntaan.")

    def kerää_esine(self, esine):
        nykyinen_huone = self.huoneet[self.tilanne.nykytilanne]
        if esine in nykyinen_huone.esineet:
            if nykyinen_huone == self.huoneet['Kanin kolo'] and "Porkkanoita" not in nykyinen_huone.esineet:
                print("Sinun täytyy antaa porkkanat Kanille saadaksesi kirjan.")
            elif nykyinen_huone == self.huoneet['Pöllön maja'] and "Kirja" not in nykyinen_huone.esineet:
                print("Sinun täytyy antaa kirja Pöllölle saadaksesi hunajaa.")
            elif nykyinen_huone == self.huoneet['Nalle Puhin koti'] and "Hunajaa" not in nykyinen_huone.esineet:
                print("Sinun täytyy antaa hunajaa Nalle Puhille saadaksesi kartan.")
            else:
                self.repunsisalto.lisaa_esine(esine)
                nykyinen_huone.esineet.remove(esine)
        else:
            print("Tätä esinettä ei ole täällä.")


    def kayta_esine(self, esine):
        nykyinen_huone = self.huoneet[self.tilanne.nykytilanne]

        if esine == "Porkkanoita" and nykyinen_huone == self.huoneet['Kanin kolo']:
            if "Porkkanoita" not in nykyinen_huone.esineet:  
                self.repunsisalto.kayta_esine("Porkkanoita")
                self.huoneet['Kanin kolo'].esineet.append("Porkkanoita") 
                print("Nyt voit ottaa kirjan")
        elif esine == "Kirja" and nykyinen_huone == self.huoneet['Pöllön maja']:
            self.repunsisalto.kayta_esine("Kirja")
            self.huoneet['Pöllön maja'].esineet.append("Kirja") 
            print("Pöllöltä löytyi hunajaa.")
        elif esine == "Hunajaa" and nykyinen_huone == self.huoneet['Nalle Puhin koti']:
            self.repunsisalto.kayta_esine("Hunajaa")
            self.huoneet['Nalle Puhin koti'].esineet.append("Hunajaa") 
            print("Nalle Puhilta löytyi kartta.")
        else:
            print("Et voi käyttää tätä esinettä tässä huoneessa.")




    def pelaa(self):
         while True:
            nykyinen_huone = self.huoneet[self.tilanne.nykytilanne]
            nykyinen_huone.hae_tiedot()
            print("\nMitä haluaisit tehdä?")
            print("1. Liiku")
            print("2. Ota esine reppuun")
            print("3. Anna esine")
            print("4. Repun sisältö")
     
            komento = input("> ")
            if komento == '1':
                suunta = input("Anna suunta (ylös, alas, vasen, oikea): ").lower()
                self.liiku(suunta)
            elif komento == '2':
                print("Esineet huoneessa: ", nykyinen_huone.esineet)
                esine = input("Kirjoita kerättävä esine: ")
                self.kerää_esine(esine)
            elif komento == '3':
                esine = input("Kirjoita annettava esine: ")
                self.kayta_esine(esine)
            elif komento == '4':
                self.repunsisalto.hae_esineet()    
            else:
                print("Virheellinen komento.")
            if self.repunsisalto.palauta_kartta() == "Kartta":    
                 print("Kartan avulla pääset kotiin! Voitit pelin!")
                 break
peli = Peli()

peli.pelaa()






# Ajatukseni on, että meillä on puolen hehtaarin metsä, jossa sijaitsevat Puhin talo, Nasun talo, Kanin kolo ja Pöllön puu. Puh omistaa kartan, jota tarvitaan tutkimusretken aloittamiseksi ja pelin voittamiseksi (kun saa kartan peli siis päättyy). Puh ei kuitenkaan luovuta karttaa ilman että saa vastineeksi hunajaa, jota löytyy Pöllöltä. Pöllö suostuu antamaan hunajan vastineeksi kirjasta, ja kirjan löydät Kanilta. Kani luopuu kirjasta, jos saa porkkanoita, jotka ovat Nasun hallussa.
# Tehtävänä on siis hakea esineet oikeista paikoista ja toimittaa ne oikeille henkilöille – tai tarkemmin sanottuna oikeisiin huoneisiin ja käyttää ne niissä.



# Toteutetaan tekstiseikkailuna Pythonilla:

# -Huoneet (satuhahmojen talot) joiden välillä pystytään siirtymään

# -Jokaisessa huoneessa on jokin tavara jonka voi lisätä reppuun (alkuehto pitää olla täytetty esim. kanille on pitänyt viedä porkkanat jotta saa kirjan)

# -Jokainen tavara on käytettävä tietyssä huoneessa, jotta peli etenee