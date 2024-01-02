#include <iostream>
#include <cmath>
#include <array>
using namespace std;
class Nokta {
private:
    double x;
    double y;

public:
    // Parametresiz yapıcı
    Nokta() : x(0.0), y(0.0) {}

    // Tek parametreli yapıcı
    Nokta(double value) : x(value), y(value) {}

    // İki parametreli yapıcı
    Nokta(double x_val, double y_val) : x(x_val), y(y_val) {}

    // Başka bir noktanın kopyasını alan yapıcı
    Nokta(const Nokta &other) : x(other.getX()), y(other.getY()) {}

    // Başka bir nokta ve ofset değerleri ile yapıcı
    Nokta(const Nokta &other, double offset_x, double offset_y) : x(other.getX() + offset_x), y(other.getY() + offset_y) {}

    // Getter ve setter metotları
    double getX() const {
        return x;
    }

    double getY() const {
        return y;
    }

    void setX(double x_val) {
        x = x_val;
    }

    void set(double x_val,double y_val){
        x = x_val;
        y = y_val;
    }

    void setY(double y_val) {
        y = y_val;
    }

    void setCoordinates(double x_val, double y_val) {
        x = x_val;
        y = y_val;
    }

    double mesafe(const Nokta &other) const {
        double dx = x - other.getX();
        double dy = y - other.getY();
        return std::sqrt(dx * dx + dy * dy);
    }

    // Diğer metotlar
    std::string toString() const {
        return "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
    }

    void yazdir() const {
        std::cout << toString() << std::endl;
    }
};

class DogruParcasi {
private:
    Nokta baslangicNoktasi;
    Nokta bitisNoktasi;

public:
    // İki uç noktayı Nokta nesnesi olarak alan yapıcı
    DogruParcasi(const Nokta &start, const Nokta &end) : baslangicNoktasi(start), bitisNoktasi(end) {}

    // Başka bir DogruParcasi nesnesi alıp onun bir kopyasını yeni bir DogruParcasi nesnesi olarak oluşturan yapıcı
    DogruParcasi(const DogruParcasi &other) : baslangicNoktasi(other.getBaslangicNoktasi()), bitisNoktasi(other.getBitisNoktasi()) {}

    // Doğru parçasının orta noktası , parçanın uzunluğu ve eğimi değerlerini alan yapıcı
    DogruParcasi(const Nokta &ortaNokta, double uzunluk, double egim) {
        // Ortanın x ve y koordinatlarını al
        double ortaX = ortaNokta.getX();
        double ortaY = ortaNokta.getY();

        // Uç noktaların x ve y koordinatlarını hesapla
        double yarimUzunluk = uzunluk / 2.0;
        double deltaX = yarimUzunluk * std::cos(egim);
        double deltaY = yarimUzunluk * std::sin(egim);

        double baslangicX = ortaX - deltaX;
        double baslangicY = ortaY - deltaY;
        double bitisX = ortaX + deltaX;
        double bitisY = ortaY + deltaY;

        // Uç noktaları ayarla
        baslangicNoktasi.setCoordinates(baslangicX, baslangicY);
        bitisNoktasi.setCoordinates(bitisX, bitisY);
    }

    // Getter metotları
    Nokta getBaslangicNoktasi() const {
        return baslangicNoktasi;
    }

    Nokta getBitisNoktasi() const {
        return bitisNoktasi;
    }

    // Setter metotları
    void setBaslangicNoktasi(const Nokta &start) {
        baslangicNoktasi = start;
    }

    void setBitisNoktasi(const Nokta &end) {
        bitisNoktasi = end;
    }


    double uzunluk() const {
        double dx = bitisNoktasi.getX() - baslangicNoktasi.getX();
        double dy = bitisNoktasi.getY() - baslangicNoktasi.getY();
        return std::sqrt(dx * dx + dy * dy);
    }

