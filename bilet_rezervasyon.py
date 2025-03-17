import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton,
    QRadioButton, QGroupBox, QComboBox, QDateEdit, QCheckBox, QListWidget, QMessageBox,
    QGridLayout, QSystemTrayIcon, QStyle, QDialog
)
from PyQt6.QtCore import QDate, Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


# Ek müşteri bilgileri için dialog
class AdditionalCustomerDialog(QDialog):
    def __init__(self, seatNumber, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{seatNumber} Numaralı Koltuk - Müşteri Bilgileri")
        layout = QGridLayout(self)

        # nameEdit
        self.nameEdit = QLineEdit()
        # tcEdit (tam 11 hane, rakam)
        tcRegex = QRegularExpression("^[0-9]{0,11}$")
        self.tcEdit = QLineEdit()
        self.tcEdit.setValidator(QRegularExpressionValidator(tcRegex))
        self.tcEdit.setMaxLength(11)
        # phoneEdit (tam 10 hane, rakam)
        phoneRegex = QRegularExpression("^[0-9]{0,10}$")
        self.phoneEdit = QLineEdit()
        self.phoneEdit.setValidator(QRegularExpressionValidator(phoneRegex))
        self.phoneEdit.setMaxLength(10)
        # emailEdit
        self.emailEdit = QLineEdit()
        # maleRadio, femaleRadio
        self.maleRadio = QRadioButton("Erkek")
        self.femaleRadio = QRadioButton("Kadın")

        layout.addWidget(QLabel("Ad Soyad:"), 0, 0)
        layout.addWidget(self.nameEdit, 0, 1)
        layout.addWidget(QLabel("TC Kimlik:"), 1, 0)
        layout.addWidget(self.tcEdit, 1, 1)
        layout.addWidget(QLabel("Telefon:"), 2, 0)
        layout.addWidget(self.phoneEdit, 2, 1)
        layout.addWidget(QLabel("E-Posta:"), 3, 0)
        layout.addWidget(self.emailEdit, 3, 1)
        genderLayout = QHBoxLayout()
        genderLayout.addWidget(self.maleRadio)
        genderLayout.addWidget(self.femaleRadio)
        layout.addWidget(QLabel("Cinsiyet:"), 4, 0)
        layout.addLayout(genderLayout, 4, 1)

        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton("Tamam")
        self.okButton.clicked.connect(self.validateAndAccept)
        self.cancelButton = QPushButton("İptal")
        self.cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout, 5, 0, 1, 2)

    def getData(self):
        """Form verilerini sözlük olarak döndürür."""
        name = self.nameEdit.text().strip()
        tc = self.tcEdit.text().strip()
        phone = self.phoneEdit.text().strip()
        email = self.emailEdit.text().strip()
        gender = "Erkek" if self.maleRadio.isChecked() else "Kadın"
        return {"name": name, "tc": tc, "phone": phone, "email": email, "gender": gender}

    def validateAndAccept(self):
        """Form verilerini kontrol edip, doğrulama sağlanırsa dialog'u onaylar."""
        data = self.getData()
        if not data["name"] or not data["tc"] or not data["phone"] or not data["email"]:
            QMessageBox.warning(self, "Uyarı", "Tüm alanlar doldurulmalıdır!")
            return
        if len(data["tc"]) != 11:
            QMessageBox.warning(self, "Uyarı", "TC Kimlik 11 haneli olmalıdır!")
            return
        if len(data["phone"]) != 10:
            QMessageBox.warning(self, "Uyarı", "Telefon 10 haneli olmalıdır!")
            return
        if data["gender"] not in ["Erkek", "Kadın"]:
            QMessageBox.warning(self, "Uyarı", "Lütfen cinsiyet seçiniz!")
            return
        self.accept()


