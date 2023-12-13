class Tir:
    def __init__(self, gelis_zamani, plaka,  ulke, _20_ton_adet, _30_ton_adet, yuk_miktari, maliyet):
        self.plaka = plaka
        self.gelis_zamani = gelis_zamani
        self.yuk_bilgisi = {
            "ulke":ulke,
            "20_ton_adet":_20_ton_adet,
            "30_ton_adet":_30_ton_adet,
            "yuk_miktari":yuk_miktari,
            "maliyet":maliyet
        }

    def __str__(self):
        return self.plaka

    def yuk_indir(self, istif_alani):
        return (f"{self.plaka} isimli tır yüklerini {istif_alani}na indiriyor.\nİndirme işlemi tamamlandı.")

class Gemi:
    def __init__(self, gelis_zamani, gemi_adi,kapasite,ulke):
        self.gelis_zamani = gelis_zamani
        self.gemi_adi = gemi_adi
        self.kapasite = kapasite
        self.yuk_bilgisi = {
            "ulke": ulke,
            "20_ton_adet": 0,
            "30_ton_adet": 0,
            "yuk_miktari": 0,
            "maliyet": 0
        }


    def yuk_yukle(self, yuk):
        if yuk["20_ton_adet"] == 1:
            self.yuk_bilgisi["20_ton_adet"] += 1
        elif yuk["30_ton_adet"] == 1:
            self.yuk_bilgisi["30_ton_adet"] += 1

        self.yuk_bilgisi["yuk_miktari"] += yuk["yuk_miktari"]

        print(f"{self.gemi_adi} isimli gemiye {yuk['yuk_miktari']} ton yüklendi.")
class yuk:
    def __init__(self, ulke, miktar,maliyet):
        self.ulke = ulke
        self.miktar = miktar
        self.maliyet = maliyet

import csv

def tir_sira(t):
    return t.plaka

tirlar = []
gemiler = []
ulkeler = ("Mordor","Neverland","Lilliputa","Occania")
_1_nolu_istif_alani = []
_2_nolu_istif_alani = []
yuklenecek_gemi = None

def istif_alani_oplam_yuk(istif_alani):
    toplam = 0
    for yuk in istif_alani:
        toplam += yuk["yuk_miktari"]

    return toplam

with open("olaylar.csv", newline='', encoding='cp1252') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for line in reader:
        tir = Tir(int(line[0]), line[1], line[2], int(line[3]), int(line[4]), int(line[5]), int(line[6]))
        tirlar.append(tir)

with open("gemiler.csv", newline='', encoding='cp1252') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for line in reader:
        gemi = Gemi(int(line[0]), line[1], int(line[2]), line[3])
        gemiler.append(gemi)


for zaman in range(1,tirlar[-1].gelis_zamani+1):
    yuk_indirecek_tirlar =list(filter(lambda obj: obj.gelis_zamani == zaman,tirlar))
    yuk_indirecek_tirlar.sort(key=tir_sira)

    if len(yuk_indirecek_tirlar) == 0:
        print(f"{zaman} zamanında yük indirecek bir tır bulunamadı.")
    else:
        print(f"{zaman} zamanında yük indiren tırlar:")
        for t in yuk_indirecek_tirlar:

            if istif_alani_oplam_yuk( _1_nolu_istif_alani) + t.yuk_bilgisi["yuk_miktari"] <= 750:
                _1_nolu_istif_alani.append(t.yuk_bilgisi)
                print(t.yuk_indir("1 numaralı istif alanı"))
                if istif_alani_oplam_yuk( _1_nolu_istif_alani) == 750:
                    print("1 numaralı istif alanı doldu.")
            else:
                _2_nolu_istif_alani.append(t.yuk_bilgisi)
                print(t.yuk_indir("2 numaralı istif alanı"))
                if istif_alani_oplam_yuk( _1_nolu_istif_alani) == 750:
                    print("2 numaralı istif alanı doldu.")

    if yuklenecek_gemi == None:
        yuklenecek_gemi = next(filter(lambda obj: obj.gelis_zamani == zaman,gemiler),None)

    if yuklenecek_gemi == None:
        print(f"{zaman} zamanında yüklenecek bir gemi bulunamadı.")
    else:
        pop_sira = -1

        for konteyner in _1_nolu_istif_alani:
            if yuklenecek_gemi.yuk_bilgisi["yuk_miktari"] + konteyner["yuk_miktari"] <= yuklenecek_gemi.kapasite\
                    and yuklenecek_gemi.yuk_bilgisi["ulke"] == konteyner["ulke"]:
                yuklenecek_gemi.yuk_yukle(_1_nolu_istif_alani.pop())