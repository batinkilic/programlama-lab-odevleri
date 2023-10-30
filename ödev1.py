from functools import reduce




def k_kucuk(k, liste):
    if k > len(liste):
        return "Hatalı k değeri! Liste boyutundan küçük bir değer girin."
    else:
        for i in range(k):
            min_index = i
            for j in range(i + 1, len(liste)):
                if liste[j] < liste[min_index]:
                    min_index = j
            liste[i], liste[min_index] = liste[min_index], liste[i]
        return liste[k - 1]


def en_yakin_cift(hedef, liste):
    en_kucuk_fark = float('inf')  # Sonsuz büyük bir değerle başlat
    en_yakin_cift = None

    for i in range(len(liste)):
        for j in range(i + 1, len(liste)):
            fark = abs(liste[i] + liste[j] - hedef)
            if fark < en_kucuk_fark:
                en_kucuk_fark = fark
                en_yakin_cift = (liste[i], liste[j])

    return en_yakin_cift


def tekrar_eden_elemanlar(liste):
    tekrar_eden_elemanlar_sonuc = list({x for x in liste if liste.count(x) > 1})
    return tekrar_eden_elemanlar_sonuc


def matris_carpimi(matris1, matris2):
    # Matrislerin satır ve sütun sayılarını al
    satir_matris1 = len(matris1)
    sutun_matris1 = len(matris1[0])
    satir_matris2 = len(matris2)
    sutun_matris2 = len(matris2[0])

    # Matris çarpımını hesapla ve sonucu list comprehension ile oluştur
    matris_carpimi_sonuc = [
        [
            sum(a * b for a, b in zip(satir_matris1, sutun_matris2))
            for sutun_matris2 in zip(*matris2)
        ]
        for satir_matris1 in matris1
    ]

    return matris_carpimi_sonuc


def kelime_frekansi(dosya_yolu):
    try:
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            metin = dosya.read().split()
            kelime_frekans_sonuc = reduce(lambda x, y: {**x, **{y: x.get(y, 0) + 1}}, metin, {})
        return kelime_frekans_sonuc
    except FileNotFoundError:
        return "Dosya bulunamadı!"
    except Exception as e:
        return str(e)


def en_kucuk_deger(liste):
    # Liste boş ise None (veya isteğe bağlı olarak bir hata mesajı) döndür
    if not liste:
        return None
    # Liste sadece bir eleman içeriyorsa o elemanı döndür
    if len(liste) == 1:
        return liste[0]
    # Listenin ilk elemanını ve geri kalanını ayır
    ilk_eleman = liste[0]
    geri_kalan = liste[1:]
    # Geri kalan listeyi recursive olarak kontrol et ve en küçük değeri bul
    en_kucuk_geri_kalan = en_kucuk_deger(geri_kalan)
    # İlk eleman ile geri kalanın en küçük değerini karşılaştır ve en küçüğü döndür
    return ilk_eleman if ilk_eleman < en_kucuk_geri_kalan else en_kucuk_geri_kalan


def karekok(N, x0=1, maxiter=10, tol=1e-10):
    iterasyon = 0

    while iterasyon < maxiter:
        iterasyon += 1
        x1 = 0.5 * (x0 + N / x0)
        hata = abs(x1 - x0)

        if hata < tol:
            return x1
        else:
            x0 = x1

    return f"{maxiter} iterasyonda sonuca ulaşılamadı. 'tol' veya 'maxiter' değerlerini değiştirin."


def eb_ortak_bolen(a, b):
    if b == 0:
        return a
    else:
        return eb_ortak_bolen(b, a % b)


def asal_veya_degil(sayi, bolen=2):
    if sayi <= 1:
        return False
    elif bolen * bolen > sayi:
        return True
    elif sayi % bolen == 0:
        return False
    else:
        return asal_veya_degil(sayi, bolen + 1)


def hizlandirici(n, k=1, fibk=0, fibk1=1):
    if n == k:
        return fibk1
    else:
        return hizlandirici(n, k + 1, fibk1, fibk + fibk1)