    Nokta kesisimNoktasi(const Nokta &nokta) const {
        // Doğru parçası ile verilen noktadan dik inen doğruyu bulma
        double m = (bitisNoktasi.getY() - baslangicNoktasi.getY()) / (bitisNoktasi.getX() - baslangicNoktasi.getX());
        double b = baslangicNoktasi.getY() - m * baslangicNoktasi.getX();

        // Verilen noktadan dik inen doğrunun kesişim noktasını bulma
        double x = (nokta.getY() - b) / m;
        double y = m * x + b;

        return Nokta(x, y);
    }

    Nokta ortaNokta() const {
        double x = (baslangicNoktasi.getX() + bitisNoktasi.getX()) / 2.0;
        double y = (baslangicNoktasi.getY() + bitisNoktasi.getY()) / 2.0;

        return Nokta(x, y);
    }
    std::string toString() const {
        return "Dogru Parcasi: " + baslangicNoktasi.toString() + " - " + bitisNoktasi.toString();
    }

    void yazdir() const {
        std::cout << toString() << std::endl;
    }
};

class Daire {
private:
    Nokta merkez;
    double yaricap;

public:
    // Merkez ve yarıçapı parametre olarak alan yapıcı
    Daire(const Nokta &center, double radius) : merkez(center), yaricap(radius) {}

    // Başka bir Daire nesnesinin kopyasını alan yapıcı
    Daire(const Daire &other) : merkez(other.getMerkez()), yaricap(other.getYaricap()) {}

    // Başka bir Daire nesnesi ve pozitif bir x değeri alarak, parametre olarak alınan Daire nesnesini yarıçapı x ile çarpılmış olarak kopyalayan yapıcı
    Daire(const Daire &other, double scale) : merkez(other.getMerkez()), yaricap(other.getYaricap() * scale) {}

    // Getter metotları
    Nokta getMerkez() const {
        return merkez;
    }

    double getYaricap() const {
        return yaricap;
    }


    double alan() const {
        return M_PI * yaricap * yaricap;
    }

    double cevre() const {
        return 2.0 * M_PI * yaricap;
    }

    int kesisim(const Daire &other) const {
        double mesafe = merkezUzaklik(other.getMerkez());

        if (mesafe < std::fabs(yaricap - other.getYaricap()))
            return 0; // İç içe daireler, birbirini içeriyor
        else if (mesafe <= yaricap + other.getYaricap())
            return 1; // Kesişen daireler
        else
            return 2; // Kesişmeyen daireler
    }

    std::string toString() const {
        return "Daire: Merkez " + merkez.toString() + ", Yaricap " + std::to_string(yaricap);
    }

    void yazdir() const {
        std::cout << toString() << std::endl;
    }

private:
    // İki nokta arasındaki uzaklığı hesaplayan yardımcı fonksiyon
    double merkezUzaklik(const Nokta &other) const {
        double dx = merkez.getX() - other.getX();
        double dy = merkez.getY() - other.getY();
        return std::sqrt(dx * dx + dy * dy);
    }
};

class Ucgen {
private:
    Nokta nokta1;
    Nokta nokta2;
    Nokta nokta3;

public:
    // Üç tane Nokta nesnesi alan yapıcı
    Ucgen(const Nokta &point1, const Nokta &point2, const Nokta &point3)
            : nokta1(point1), nokta2(point2), nokta3(point3) {}

    // Getter metotları
    Nokta getNokta1() const {
        return nokta1;
    }

    Nokta getNokta2() const {
        return nokta2;
    }

    Nokta getNokta3() const {
        return nokta3;
    }

    // Setter metotları
    void setNokta1(const Nokta &point) {
        nokta1 = point;
    }

    void setNokta2(const Nokta &point) {
        nokta2 = point;
    }

    void setNokta3(const Nokta &point) {
        nokta3 = point;
    }

    std::string toString() const {
        return "Üçgen: " + nokta1.toString() + ", " + nokta2.toString() + ", " + nokta3.toString();
    }

    void yazdir() const {
        std::cout << toString() << std::endl;
    }



    double alan() const {

        double a = nokta1.mesafe(nokta2);
        double b = nokta2.mesafe(nokta3);
        double c = nokta3.mesafe(nokta1);

        double s = (a + b + c) / 2.0;
        return std::sqrt(s * (s - a) * (s - b) * (s - c));
    }

