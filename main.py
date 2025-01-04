import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, 
                           QLabel, QVBoxLayout, QWidget, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt

class SteganografiUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dosya Gizleme Uygulaması")
        self.setMinimumSize(500, 350)
        
        # Ana widget ve layout oluştur
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Başlık
        baslik = QLabel("Dosya Gizleme Uygulaması")
        baslik.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # Dosya tipi seçici
        self.dosya_tipi_combo = QComboBox()
        self.dosya_tipi_combo.addItems(["JPEG Dosyası", "MP4 Dosyası"])
        self.dosya_tipi_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                min-width: 200px;
                margin: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.dosya_tipi_combo)
        
        # Gizleme bölümü
        gizleme_baslik = QLabel("RAR Dosyasını Gizle")
        gizleme_baslik.setStyleSheet("font-weight: bold;")
        layout.addWidget(gizleme_baslik)
        
        self.ana_dosya_label = QLabel("Seçilen Dosya: Henüz seçilmedi")
        self.rar_label = QLabel("Seçilen RAR: Henüz seçilmedi")
        
        ana_dosya_sec_btn = QPushButton("Dosya Seç")
        rar_sec_btn = QPushButton("RAR Dosyası Seç")
        gizle_btn = QPushButton("Gizle")
        
        layout.addWidget(self.ana_dosya_label)
        layout.addWidget(ana_dosya_sec_btn)
        layout.addWidget(self.rar_label)
        layout.addWidget(rar_sec_btn)
        layout.addWidget(gizle_btn)
        
        # Ayırıcı çizgi
        ayirici = QLabel("")
        ayirici.setStyleSheet("border-bottom: 1px solid #ccc; margin: 20px 0;")
        layout.addWidget(ayirici)
        
        # Çıkarma bölümü
        cikarma_baslik = QLabel("Gizlenmiş RAR Dosyasını Çıkar")
        cikarma_baslik.setStyleSheet("font-weight: bold;")
        layout.addWidget(cikarma_baslik)
        
        self.gizli_dosya_label = QLabel("Seçilen Dosya: Henüz seçilmedi")
        gizli_dosya_sec_btn = QPushButton("Dosya Seç")
        cikar_btn = QPushButton("RAR'ı Çıkar")
        
        layout.addWidget(self.gizli_dosya_label)
        layout.addWidget(gizli_dosya_sec_btn)
        layout.addWidget(cikar_btn)
        
        # Dosya yolları
        self.ana_dosya_path = ""
        self.rar_path = ""
        self.gizli_dosya_path = ""
        
        # Buton bağlantıları
        ana_dosya_sec_btn.clicked.connect(self.ana_dosya_sec)
        rar_sec_btn.clicked.connect(self.rar_sec)
        gizle_btn.clicked.connect(self.gizle)
        gizli_dosya_sec_btn.clicked.connect(self.gizli_dosya_sec)
        cikar_btn.clicked.connect(self.cikar)
        
        # Stil
        self.setStyleSheet("""
            QPushButton {
                padding: 8px;
                min-width: 200px;
                margin: 5px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                margin: 5px;
            }
        """)

    def get_dosya_filtresi(self):
        if self.dosya_tipi_combo.currentText() == "JPEG Dosyası":
            return "JPEG Dosyaları (*.jpg *.jpeg)"
        else:
            return "MP4 Dosyaları (*.mp4)"

    def ana_dosya_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", self.get_dosya_filtresi())
        if dosya:
            self.ana_dosya_path = dosya
            self.ana_dosya_label.setText(f"Seçilen Dosya: {dosya}")

    def rar_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "RAR Dosyası Seç", "", "RAR Dosyaları (*.rar)")
        if dosya:
            self.rar_path = dosya
            self.rar_label.setText(f"Seçilen RAR: {dosya}")

    def gizli_dosya_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Tüm Dosyalar (*.jpg *.jpeg *.mp4)")
        if dosya:
            self.gizli_dosya_path = dosya
            self.gizli_dosya_label.setText(f"Seçilen Dosya: {dosya}")

    def gizle(self):
        if not self.ana_dosya_path or not self.rar_path:
            QMessageBox.warning(self, "Hata", "Lütfen gerekli dosyaları seçin!")
            return
        
        dosya_tipi = ".jpg" if self.dosya_tipi_combo.currentText() == "JPEG Dosyası" else ".mp4"
        output_path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", f"Dosya (*{dosya_tipi})")
        if output_path:
            try:
                hide_rar_in_file(self.ana_dosya_path, self.rar_path, output_path)
                QMessageBox.information(self, "Başarılı", "RAR dosyası başarıyla gizlendi!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

    def cikar(self):
        if not self.gizli_dosya_path:
            QMessageBox.warning(self, "Hata", "Lütfen dosya seçin!")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "RAR'ı Kaydet", "", "RAR Dosyaları (*.rar)")
        if output_path:
            try:
                extract_rar_from_file(self.gizli_dosya_path, output_path)
                QMessageBox.information(self, "Başarılı", "RAR dosyası başarıyla çıkarıldı!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

def hide_rar_in_file(file_path, rar_path, output_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    with open(rar_path, 'rb') as rar_file:
        rar_data = rar_file.read()
    
    marker = b'RARSTART'
    combined_data = file_data + marker + rar_data
    
    with open(output_path, 'wb') as output_file:
        output_file.write(combined_data)

def extract_rar_from_file(file_path, output_rar_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    
    marker = b'RARSTART'
    rar_start = data.find(marker)
    
    if rar_start == -1:
        raise Exception("Bu dosyada gizlenmiş RAR bulunamadı!")
    
    rar_data = data[rar_start + len(marker):]
    
    with open(output_rar_path, 'wb') as rar_file:
        rar_file.write(rar_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = SteganografiUygulamasi()
    pencere.show()
    sys.exit(app.exec_())
