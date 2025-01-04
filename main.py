import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, 
                           QLabel, QVBoxLayout, QWidget, QMessageBox)
from PyQt5.QtCore import Qt

class SteganografiUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JPEG-RAR Steganografi Uygulaması")
        self.setMinimumSize(500, 300)
        
        # Ana widget ve layout oluştur
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Başlık
        baslik = QLabel("JPEG-RAR Steganografi Uygulaması")
        baslik.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # Gizleme bölümü
        gizleme_baslik = QLabel("RAR Dosyasını JPEG İçine Gizle")
        gizleme_baslik.setStyleSheet("font-weight: bold;")
        layout.addWidget(gizleme_baslik)
        
        self.jpeg_label = QLabel("Seçilen JPEG: Henüz seçilmedi")
        self.rar_label = QLabel("Seçilen RAR: Henüz seçilmedi")
        
        jpeg_sec_btn = QPushButton("JPEG Dosyası Seç")
        rar_sec_btn = QPushButton("RAR Dosyası Seç")
        gizle_btn = QPushButton("Gizle")
        
        layout.addWidget(self.jpeg_label)
        layout.addWidget(jpeg_sec_btn)
        layout.addWidget(self.rar_label)
        layout.addWidget(rar_sec_btn)
        layout.addWidget(gizle_btn)
        
        # Ayırıcı çizgi
        ayirici = QLabel("")
        ayirici.setStyleSheet("border-bottom: 1px solid #ccc; margin: 20px 0;")
        layout.addWidget(ayirici)
        
        # Çıkarma bölümü
        cikarma_baslik = QLabel("JPEG'den RAR Dosyasını Çıkar")
        cikarma_baslik.setStyleSheet("font-weight: bold;")
        layout.addWidget(cikarma_baslik)
        
        self.gizli_jpeg_label = QLabel("Seçilen JPEG: Henüz seçilmedi")
        gizli_jpeg_sec_btn = QPushButton("JPEG Dosyası Seç")
        cikar_btn = QPushButton("RAR'ı Çıkar")
        
        layout.addWidget(self.gizli_jpeg_label)
        layout.addWidget(gizli_jpeg_sec_btn)
        layout.addWidget(cikar_btn)
        
        # Dosya yolları
        self.jpeg_path = ""
        self.rar_path = ""
        self.gizli_jpeg_path = ""
        
        # Buton bağlantıları
        jpeg_sec_btn.clicked.connect(self.jpeg_sec)
        rar_sec_btn.clicked.connect(self.rar_sec)
        gizle_btn.clicked.connect(self.gizle)
        gizli_jpeg_sec_btn.clicked.connect(self.gizli_jpeg_sec)
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

    def jpeg_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "JPEG Dosyası Seç", "", "JPEG Dosyaları (*.jpg *.jpeg)")
        if dosya:
            self.jpeg_path = dosya
            self.jpeg_label.setText(f"Seçilen JPEG: {dosya}")

    def rar_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "RAR Dosyası Seç", "", "RAR Dosyaları (*.rar)")
        if dosya:
            self.rar_path = dosya
            self.rar_label.setText(f"Seçilen RAR: {dosya}")

    def gizli_jpeg_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "JPEG Dosyası Seç", "", "JPEG Dosyaları (*.jpg *.jpeg)")
        if dosya:
            self.gizli_jpeg_path = dosya
            self.gizli_jpeg_label.setText(f"Seçilen JPEG: {dosya}")

    def gizle(self):
        if not self.jpeg_path or not self.rar_path:
            QMessageBox.warning(self, "Hata", "Lütfen JPEG ve RAR dosyalarını seçin!")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", "JPEG Dosyaları (*.jpg *.jpeg)")
        if output_path:
            try:
                hide_rar_in_jpeg(self.jpeg_path, self.rar_path, output_path)
                QMessageBox.information(self, "Başarılı", "RAR dosyası başarıyla JPEG içine gizlendi!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

    def cikar(self):
        if not self.gizli_jpeg_path:
            QMessageBox.warning(self, "Hata", "Lütfen JPEG dosyasını seçin!")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "RAR'ı Kaydet", "", "RAR Dosyaları (*.rar)")
        if output_path:
            try:
                extract_rar_from_jpeg(self.gizli_jpeg_path, output_path)
                QMessageBox.information(self, "Başarılı", "RAR dosyası başarıyla çıkarıldı!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

def hide_rar_in_jpeg(jpeg_path, rar_path, output_path):
    with open(jpeg_path, 'rb') as jpeg_file:
        jpeg_data = jpeg_file.read()
    
    with open(rar_path, 'rb') as rar_file:
        rar_data = rar_file.read()
    
    marker = b'RARSTART'
    combined_data = jpeg_data + marker + rar_data
    
    with open(output_path, 'wb') as output_file:
        output_file.write(combined_data)

def extract_rar_from_jpeg(jpeg_path, output_rar_path):
    with open(jpeg_path, 'rb') as file:
        data = file.read()
    
    marker = b'RARSTART'
    rar_start = data.find(marker)
    
    if rar_start == -1:
        raise Exception("Bu JPEG dosyasında gizlenmiş RAR bulunamadı!")
    
    rar_data = data[rar_start + len(marker):]
    
    with open(output_rar_path, 'wb') as rar_file:
        rar_file.write(rar_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = SteganografiUygulamasi()
    pencere.show()
    sys.exit(app.exec_())