def main():
    while True:
        print("\n*** Menü ***")
        print("1. En Küçük Elemanı Bulma")
        print("2. En Yakın Çifti Bulma")
        print("3. Tekrar Eden Elemanları Bulma")
        print("4. Matris Çarpımı")
        print("5  Frekans bulma")
        print("6  Listedeki En Küçük Elemanı Bulma")
        print("7. Karekök Bulma")
        print("8. Ebob Bulma")
        print("9. Asal Sayı Kontrolü")
        print("10. Fibonacci Sayısı Hesaplama")
        print("11. Çıkış")

        secim = input("Yapmak istediğiniz işlemi seçin (1-11): ")




        if secim == "1":
            # En Küçük Elemanı Bulma işlemi için girdileri al ve sonucu ekrana yaz
            k_degeri = int(input("k değerini girin: "))
            liste = list(map(int, input("Listeyi girin (örneğin: 7 10 4 3 20 15): ").split()))

            sonuc = k_kucuk(k_degeri, liste)
            print(f"{k_degeri}. en küçük eleman: {sonuc}")

            pass
        elif secim == "2":
            # En Yakın Çifti Bulma işlemi için girdileri al ve sonucu ekrana yaz
            hedef_sayi = int(input("Hedef sayıyı girin: "))
            liste = list(map(int, input("Listeyi girin (örneğin: 10 22 28 29 30 40): ").split()))

            sonuc = en_yakin_cift(hedef_sayi, liste)
            print(f"{hedef_sayi} sayısına en yakın çift sayılar: {sonuc}")

            pass
        elif secim == "3":
            # Tekrar Eden Elemanları Bulma işlemi için girdileri al ve sonucu ekrana yaz
            liste = list(map(int, input("Listeyi girin (örneğin: 1 2 3 2 1 5 6 5): ").split()))

            tekrar_edenler = tekrar_eden_elemanlar(liste)
            print("Tekrar eden elemanlar:", tekrar_edenler)
            pass
        elif secim == "4":
            # Matris Çarpımı işlemi için girdileri al ve sonucu ekrana yaz
            print("Matris1:")
            matris1 = [list(map(int, input().split())) for _ in range(int(input("Satır sayısını girin: ")))]

            print("Matris2:")
            matris2 = [list(map(int, input().split())) for _ in range(int(input("Satır sayısını girin: ")))]

            sonuc = matris_carpimi(matris1, matris2)
            print("Çarpım Matrisi:")
            for row in sonuc:
                print(row)
            pass
        elif secim == "5":
            # Kelime frekanslarını bulmak için dosyo yolunu gir ve frekansları yaz
            dosya_yolu = input("Dosya yolunu girin: ")
            sonuc = kelime_frekansi(dosya_yolu)
            for kelime, frekans in sonuc.items():
                print(f"{kelime}={frekans}")
            pass
        elif secim == "6":
            # listedeki en küçük değeri bulan özyinelemeli fonksiyon için liste gir ve sonucu yaz
            liste1 = list(map(int, input("Listeyi girin (örneğin: 1 4 6 91 2 5): ").split()))

            sonuc1 = en_kucuk_deger(liste1)
            print(f"En küçük değer: {sonuc1}")
            pass
        elif secim == "7":
            # Karekök Bulma işlemi için girdileri al ve sonucu ekrana yaz
            N = int(input("Karekök alınacak sayıyı girin: "))
            x0_str = input(
                "İlk tahmini girin (isteğe bağlı, varsayılan: 0.1, boş bırakmak için Enter'a basın): ").strip()
            maxiter_str = input(
                "Maksimum iterasyon sayısını girin (isteğe bağlı, varsayılan: 10, boş bırakmak için Enter'a basın): ").strip()

            if x0_str:
                x0 = float(x0_str)
                if maxiter_str:
                    maxiter = int(maxiter_str)
                    sonuc = karekok(N, x0, maxiter)
                else:
                    sonuc = karekok(N, x0)
            else:
                sonuc = karekok(N)

            print(f"{N}'in karekökü: {sonuc}")

            pass
        elif secim == "8":
            # Ebob Bulma işlemi için girdileri al ve sonucu ekrana yaz

            sayi1 = int(input("Birinci sayıyı girin: "))
            sayi2 = int(input("İkinci sayıyı girin: "))

            sonuc = eb_ortak_bolen(sayi1, sayi2)
            print(f"{sayi1} ve {sayi2} sayılarının en büyük ortak böleni: {sonuc}")

            pass
        elif secim == "9":
            # Asal Sayı Kontrolü işlemi için girdileri al ve sonucu ekrana yaz
            sayi = int(input("Bir sayı girin: "))
            sonuc = asal_veya_degil(sayi)
            print(f"{sayi} sayısı asal mı? {sonuc}")
            pass
        elif secim == "10":
            # Fibonacci Sayısı Hesaplama işlemi için girdileri al ve sonucu ekrana yaz
            n = int(input("Fibonacci dizisinin kaçıncı terimini hesaplamak istersiniz? "))
            sonuc = hizlandirici(n)
            print(f"Fibonacci dizisinin {n}. terimi: {sonuc}")
            pass
        elif secim == "11":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