    double cevre() const {
        DogruParcasi kenar1(nokta1, nokta2);
        DogruParcasi kenar2(nokta2, nokta3);
        DogruParcasi kenar3(nokta3, nokta1);

        return kenar1.uzunluk() + kenar2.uzunluk() + kenar3.uzunluk();
    }

    std::array<double, 3> acilar() const {
        double a = nokta2.mesafe(nokta3);
        double b = nokta3.mesafe(nokta1);
        double c = nokta1.mesafe(nokta2);

        double angleA = std::acos((b * b + c * c - a * a) / (2.0 * b * c));
        double angleB = std::acos((c * c + a * a - b * b) / (2.0 * c * a));
        double angleC = std::acos((a * a + b * b - c * c) / (2.0 * a * b));

        return {angleA, angleB, angleC};
    }
};





int main() {
    setlocale(LC_ALL, "Turkish");
    //Nokta
    cout << endl << "NOKTA SINIFI İÇİN TEST ÇIKTILARI:" << endl;
    Nokta n1;
    Nokta n2(5);
    Nokta n3(3, 4);
    Nokta n4(n3);
    Nokta n5(n3, 1, -1);

    cout << "Oluşturulan 5 noktanın x ve y değerleri:" << endl;
    n1.yazdir();
    n2.yazdir();
    n3.yazdir();
    n4.yazdir();
    n5.yazdir();

    cout << "1. ve 2. noktaların güncel x ve y değerleri:" << endl;
    n1.setX(10);
    n1.yazdir();
    n2.set(25, 30);
    n2.yazdir();

    //Dogru Parcasi
    cout << endl << "DOGRUPARCASI SINIFI İÇİN TEST SONUÇLARI:" << endl;
    Nokta n11;
    Nokta n21(3, 4);
    DogruParcasi dp(n11, n21);
    DogruParcasi dp2(dp);
    DogruParcasi dp3(n21, 10, 45);

    cout << "Oluşturulan 3 doğru parçasının başlangıç ve bitiş noktaları:" << endl;
    dp.yazdir();
    dp2.yazdir();
    dp3.yazdir();

    cout << "2. doğru parçasının başlangıç ve bitiş noktaları:" << endl;
    dp2.setBaslangicNoktasi(Nokta());
    dp2.yazdir();

    cout << "1. doğru parçası için uzunluk değeri: " << dp.uzunluk() << endl;
    cout << "1. doğru parçası içib orta nokta: " << dp.ortaNokta().toString() << endl;

    //Daire
    cout << endl << "DAIRE SINIFI İÇİN TEST SONUÇLARI:" << endl;
    Nokta merkez1(0, 0);
    Daire d1(merkez1, 5);
    Daire d2(d1);
    Daire d3(d2, 3);

    cout << "Daire 1: ";
    d1.yazdir();
    cout << "Alan: " << d1.alan() << ", Çevre: " << d1.cevre() << endl;

    cout << "Daire 2: ";
    d2.yazdir();
    cout << "Alan: " << d2.alan() << ", Çevre: " << d2.cevre() << endl;

    cout << "Daire 3: ";
    d3.yazdir();
    cout << "Alan: " << d3.alan() << ", Çevre: " << d3.cevre() << endl;

    cout << "Daire 1 ve Daire 2 Kesişim Durumu: " << d1.kesisim(d2) << endl;
    cout << "Daire 1 ve Daire 3 Kesişim Durumu: " << d1.kesisim(d3) << endl;

    //Ucgen
    cout << endl << "UCGEN SINIFI İÇİN TEST SONUÇLARI:" << endl;
    Ucgen ucgen(Nokta(0, 0), Nokta(4, 0), Nokta(0, 3));

    cout << ucgen.toString() << endl;
    cout << "Alan: " << ucgen.alan() << endl;
    cout << "Çevre: " << ucgen.cevre() << endl;

    std::array<double, 3> acilar= ucgen.acilar();
    cout << "Açılar: " << acilar[0] << ", " << acilar[1] << ", " << acilar[2] << endl;


    return 0;
}
