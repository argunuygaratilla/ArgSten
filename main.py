# RAR dosyasını JPEG içine gizlemek için kullanılan Python kodu
#python main.py hide orjinal.jpeg gizlenecek.rar sonuc.jpeg

# JPEG dosyasından RAR dosyasını çıkarmak için kullanılan Python kodu
#python main.py extract sonuc.jpeg sonuc.rar




def hide_rar_in_jpeg(jpeg_path, rar_path, output_path):
    # JPEG ve RAR dosyalarını binary modda aç
    with open(jpeg_path, 'rb') as jpeg_file:
        jpeg_data = jpeg_file.read()
    
    with open(rar_path, 'rb') as rar_file:
        rar_data = rar_file.read()
    
    # JPEG dosyasının sonuna özel bir işaret ve RAR verisini ekle
    marker = b'RARSTART'  # RAR verisinin başladığını belirten işaret
    combined_data = jpeg_data + marker + rar_data
    
    # Yeni dosyayı oluştur
    with open(output_path, 'wb') as output_file:
        output_file.write(combined_data)

def extract_rar_from_jpeg(jpeg_path, output_rar_path):
    # Gizlenmiş RAR'ı içeren JPEG dosyasını aç
    with open(jpeg_path, 'rb') as file:
        data = file.read()
    
    # RAR verisinin başlangıcını bul
    marker = b'RARSTART'
    rar_start = data.find(marker)
    
    if rar_start == -1:
        raise Exception("Bu JPEG dosyasında gizlenmiş RAR bulunamadı!")
    
    # RAR verisini çıkart
    rar_data = data[rar_start + len(marker):]
    
    # RAR dosyasını kaydet
    with open(output_rar_path, 'wb') as rar_file:
        rar_file.write(rar_data)

# Kullanım örneği
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Kullanım:")
        print("Gizlemek için: python main.py hide input.jpeg input.rar output.jpeg")
        print("Çıkarmak için: python main.py extract input.jpeg output.rar")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "hide":
        if len(sys.argv) != 5:
            print("Hatalı parametre sayısı!")
            sys.exit(1)
        hide_rar_in_jpeg(sys.argv[2], sys.argv[3], sys.argv[4])
        print("RAR dosyası başarıyla JPEG içine gizlendi!")
    
    elif command == "extract":
        if len(sys.argv) != 4:
            print("Hatalı parametre sayısı!")
            sys.exit(1)
        extract_rar_from_jpeg(sys.argv[2], sys.argv[3])
        print("RAR dosyası başarıyla çıkarıldı!")
    
    else:
        print("Geçersiz komut! 'hide' veya 'extract' kullanın.")
