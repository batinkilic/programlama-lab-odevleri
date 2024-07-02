import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import json
import os


# Resim dosyalarının mevcut olup olmadığını kontrol eden fonksiyon
def dosya_mevcut_mu(dosya_adi):
    return os.path.isfile(dosya_adi)


# Pokemon sınıfı
class Pokemon:
    def __init__(self, isim, hasar_puani, resim_dosyasi):
        self._isim = isim
        self._hasar_puani = hasar_puani
        self._resim_dosyasi = resim_dosyasi

    def isim_al(self):
        return self._isim

    def hasar_puani_al(self):
        return self._hasar_puani

    def resim_al(self):
        return self._resim_dosyasi


# Deste sınıfı
class Deste:
    def __init__(self):
        self._kartlar = [
            Pokemon("Charmander", 50, "charmander.png"),
            Pokemon("Squirtle", 40, "squirtle.png"),
            Pokemon("Bulbasaur", 45, "bulbasaur.png"),
            Pokemon("Pikachu", 55, "pikachu.png"),
            Pokemon("Eevee", 30, "eevee.png"),
            Pokemon("Jigglypuff", 25, "jigglypuff.png"),
            Pokemon("Meowth", 35, "meowth.png"),
            Pokemon("Psyduck", 20, "psyduck.png"),
            Pokemon("Snorlax", 60, "snorlax.png"),
            Pokemon("Mewtwo", 70, "mewtwo.png")
        ]
        random.shuffle(self._kartlar)

    def kart_cek(self):
        return self._kartlar.pop() if self._kartlar else None


# Oyuncu sınıfı
class Oyuncu:
    def __init__(self, isim):
        self._isim = isim
        self._el = []

    def kart_cek(self, deste):
        kart = deste.kart_cek()
        if kart:
            self._el.append(kart)

    def kart_oyna(self, kart_indeksi):
        return self._el.pop(kart_indeksi)

    def el_al(self):
        return self._el

    def isim_al(self):
        return self._isim


# Oyun sınıfı
class Oyun:
    def __init__(self, oyuncu_turu):
        self._deste = Deste()
        self._kullanici = Oyuncu("Kullanıcı")
        self._bilgisayar = Oyuncu("Bilgisayar")
        self._ortadaki_kartlar = []
        self._kullanici_skor = 0
        self._bilgisayar_skor = 0
        self._oyuncu_turu = oyuncu_turu

        for _ in range(3):
            self._kullanici.kart_cek(self._deste)
            self._bilgisayar.kart_cek(self._deste)

        for _ in range(4):
            self._ortadaki_kartlar.append(self._deste.kart_cek())

    def tur_oyna(self, kullanici_karti_indeksi):
        kullanici_karti = self._kullanici.kart_oyna(kullanici_karti_indeksi)
        bilgisayar_karti_indeksi = random.randint(0, len(self._bilgisayar.el_al()) - 1)
        bilgisayar_karti = self._bilgisayar.kart_oyna(bilgisayar_karti_indeksi)

        if kullanici_karti.hasar_puani_al() > bilgisayar_karti.hasar_puani_al():
            self._kullanici_skor += 5
            kazanan = self._kullanici.isim_al()
            kazanan_oyuncu = self._kullanici
        else:
            self._bilgisayar_skor += 5
            kazanan = self._bilgisayar.isim_al()
            kazanan_oyuncu = self._bilgisayar

        if self._ortadaki_kartlar:
            kazanan_kart = self._ortadaki_kartlar.pop(random.randint(0, len(self._ortadaki_kartlar) - 1))
            kazanan_oyuncu._el.append(kazanan_kart)

        return (kullanici_karti, bilgisayar_karti, kazanan)

    def oyun_bitti_mi(self):
        return len(self._kullanici.el_al()) == 0 or len(self._bilgisayar.el_al()) == 0

    def skorlar_al(self):
        return (self._kullanici_skor, self._bilgisayar_skor)

    def oyun_durumunu_kaydet(self, dosya_adi):
        oyun_durumu = {
            "kullanici": {
                "isim": self._kullanici.isim_al(),
                "el": [(kart.isim_al(), kart.hasar_puani_al(), kart.resim_al()) for kart in self._kullanici.el_al()],
                "skor": self._kullanici_skor
            },
            "bilgisayar": {
                "isim": self._bilgisayar.isim_al(),
                "el": [(kart.isim_al(), kart.hasar_puani_al(), kart.resim_al()) for kart in self._bilgisayar.el_al()],
                "skor": self._bilgisayar_skor
            },
            "ortadaki_kartlar": [(kart.isim_al(), kart.hasar_puani_al(), kart.resim_al()) for kart in
                                 self._ortadaki_kartlar],
            "deste": [(kart.isim_al(), kart.hasar_puani_al(), kart.resim_al()) for kart in self._deste._kartlar]
        }
        with open(dosya_adi, 'w') as dosya:
            json.dump(oyun_durumu, dosya)

    def oyun_durumunu_yukle(self, dosya_adi):
        with open(dosya_adi, 'r') as dosya:
            oyun_durumu = json.load(dosya)

        self._kullanici = Oyuncu(oyun_durumu["kullanici"]["isim"])
        self._kullanici._el = [Pokemon(isim, hasar, resim) for isim, hasar, resim in oyun_durumu["kullanici"]["el"]]
        self._kullanici_skor = oyun_durumu["kullanici"]["skor"]

        self._bilgisayar = Oyuncu(oyun_durumu["bilgisayar"]["isim"])
        self._bilgisayar._el = [Pokemon(isim, hasar, resim) for isim, hasar, resim in oyun_durumu["bilgisayar"]["el"]]
        self._bilgisayar_skor = oyun_durumu["bilgisayar"]["skor"]

        self._ortadaki_kartlar = [Pokemon(isim, hasar, resim) for isim, hasar, resim in oyun_durumu["ortadaki_kartlar"]]
        self._deste._kartlar = [Pokemon(isim, hasar, resim) for isim, hasar, resim in oyun_durumu["deste"]]


