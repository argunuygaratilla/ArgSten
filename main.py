import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, 
                           QLabel, QVBoxLayout, QWidget, QMessageBox, QComboBox,
                           QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os

class FileProcessThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, mode, file_path, rar_path, output_path):
        super().__init__()
        self.mode = mode
        self.file_path = file_path
        self.rar_path = rar_path
        self.output_path = output_path

    def run(self):
        try:
            if self.mode == "hide":
                self.hide_rar_in_file()
            else:
                self.extract_rar_from_file()
            self.finished.emit(True, "İşlem başarıyla tamamlandı!")
        except Exception as e:
            self.finished.emit(False, str(e))

    def hide_rar_in_file(self):
        with open(self.file_path, 'rb') as file:
            file_data = file.read()
        
        with open(self.rar_path, 'rb') as archive_file:
            archive_data = archive_file.read()
        
        # Dosya uzantısına göre marker belirle
        archive_ext = os.path.splitext(self.rar_path)[1].lower()
        if archive_ext == '.rar':
            marker = b'RARSTART'
        else:  # .zip için
            marker = b'ZIPSTART'
        
        total_size = len(file_data) + len(archive_data)
        processed_size = 0
        
        with open(self.output_path, 'wb') as output_file:
            # Ana dosyayı yaz
            chunk_size = 1024 * 1024  # 1MB chunks
            for i in range(0, len(file_data), chunk_size):
                chunk = file_data[i:i + chunk_size]
                output_file.write(chunk)
                processed_size += len(chunk)
                progress = (processed_size * 100) // total_size
                self.progress.emit(progress)
            
            # Markeri yaz
            output_file.write(marker)
            
            # Arşiv dosyasını yaz
            for i in range(0, len(archive_data), chunk_size):
                chunk = archive_data[i:i + chunk_size]
                output_file.write(chunk)
                processed_size += len(chunk)
                progress = (processed_size * 100) // total_size
                self.progress.emit(progress)

    def extract_rar_from_file(self):
        total_size = os.path.getsize(self.file_path)
        processed_size = 0
        chunk_size = 1024 * 1024  # 1MB chunks
        
        with open(self.file_path, 'rb') as file:
            data = file.read()
        
        # Her iki marker'ı da kontrol et
        rar_marker = b'RARSTART'
        zip_marker = b'ZIPSTART'
        
        rar_start = data.find(rar_marker)
        zip_start = data.find(zip_marker)
        
        if rar_start != -1:
            marker = rar_marker
            archive_start = rar_start
            archive_type = '.rar'
        elif zip_start != -1:
            marker = zip_marker
            archive_start = zip_start
            archive_type = '.zip'
        else:
            raise Exception("Bu dosyada gizlenmiş arşiv dosyası bulunamadı!")
        
        archive_data = data[archive_start + len(marker):]
        
        # Çıktı dosyasının uzantısını kontrol et ve gerekirse düzelt
        output_base, output_ext = os.path.splitext(self.output_path)
        if output_ext.lower() != archive_type:
            self.output_path = output_base + archive_type
        
        with open(self.output_path, 'wb') as archive_file:
            for i in range(0, len(archive_data), chunk_size):
                chunk = archive_data[i:i + chunk_size]
                archive_file.write(chunk)
                processed_size += len(chunk)
                progress = (processed_size * 100) // total_size
                self.progress.emit(progress)

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
        gizleme_baslik = QLabel("Arşiv Dosyasını Gizle (RAR/ZIP)")
        gizleme_baslik.setStyleSheet("font-weight: bold;")
        layout.addWidget(gizleme_baslik)
        
        self.ana_dosya_label = QLabel("Seçilen Dosya: Henüz seçilmedi")
        self.rar_label = QLabel("Seçilen Arşiv: Henüz seçilmedi")
        
        ana_dosya_sec_btn = QPushButton("Dosya Seç")
        rar_sec_btn = QPushButton("Arşiv Dosyası Seç")
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
        cikarma_baslik = QLabel("Gizlenmiş Arşiv Dosyasını Çıkar")
        cikarma_baslik.setStyleSheet("font-weight: bold;")
        layout.addWidget(cikarma_baslik)
        
        self.gizli_dosya_label = QLabel("Seçilen Dosya: Henüz seçilmedi")
        gizli_dosya_sec_btn = QPushButton("Dosya Seç")
        cikar_btn = QPushButton("Gizlenmiş Dosyayı Çıkar")
        
        layout.addWidget(self.gizli_dosya_label)
        layout.addWidget(gizli_dosya_sec_btn)
        layout.addWidget(cikar_btn)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        layout.addWidget(self.progress_bar)
        
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
        dosya, _ = QFileDialog.getOpenFileName(self, "Arşiv Dosyası Seç", "", 
                                             "Arşiv Dosyaları (*.rar *.zip)")
        if dosya:
            self.rar_path = dosya
            self.rar_label.setText(f"Seçilen Arşiv: {dosya}")

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
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.thread = FileProcessThread("hide", self.ana_dosya_path, self.rar_path, output_path)
            self.thread.progress.connect(self.update_progress)
            self.thread.finished.connect(self.process_finished)
            self.thread.start()

    def cikar(self):
        if not self.gizli_dosya_path:
            QMessageBox.warning(self, "Hata", "Lütfen dosya seçin!")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "RAR'ı Kaydet", "", "RAR Dosyaları (*.rar)")
        if output_path:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.thread = FileProcessThread("extract", self.gizli_dosya_path, None, output_path)
            self.thread.progress.connect(self.update_progress)
            self.thread.finished.connect(self.process_finished)
            self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def process_finished(self, success, message):
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "Başarılı", message)
        else:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = SteganografiUygulamasi()
    pencere.show()
    sys.exit(app.exec_())
#uygar atilla argun