class BiletRezervasyon(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Otobüs Bilet Rezervasyon Sistemi")
        self.setGeometry(100, 100, 1100, 650)

        # Sabit şehir listesi (10 şehir)
        self.cityList = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Gaziantep", "Kayseri",
                         "Mersin"]
        # Sepet toplamı için değişken
        self.cartTotal = 0

        mainLayout = QHBoxLayout(self)

        # ------------ SOL PANEL ------------
        leftLayout = QVBoxLayout()

        # Müşteri Bilgileri
        customerGroup = QGroupBox("Müşteri Bilgileri")
        gridCust = QGridLayout()
        self.nameInput = QLineEdit()  # nameInput
        tcRegex = QRegularExpression("^[0-9]{0,11}$")
        self.tcInput = QLineEdit()  # tcInput
        self.tcInput.setValidator(QRegularExpressionValidator(tcRegex))
        self.tcInput.setMaxLength(11)
        phoneRegex = QRegularExpression("^[0-9]{0,10}$")
        self.phoneInput = QLineEdit()  # phoneInput
        self.phoneInput.setValidator(QRegularExpressionValidator(phoneRegex))
        self.phoneInput.setMaxLength(10)
        self.emailInput = QLineEdit()  # emailInput
        gridCust.addWidget(QLabel("Ad Soyad:"), 0, 0)
        gridCust.addWidget(self.nameInput, 0, 1)
        gridCust.addWidget(QLabel("TC Kimlik:"), 1, 0)
        gridCust.addWidget(self.tcInput, 1, 1)
        gridCust.addWidget(QLabel("Telefon:"), 2, 0)
        gridCust.addWidget(self.phoneInput, 2, 1)
        gridCust.addWidget(QLabel("E-Posta:"), 3, 0)
        gridCust.addWidget(self.emailInput, 3, 1)
        customerGroup.setLayout(gridCust)

        # Cinsiyet
        genderGroup = QGroupBox("Cinsiyet")
        self.maleRadio = QRadioButton("Erkek")  # maleRadio
        self.femaleRadio = QRadioButton("Kadın")  # femaleRadio
        genderLayout = QHBoxLayout()
        genderLayout.addWidget(self.maleRadio)
        genderLayout.addWidget(self.femaleRadio)
        genderGroup.setLayout(genderLayout)

        # Otobüs Firması
        companyGroup = QGroupBox("Otobüs Firması")
        self.companyCombo = QComboBox()  # companyCombo
        self.companyCombo.addItems(["Kamil Koç", "İstanbul Seyahat", "Lüks Artvin", "Kale Seyahat"])
        companyLayout = QVBoxLayout()
        companyLayout.addWidget(self.companyCombo)
        companyGroup.setLayout(companyLayout)

        # Gidiş-Dönüş seçimi
        self.roundTripCheck = QCheckBox("Gidiş-Dönüş bileti almak istiyorum")  # roundTripCheck

        # Şehir Seçimi: Gidiş ve Dönüş
        self.departureCityCombo = QComboBox()  # departureCityCombo
        self.arrivalCityCombo = QComboBox()  # arrivalCityCombo
        self.departureCityCombo.addItems(self.cityList)
        self.departureCityCombo.currentIndexChanged.connect(self.updateArrivalCities)
        self.updateArrivalCities()
        cityGroup = QGroupBox("Şehir Seçimi")
        cityLayout = QGridLayout()
        cityLayout.addWidget(QLabel("Kalkış Şehri:"), 0, 0)
        cityLayout.addWidget(self.departureCityCombo, 0, 1)
        cityLayout.addWidget(QLabel("Varış Şehri:"), 1, 0)
        cityLayout.addWidget(self.arrivalCityCombo, 1, 1)
        cityGroup.setLayout(cityLayout)

        # Tarih ve Saat Seçimi
        self.departureDate = QDateEdit()  # departureDate
        self.departureDate.setCalendarPopup(True)
        self.departureDate.setDate(QDate.currentDate())
        self.departureDate.setMinimumDate(QDate.currentDate())

        self.returnDate = QDateEdit()  # returnDate
        self.returnDate.setCalendarPopup(True)
        self.returnDate.setDate(QDate.currentDate().addDays(1))
        self.returnDate.setMinimumDate(QDate.currentDate())
        self.returnDate.setEnabled(False)

        self.departureTimeCombo = QComboBox()  # departureTimeCombo
        self.returnTimeCombo = QComboBox()  # returnTimeCombo
        self.fillTimeComboboxes()
        self.returnTimeCombo.setEnabled(False)
        self.roundTripCheck.stateChanged.connect(self.enableReturnDate)

        dateGroup = QGroupBox("Tarih ve Saat Seçimi")
        dateLayout = QGridLayout()
        dateLayout.addWidget(QLabel("Gidiş Tarihi:"), 0, 0)
        dateLayout.addWidget(self.departureDate, 0, 1)
        dateLayout.addWidget(QLabel("Gidiş Saati:"), 0, 2)
        dateLayout.addWidget(self.departureTimeCombo, 0, 3)
        dateLayout.addWidget(QLabel("Dönüş Tarihi:"), 1, 0)
        dateLayout.addWidget(self.returnDate, 1, 1)
        dateLayout.addWidget(QLabel("Dönüş Saati:"), 1, 2)
        dateLayout.addWidget(self.returnTimeCombo, 1, 3)
        dateGroup.setLayout(dateLayout)

        leftLayout.addWidget(customerGroup)
        leftLayout.addWidget(genderGroup)
        leftLayout.addWidget(companyGroup)
        leftLayout.addWidget(cityGroup)
        leftLayout.addWidget(dateGroup)
        leftLayout.addWidget(self.roundTripCheck)

        # ------------ SAĞ PANEL ------------
        rightLayout = QVBoxLayout()

        # Koltuk Seçimi (5x10 grid, toplam 50 koltuk)
        self.seatChecks = []  # seatChecks
        seatGroup = QGroupBox("Koltuk Seçimi")
        seatLayout = QGridLayout()
        seatNumber = 1
        for i in range(5):
            for j in range(10):
                cb = QCheckBox(str(seatNumber))
                seatLayout.addWidget(cb, i, j)
                self.seatChecks.append(cb)
                seatNumber += 1
        seatGroup.setLayout(seatLayout)

        # Satın Alınan Biletler Listesi
        self.ticketList = QListWidget()  # ticketList
        ticketGroup = QGroupBox("Satın Alınan Biletler")
        vboxTicket = QVBoxLayout()
        vboxTicket.addWidget(self.ticketList)
        ticketGroup.setLayout(vboxTicket)

        # Güncel Seçim Fiyatı ve Sepet Tutarı Etiketleri
        self.priceLabel = QLabel("Fiyat: 0 TL")  # Seçili biletlerin anlık toplamı
        self.cartTotalLabel = QLabel("Sepet Tutarı: 0 TL")  # Listeye eklenen toplam tutar

        # Butonlar
        self.buyButton = QPushButton("Satın Al")
        self.buyButton.clicked.connect(self.buyTicket)
        self.clearButton = QPushButton("Temizle")
        self.clearButton.clicked.connect(self.clearAll)

        rightLayout.addWidget(seatGroup)
        rightLayout.addWidget(ticketGroup)
        rightLayout.addWidget(self.priceLabel)
        rightLayout.addWidget(self.cartTotalLabel)
        rightLayout.addWidget(self.buyButton)
        rightLayout.addWidget(self.clearButton)

        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        # System Tray Icon
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.trayIcon.setVisible(True)

    def updateArrivalCities(self):
        """Gidiş şehri seçildiğinde, dönüş şehri listesini günceller."""
        selectedCity = self.departureCityCombo.currentText()
        self.arrivalCityCombo.clear()
        filteredCities = [city for city in self.cityList if city != selectedCity]
        self.arrivalCityCombo.addItems(filteredCities)

    def fillTimeComboboxes(self):
        """Her yarım saatlik dilimlerle zaman combobox'larını doldurur."""
        times = []
        for hour in range(24):
            times.append(f"{hour:02d}:00")
            times.append(f"{hour:02d}:30")
        self.departureTimeCombo.addItems(times)
        self.returnTimeCombo.addItems(times)

    def enableReturnDate(self):
        """Gidiş-Dönüş bileti seçilmişse, dönüş tarih ve saat seçimlerini aktif eder."""
        enabled = self.roundTripCheck.isChecked()
        self.returnDate.setEnabled(enabled)
        self.returnTimeCombo.setEnabled(enabled)

    def buyTicket(self):
        """Bilet satın alma işlemi:
           - Ana form verileri doğrulanır.
           - Seçilen koltuk sayısına göre, ilk bilet ana formdan,
             diğerleri için ek müşteri bilgileri dialog'u açılır.
           - Satın alındıktan sonra, seçilen koltuklar kilitlenir (tekrar seçilemez).
           - Fiyat hesaplanır ve hem anlık seçim hem de sepet tutarı güncellenir.
        """
        # Ana form doğrulamaları
        if not self.nameInput.text().strip() or not self.tcInput.text().strip():
            QMessageBox.warning(self, "Uyarı", "Ad Soyad ve TC Kimlik boş olamaz!")
            return
        if len(self.tcInput.text()) != 11:
            QMessageBox.warning(self, "Uyarı", "TC Kimlik 11 haneli olmalıdır!")
            return
        if not self.phoneInput.text().strip() or not self.emailInput.text().strip():
            QMessageBox.warning(self, "Uyarı", "Telefon ve E-Posta boş olamaz!")
            return
        if len(self.phoneInput.text()) != 10:
            QMessageBox.warning(self, "Uyarı", "Telefon 10 haneli olmalıdır!")
            return
        if not (self.maleRadio.isChecked() or self.femaleRadio.isChecked()):
            QMessageBox.warning(self, "Uyarı", "Lütfen cinsiyet seçiniz!")
            return

        depCity = self.departureCityCombo.currentText()
        arrCity = self.arrivalCityCombo.currentText()
        if depCity == arrCity:
            QMessageBox.warning(self, "Uyarı", "Gidiş ve Dönüş şehirleri aynı olamaz!")
            return

        depDate = self.departureDate.date()
        retDate = self.returnDate.date()
        depTime = self.departureTimeCombo.currentText()
        retTime = self.returnTimeCombo.currentText()

        if self.roundTripCheck.isChecked():
            if retDate < depDate:
                QMessageBox.warning(self, "Uyarı", "Dönüş tarihi, gidiş tarihinden önce olamaz!")
                return
            if depDate.daysTo(retDate) > 30:
                QMessageBox.warning(self, "Uyarı",
                                    "Dönüş tarihi, gidiş tarihinden en fazla 30 gün sonrasına kadar olabilir!")
                return
            if depDate == retDate and retTime <= depTime:
                QMessageBox.warning(self, "Uyarı", "Aynı gün içinde dönüş saati, gidiş saatinden önce olamaz!")
                return

        selectedSeats = [cb.text() for cb in self.seatChecks if cb.isChecked() and cb.isEnabled()]
        if not selectedSeats:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir koltuk seçiniz!")
            return

        # Ana formdaki müşteri bilgileri (ilk koltuk)
        tcMasked = self.tcInput.text()[:3] + "****" + self.tcInput.text()[-2:]
        mainCustomer = {
            "name": self.nameInput.text().strip(),
            "tc": tcMasked,
            "phone": self.phoneInput.text().strip(),
            "email": self.emailInput.text().strip(),
            "gender": "Erkek" if self.maleRadio.isChecked() else "Kadın"
        }
        tickets = [(selectedSeats[0], mainCustomer)]

        # Ek müşteri formları (birden fazla koltuk seçilmişse)
        if len(selectedSeats) > 1:
            for seat in selectedSeats[1:]:
                dialog = AdditionalCustomerDialog(seat, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    custData = dialog.getData()
                    tcMaskedExtra = custData["tc"][:3] + "****" + custData["tc"][-2:]
                    custData["tc"] = tcMaskedExtra
                    tickets.append((seat, custData))
                else:
                    QMessageBox.warning(self, "Uyarı", "Ek müşteri bilgileri girilmedi, işlem iptal!")
                    return

        # Fiyat hesaplama: Tek gidiş 350 TL, gidiş-dönüş 600 TL
        if self.roundTripCheck.isChecked():
            pricePerTicket = 600
        else:
            pricePerTicket = 350
        currentPrice = len(selectedSeats) * pricePerTicket
        # Anlık seçim fiyatı güncelleniyor
        self.priceLabel.setText(f"Fiyat: {currentPrice} TL")
        # Sepet tutarına ekleniyor
        self.cartTotal += currentPrice
        self.cartTotalLabel.setText(f"Sepet Tutarı: {self.cartTotal} TL")

        company = self.companyCombo.currentText()
        # Satın alınan her bilet bilgisi listeye ekleniyor ve ilgili koltuk kilitleniyor
        for seat, customer in tickets:
            ticketInfo = (
                f"Ad Soyad: {customer['name']} ({customer['tc']}) | "
                f"Cinsiyet: {customer['gender']} | "
                f"Firma: {company} | "
                f"Koltuk: {seat} | "
                f"Gidiş: {depCity} {depDate.toString(Qt.DateFormat.ISODate)} {depTime}"
            )
            if self.roundTripCheck.isChecked():
                ticketInfo += f" | Dönüş: {arrCity} {retDate.toString(Qt.DateFormat.ISODate)} {retTime}"
            else:
                ticketInfo += f" | Varış: {arrCity}"
            ticketInfo += f" | Tel: {customer['phone']} | E-Posta: {customer['email']}"
            self.ticketList.addItem(ticketInfo)
            # İlgili koltuk checkbox'ı kilitleniyor
            for cb in self.seatChecks:
                if cb.text() == seat:
                    cb.setChecked(False)
                    cb.setEnabled(False)
                    break

        self.trayIcon.showMessage("Bilet Satın Alındı", f"Toplam Tutar: {currentPrice} TL",
                                  QSystemTrayIcon.MessageIcon.Information)

    def clearAll(self):
        """Tüm form alanlarını temizler ve satın alınmış koltukları tekrar seçilebilir hale getirir."""
        self.nameInput.clear()
        self.tcInput.clear()
        self.phoneInput.clear()
        self.emailInput.clear()
        self.maleRadio.setChecked(False)
        self.femaleRadio.setChecked(False)
        self.companyCombo.setCurrentIndex(0)
        self.departureCityCombo.setCurrentIndex(0)
        self.updateArrivalCities()
        self.departureDate.setDate(QDate.currentDate())
        self.returnDate.setDate(QDate.currentDate().addDays(1))
        self.roundTripCheck.setChecked(False)
        # Tüm koltuklar yeniden aktif edilir
        for cb in self.seatChecks:
            cb.setChecked(False)
            cb.setEnabled(True)
        self.ticketList.clear()
        self.priceLabel.setText("Fiyat: 0 TL")
        self.cartTotal = 0
        self.cartTotalLabel.setText("Sepet Tutarı: 0 TL")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BiletRezervasyon()
    window.show()
    sys.exit(app.exec())