# Oyun Arayüzü sınıfı
class OyunArayuzu:
    def __init__(self, root, oyun):
        self.root = root
        self.oyun = oyun

        self.root.title("Pokemon Kart Oyunu")

        self.kullanici_etiketi = tk.Label(root, text="Kullanıcı Kartları:")
        self.kullanici_etiketi.pack()

        self.kullanici_kartlari_frame = tk.Frame(root)
        self.kullanici_kartlari_frame.pack()

        self.bilgisayar_etiketi = tk.Label(root, text="Bilgisayar Kartları:")
        self.bilgisayar_etiketi.pack()

        self.bilgisayar_kartlari_frame = tk.Frame(root)
        self.bilgisayar_kartlari_frame.pack()

        self.ortadaki_kartlar_etiketi = tk.Label(root, text="Ortadaki Kartlar:")
        self.ortadaki_kartlar_etiketi.pack()

        self.ortadaki_kartlar_frame = tk.Frame(root)
        self.ortadaki_kartlar_frame.pack()

        self.skor_etiketi = tk.Label(root, text="Skorlar:")
        self.skor_etiketi.pack()

        self.skor_frame = tk.Frame(root)
        self.skor_frame.pack()

        self.kaydet_butonu = tk.Button(root, text="Kaydet", command=self.oyunu_kaydet)
        self.kaydet_butonu.pack(side=tk.LEFT)

        self.yukle_butonu = tk.Button(root, text="Yükle", command=self.oyunu_yukle)
        self.yukle_butonu.pack(side=tk.RIGHT)

        self.kartlari_guncelle()

    def kartlari_guncelle(self):
        for widget in self.kullanici_kartlari_frame.winfo_children():
            widget.destroy()

        for i, kart in enumerate(self.oyun._kullanici.el_al()):
            if dosya_mevcut_mu(kart.resim_al()):
                resim = Image.open(kart.resim_al())
                resim = resim.resize((100, 150), Image.Resampling.LANCZOS)
                resim = ImageTk.PhotoImage(resim)
                frame = tk.Frame(self.kullanici_kartlari_frame)
                button = tk.Button(frame, image=resim, command=lambda i=i: self.kart_oyna(i))
                button.image = resim  # Referansı saklamak için
                button.pack()
                label = tk.Label(frame, text=f"Hasar: {kart.hasar_puani_al()}")
                label.pack()
                frame.pack(side=tk.LEFT)
            else:
                print(f"Dosya bulunamadı: {kart.resim_al()}")

        for widget in self.bilgisayar_kartlari_frame.winfo_children():
            widget.destroy()

        for i, kart in enumerate(self.oyun._bilgisayar.el_al()):
            if dosya_mevcut_mu("kapali_kart.png"):
                resim = Image.open("kapali_kart.png")
                resim = resim.resize((100, 150), Image.Resampling.LANCZOS)
                resim = ImageTk.PhotoImage(resim)
                frame = tk.Frame(self.bilgisayar_kartlari_frame)
                button = tk.Button(frame, image=resim)
                button.image = resim  # Referansı saklamak için
                button.pack()
                label = tk.Label(frame, text=f"Bilgisayar Kartı {i + 1}")
                label.pack()
                frame.pack(side=tk.LEFT)
            else:
                print("Dosya bulunamadı: kapali_kart.png")

        for widget in self.ortadaki_kartlar_frame.winfo_children():
            widget.destroy()

        self.ortadaki_kart_dizileri = []
        for i in range(len(self.oyun._ortadaki_kartlar)):
            self.kapali_kart_goster(i)

        self.skorları_guncelle()

    def kapali_kart_goster(self, indeks):
        if dosya_mevcut_mu("kapali_kart.png"):
            resim = Image.open("kapali_kart.png")
            resim = resim.resize((100, 150), Image.Resampling.LANCZOS)
            resim = ImageTk.PhotoImage(resim)
            frame = tk.Frame(self.ortadaki_kartlar_frame)
            button = tk.Button(frame, image=resim)
            button.image = resim  # Referansı saklamak için
            button.pack()
            frame.pack(side=tk.LEFT)
            self.ortadaki_kart_dizileri.append(frame)
        else:
            print("Dosya bulunamadı: kapali_kart.png")

    def karti_goster(self, kart, frame):
        if dosya_mevcut_mu(kart.resim_al()):
            resim = Image.open(kart.resim_al())
            resim = resim.resize((100, 150), Image.Resampling.LANCZOS)
            resim = ImageTk.PhotoImage(resim)
            for widget in frame.winfo_children():
                widget.destroy()
            button = tk.Button(frame, image=resim)
            button.image = resim  # Referansı saklamak için
            button.pack()
            label = tk.Label(frame, text=f"Hasar: {kart.hasar_puani_al()}")
            label.pack()
        else:
            print(f"Dosya bulunamadı: {kart.resim_al()}")

    def skorları_guncelle(self):
        for widget in self.skor_frame.winfo_children():
            widget.destroy()

        kullanici_skor, bilgisayar_skor = self.oyun.skorlar_al()
        skor_text = f"Kullanıcı: {kullanici_skor} - Bilgisayar: {bilgisayar_skor}"
        label = tk.Label(self.skor_frame, text=skor_text)
        label.pack()

    def kart_oyna(self, kart_indeksi):
        kullanici_karti, bilgisayar_karti, kazanan = self.oyun.tur_oyna(kart_indeksi)

        # Kullanıcının ve bilgisayarın oynadığı kartları göster
        self.karti_goster(kullanici_karti, self.kullanici_kartlari_frame)
        self.karti_goster(bilgisayar_karti, self.bilgisayar_kartlari_frame)

        messagebox.showinfo("Tur Sonucu",
                            f"Kullanıcı: {kullanici_karti.isim_al()} ({kullanici_karti.hasar_puani_al()})\n"
                            f"Bilgisayar: {bilgisayar_karti.isim_al()} ({bilgisayar_karti.hasar_puani_al()})\n"
                            f"Kazanan: {kazanan}")

        if not self.oyun.oyun_bitti_mi():
            self.kartlari_guncelle()
        else:
            self.skorları_guncelle()
            kullanici_skor, bilgisayar_skor = self.oyun.skorlar_al()
            kazanan = "Kullanıcı" if kullanici_skor > bilgisayar_skor else "Bilgisayar"
            messagebox.showinfo("Oyun Bitti",
                                f"Oyun Bitti!\nKullanıcı: {kullanici_skor} - Bilgisayar: {bilgisayar_skor}\nKazanan: {kazanan}")
            self.root.quit()

    def oyunu_kaydet(self):
        self.oyun.oyun_durumunu_kaydet("oyun_durumu.json")
        messagebox.showinfo("Kaydet", "Oyun durumu kaydedildi.")

    def oyunu_yukle(self):
        self.oyun.oyun_durumunu_yukle("oyun_durumu.json")
        self.kartlari_guncelle()
        messagebox.showinfo("Yükle", "Oyun durumu yüklendi.")


def main():
    root = tk.Tk()
    oyun = Oyun("Kullanıcı")
    arayuz = OyunArayuzu(root, oyun)
    root.mainloop()


if __name__ == "__main__":
    main()
