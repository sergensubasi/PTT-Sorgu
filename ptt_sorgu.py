import requests
import json
from datetime import datetime
# PTT Durum Kodları Tablosu
PTT_DURUM_KODLARI = {
    831: "Tasfiye Edildi", 1: "Kabul Edildi", 701: "Kayıt Edildi", 159: "Güncelleme Yapıldı", 16: "Yurtdışı Kabul Geliş Kaydı Yapıldı", 
    77: "Sevk Edildi", 8: "Zimmet Alındı", 9: "Zimmet Edildi", 3: "Torbaya Eklendi", 6: "Torbadan Alìndì", 4: "Torbadan Çıkarıldı", 
    78: "PTB'den Çıkarıldı", 303: "Gönderi Gümrükte Tutuluyor", 5: "Torbası İptal Edildi", 91: "Torbası Sevk Edildi", 302: "Gümrüğe Sevk Edildi", 
    999: "Zimmet İptal Edildi", 320: "Yurtdışına Sevk Edildi", 14: "Kayıt Defterinden Silindi", 149: "Ptt Tarafından Zimmet Alındı", 
    11: "Gönderinin Geliş Kaydı Yapıldı", 13: "Merkez Kayıt Defterine Eklendi", 92: "Torbasının Geliş Kaydı Yapıldı", 148: "Firma Tarafından Zimmet Alındı", 
    7: "Dağıtıcıya Verildi", 12: "Cihetten Gönderi Çıkarıldı", 156: "İADE-Diğer", 99: "İade Edilecek", 151: "İADE-Tanınmıyor", 
    163: "İADE-Aranılmadı", 161: "İADE-Adreste Yok", 164: "İADE-İthali Yasak", 830: "İADE-Geri İstendi", 133: "İADE-Kayıp Gönderi", 
    154: "İADE-Kabul Edilmedi", 155: "İADE-Adres Yetersiz", 152: "İADE-Adresden Ayrılmış", 160: "İADE-Binaya Girilemedi", 
    162: "İADE-Alıcı Vefat Etmiş", 134: "İADE-Alıcısı Vefat Etmiş", 135: "İADE-Geri İstendi (Banka)", 136: "İADE-İade İstendi (Banka)", 
    153: "İADE-Bekleme Süresi Bitti", 166: "İADE:Kimlik İbraz Edilmedi", 158: "İADE-Adres Hatalı/Okunmuyor", 167: "İADE:Tutanaklı/Talimatlı İşlem", 
    137: "İADE-Dağıtım Sahası Dışı Sevk (Banka)", 168: "İADE:Muhatap Adresi Değişmiş/Yeni Adres Bulunumadı", 198: "İADE:Vergi Tebligatı 2. Dağıtımda Tebliğ Edilemedi", 
    169: "İADE:Adresteki Bina Yıkılmış veya Bina Özelliğini Tamamen Yitirmiştir", 165: "İade İptal Edildi", 100: "Teslim Edildi", 
    252: "MAZBATA TESLİM", 157: "Evrak Memuruna Teslim", 807: "MUHATABA BiZZAT TESLiM", 818: "iSYERiNDE AMiRiNE TESLiM", 
    812: "AYNI KONUTTA YAKINA TESLiM", 202: "Kargomatikten Teslim Alındı", 813: "21.MAD. GORE MUHTARA TESLiM", 221: "İkinci Adreste Kendisine Teslim", 
    222: "Üçüncü Adreste Kendisine Teslim", 223: "Farklı Adreste Kendisine Teslim", 824: "iSYERiNDE DAiMi CALISANA TESLiM", 
    220: "Birinci Adreste Kendisine Teslim", 225: "İkinci Adreste Aile Bireyine Teslim", 226: "Üçüncü Adreste Aile Bireyine Teslim", 
    227: "Farklı Adreste Aile Bireyine Teslim", 224: "Birinci Adreste Aile Bireyine Teslim", 815: "21.MAD. GORE ZABITA AMiRi/MEMURA TESLiM", 
    232: "Teslim Edildi(Tutanaklı/Talimatlı İşlem)", 814: "21.MAD. GORE iHTiYAR HEYETi/AZAYA TESLiM", 229: "İkinci Adreste İş Yeri Yetkilisine Teslim", 
    230: "Üçüncü Adreste İş Yeri Yetkilisine Teslim", 231: "Farklı Adreste İş Yeri Yetkilisine Teslim", 228: "Birinci Adreste İş Yeri Yetkilisine Teslim", 
    826: "BAĞIMSIZ BÖLÜMDE OTURAN YOK, PANOYA ASILDI", 829: "21/2. Maddeye Göre Muhtara Teslim (MERNİS)", 827: "21.MADDE VE EK.1 E GÖRE TEBLİĞ, PANOYA ASILDI", 
    825: "BAĞIMSIZ BÖLÜMDE OTURANA TEBLİĞ, PANOYA ASILDI", 816: "35.MAD. GORE MUHATAP ADRESi KAPISINA YAPISTIRMA", 
    828: "Muhatap imtinaEttigindenSahitleÖnüneBirakilmistir", 120: "Göndericisine Teslim Edildi", 141: "İadeten Banka Şubesine Teslim", 
    106: "Banka Şubesine Teslim", 121: "Alma Haber Kartı Teslimi", 138: "Sözleşme Teslim (Banka)", 15: "Teslim İptal Edildi", 
    109: "İmha", 118: "Diğer", 127: "Askerde", 147: "El Koyma", 105: "Geri İstendi", 150: "İade İstendi", 140: "Kabul Edilmedi", 
    101: "Teslim Edilemedi", 145: "Imha-Vefat Etmiş", 125: "İsim/Soyad Hatalı", 146: "Binaya Girilemedi", 380: "Diğer Adrese Sevk", 
    107: "Üçüncü Adrese Sevk", 113: "İkinci Adrese Sevk", 124: "Adreste Yok/Kapalı", 126: "Adreste Tanınmıyor", 112: "PTT İşyerine Teslim", 
    131: "Sorunlu Alıcı/Diğer", 144: "Imha-Kabul Edilmedi", 381: "Alıcısı Vefat Etmiş", 111: "Haber Kağıdı Bırakıldı", 
    143: "Imha-Banka Geri İstedi", 117: "Yargıtay Teslimli Kargo", 388: "İliçi Diğer Adrese Sevk", 389: "İldışı Diğer Adrese Sevk", 
    142: "Imha-Bekleme Süresi Bitti", 110: "PTT İşyerine Teslim Edildi", 139: "Adresten Ayrılmış/Taşınmış", 501: "İmha İptal Edildi", 
    399: "Teslim Edilen Gönderi Ücreti Yatırıldı.", 132: "Adres Hatalı/Adres Yetersiz", 114: "Mutemetin Gelmesi Bekleniyor", 
    115: "Köy Dağıtımına Tabi Bekliyor", 116: "2.Kez Haber Kağıdı Bırakıldı", 716: "Gönderi Akıbeti Araştırılıyor", 
    194: "Hava Şartları/Terör/Doğal Afet", 712: "E-posta Gönderilemedi Bekliyor", 108: "Geçici Olarak Adresten Ayrılmış", 
    128: "Sorunlu Alıcı-Kimlik Göstermedi", 713: "Alıcı Talimatı ile Bekletiliyor", 129: "Sorunlu Alıcı-TC No İsim Tutmuyor", 
    711: "SMS ile Mesaj Gönderildi Bekliyor", 709: "PTT İşyeri Teslim Cihetine Eklendi", 714: "Gönderici Talimatı ile Bekletiliyor", 
    717: "Gönderi Akıbeti Belirlenemedi/Kayıp", 718: "Mazbata Akıbeti Belirlenemedi/Kayıp", 211: "Telefon ile Haber Verilmedi Bekliyor", 
    710: "SMS ile Mesaj Gönderilemedi Bekliyor", 130: "Sorunlu Alıcı/Sözleşmeyi İmzalamıyor/Şerh", 715: "Teslim Edilemedi(Tutanaklı/Talimatlı İşlem)", 
    719: "Vergi Tebligatı 1. Dağıtımda Tebliğ Edilemedi", 196: "Dağıtım Binaya Girilemedi-Haber Kağıdı Bırakıldı", 
    195: "Dağıtım Adreste Yok/Kapalı-Haber Kağıdı Bırakıldı", 199: "PTT ye Teslim Binaya Girilemedi-Haber Kağıdı Bırakıldı", 
    197: "PTT ye Teslim Adreste Yok/Kapalı-Haber Kağıdı Bırakıldı", 2: "İptal Edildi", 176: "EL KOYMA", 177: "SÖZLEŞME", 
    174: "2. ADRESE SEVK", 175: "3. ADRESE SEVK", 172: "SERVİS GÖNDERİSİ", 178: "ALMA HABER KARTI", 170: "PTT ADRESLİ GÖNDERİ", 
    171: "KÖY DAĞITIMINA TABİ GÖNDERİ", 173: "DAĞITIM SAHASI DIŞI GÖNDERİ", 600: "Tanınmıyor", 601: "Tanınmıyor", 532: "Yerinde Yok", 
    568: "Yerinde Yok", 531: "Adres Hatalı", 557: "Yanlış Cihet", 567: "Adres Hatalı", 569: "Yanlış Cihet", 530: "Adres Okunmuyor", 
    566: "Adres Okunmuyor", 527: "İade : Alıcısı Ölmüş", 560: "İade : Alıcısı Ölmüş", 528: "İade : Adres Yetersiz", 
    545: "İade : Adres Yetersiz", 565: "Haber Kağıdı Bırakıldı", 583: "PTT İşyerinde İhbarlandı", 547: "İade : Alıcısı Kabul Etmiyor", 
    556: "İade : Alıcısı Kabul Etmiyor", 529: "İade : Adresten Ayrılmış(Yeni Adresi Yok)", 546: "İade : Adresten Ayrılmış(Yeni Adresi Yok)", 
    585: "Teslim Edilemedi : PTT İşyerinde İhbarlandı", 578: "Teslim Edilemedi : Adresten Ayrılmış(Yeni Adrese Sevk)", 
    652: "Talimat Bekleniyor", 650: "PTT İşyerinde Bekliyor", 653: "PTT İşyerinde Bekliyor", 657: "PTT İşyerinde Bekliyor", 
    699: "Depodan Gönderi Çıkartıldı", 651: "Köy Dağıtımına Tabi Bekliyor", 656: "(MEVKUF) Elde Kalmış Gönderi", 
    654: "(İADE) PTT İşyerinde Bekliyor", 655: "(BANKA İADE) PTT İşyerinde Bekliyor", 21: "Sistemden Çıkartıldı", 307: "TEST", 
    180: "Kayıp", 181: "Hasar", 240: "Satıldı", 185: "El Koyma", 301: "Onaylandı", 955: "Sözleşme Kayıp", 183: "Tazminat Ödendi", 
    300: "Siparis Verildi", 304: "Gümrükten Çıktı", 10: "Problemli Gönderi", 192: "Kayıp (Tasfiye)", 305: "Onay İptal Edildi", 
    103: "Elde Kalmış Gönderi", 954: "Sözleşme Tamamlandı", 182: "Araştırma Başlatıldı", 184: "Süresinde Aranılmadı", 
    306: "E-Telgraf Gönderildi", 201: "İhb-Kargomatiğe Bırakıldı", 450: "Talimat İptal Edildi", 210: "Telefonla Haber Verildi", 
    700: "Talimat İçin Bekleniyor", 950: "Sözleşme Kontrol Edildi", 952: "Sözleşme İmza Sürecinde", 186: "Tutanaklı/Talimatlı İşlem", 
    191: "PTT (Tasfiye) Geri Aldı", 953: "Sözleşme Tamamlatılamıyor", 102: "PTT Terk/Hesabıma Satılsın", 241: "Elde Kalmış Gönderi İmhası", 
    471: "Posta Çeki Güncellendi", 119: "Banka İsteğiyle Geri Çekildi", 188: "Kayıp Tebligat Suret İstendi", 403: "Talimat Verildi(Geri Alma)", 
    470: "Ödeme Bedeli Güncellendi", 951: "Sözleşme Kontrol İptal Edildi", 190: "Gönderici Talebi İle Geri Alındı", 
    410: "Talimat Verildi(II.Adrese Git)", 413: "Talimat Verildi(3. Adrese Git)", 44: "Cihet Hazırlama Listesine Eklendi", 
    472: "Ödeme Şart Türü Güncellendi", 411: "Talimat Verildi(İade Adresine Git)", 720: "Kargomatta Bekleme Süresi Bitti", 
    262: "Kimlik Bilgisi Alınamadı", 45: "Cihet Hazırlama Listesinden Çıkarıldı", 423: "Talimat Etiketi Üretildi(Geri Alma)", 
    187: "Hatalı Tebliğ Nedeni İle Suret İstendi", 203: "İade Edilmek Üzere Kargomatikten Alındı", 412: "Talimat Verildi(Banka Şubesine Teslim)", 
    308: "Mazbata Datası Çıkaran Merciye Gönderildi", 400: "Talimat Verildi(Alıcı Adını Değiştirme)", 430: "Talimat Etiketi Üretildi(II.Adrese Git)", 
    433: "Talimat Yerine Getirildi(3. Adrese Git)", 405: "Talimat Verildi(Teslim Gününü Belirleme)", 104: "Alıcının Talebi ile PTT İşyerine Teslim", 
    401: "Talimat Verildi(Alıcı Adresini Değiştirme)", 189: "Kayıp Mazbata Teslim Belgesi Suret Gönderildi", 431: "Talimat Etiketi Üretildi(İade Adresine Git)", 
    402: "Talimat Verildi(Bekleme Suresini Değiştirme)", 440: "Talimat Verildi(Alma Haber Ek Hizmeti Ekleme)", 
    417: "Talimat Verildi(Gönderici Adresini Değiştirme)", 432: "Talimat Etiketi Üretildi(Banka Şubesine Teslim)", 
    441: "Talimat Verildi(Alma Haber Ek Hizmeti Kaldırma)", 416: "Talimat Verildi(Kontrollü Teslim Hizmeti Ekleme)", 
    420: "Talimat Etiketi Üretildi(Alıcı Adını Değiştirme)", 409: "Talimat Verildi(Gönderiyi 3 kez Dağıtıma Çıkarma)", 
    425: "Talimat Etiketi Üretildi(Teslim Gününü Belirleme)", 404: "Talimat Verildi(Gonderiyi Tekrar Dağıtıma Çıkarma)", 
    406: "Talimat Verildi(Teslim Edilememe Bilgisi Gönderme)", 414: "Talimat Verildi(Barkod Bilgisi Güncelle (Ödemeli))", 
    418: "Talimat Verildi(Ücreti Alıcıdan Ek Hizmeti Ekleme)", 407: "Talimat Verildi(Teslim Edilemez ise İdareye Kalsın)", 
    421: "Talimat Etiketi Üretildi(Alıcı Adresini Değiştirme)", 415: "Talimat Verildi(Ücreti Alıcıdan Ek Hizmeti Kaldırma)", 
    422: "Talimat Etiketi Üretildi(Bekleme Suresini Değiştirme)", 408: "Talimat Verildi(Teslim Edilemez ise Hesabıma Satılsın)", 
    460: "Talimat Etiketi Üretildi(Alma Haber Ek Hizmeti Ekleme)", 437: "Talimat Etiketi Üretildi(Gönderici Adresini Değiştirme)", 
    461: "Talimat Etiketi Üretildi(Alma Haber Ek Hizmeti Kaldırma)", 436: "Talimat Yerine Getirildi(Kontrollü Teslim Hizmeti Ekleme)", 
    429: "Talimat Etiketi Üretildi(Gönderiyi 3 kez Dağıtıma Çıkarma)", 424: "Talimat Etiketi Üretildi(Gonderiyi Tekrar Dağıtıma Çıkarma)", 
    426: "Talimat Etiketi Üretildi(Teslim Edilememe Bilgisi Gönderme)", 434: "Talimat Yerine Getirildi(Barkod Bilgisi Güncelle (Ödemeli))", 
    438: "Talimat Etiketi Üretildi(Ücreti Alıcıdan Ek Hizmeti Ekleme)", 427: "Talimat Etiketi Üretildi(Teslim Edilemez ise İdareye Kalsın)", 
    435: "Talimat Yerine Getirildi(Ücreti Alıcıdan Ek Hizmeti Kaldırma)", 428: "Talimat Etiketi Üretildi(Teslim Edilemez ise Hesabıma Satılsın)", 
    310: "Gönderinin İthaline Gümrükçe İzin Verilmedi", 849: "İADE-Elçilik Adresi-Tebligat Yapılamadı", 442: "Talimat Verildi(Alıcı Alıcı Telefonu Değiştirme (Kargomat))", 
    462: "Talimat Yerine Getirildi(Alıcı Telefonu Değiştirme (Kargomat))", 854: "Vergi Tebligatı-Muhatap Adına Almaya Yetkili Kişiler İmtina Etti,İade", 
    204: "Islem Iptali Sebebiyle Kargomatikten Alindi", 473: "Pal Ebay Ücret Ödemesi Yapıldı", 855: "İADE:Cezaevi Adresi-Tebligat Yapılamadı", 
    856: "İADE:Kargomatta Bekleme Süresi Bitti", 474: "Gümrük Ücret Kaydı Yapıldı", 260: "Sözleşme Gereği İhbarlanmayan Gönderi", 
    261: "Kimlik Bilgisi Alınamadı", 290: "Kargomat İşlem İptal (Sistem Hatası/Zaman Aşımı)", 291: "Kargomattan Alınmak Üzere İptal Onayı Verildi", 
    832: "İADE:Sevk Edildi", 443: "Talimat Verildi(Elektronik Alma Haber Ek Hizmeti Ekleme)", 444: "Talimat Verildi(Alıcı Telefonu Değiştirme/Ekleme)", 
    463: "Talimat Etiketi Üretildi(Elektronik Alma Haber Ek Hizmeti Ekleme)", 464: "Talimat Etiketi Üretildi(Alıcı Telefonu Değiştirme/Ekleme)", 
    997: "Gönderi Arşivlenebilir", 998: "Gönderi Arşivlenemez", 309: "Suret Baskısı Alındı"
}

def ptt_kargo_sorgula(barkod_no):
    url = "https://api.ptt.gov.tr/api/ShipmentTracking"
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    payload = [barkod_no]
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"API bağlantı hatası: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse hatası: {e}")
        return None
def kargo_bilgilerini_yazdir(data):
    if not data or len(data) == 0:
        print("Kargo bilgisi bulunamadı!")
        return
    
    kargo = data[0]
    
    # KABUL VE SON DURUM BİLGİLERİ YAZDIRILMIYOR (Kullanıcı İsteği)
    
    # ÖZEL DURUM ANALİZİ
    hareketler = kargo.get('hareketDongu', [])
    # Başlıkları da kaldırıyoruz sade çıktı için
    
    found_any_delivery = False # Hiç teslim/iade kelimesi geçti mi?
    found_special = False      # Özel kodlu teslim/iade var mı?
    
    for hareket in hareketler:
        aciklama = hareket.get('aciklama', '')
        durum = hareket.get('durum')
        tarih = hareket.get('tarih')
        
        # Filtre: Açıklama TESLİM EDİLDİ veya İADE ise
        if aciklama in ["TESLİM EDİLDİ", "İADE"]:
            found_any_delivery = True
            
            # VE durum standart (252, 120) değilse detay yaz
            if durum not in [252, 120]:
                ozel_aciklama = PTT_DURUM_KODLARI.get(durum, f"Bilinmeyen Kod ({durum})")
                
                # Prefix belirle
                durum_baslik = "Tebliğ Edildi" if aciklama == "TESLİM EDİLDİ" else "İade Edildi"
                
                print(f"Durum: {durum_baslik} -- {ozel_aciklama} -- {tarih}")
                found_special = True
    
    # Eğer hiç TESLİM veya İADE yoksa, son durumu yazdır
    if not found_any_delivery and hareketler:
        son_hareket = hareketler[-1]
        son_durum_kodu = son_hareket.get('durum')
        son_tarih = son_hareket.get('tarih')
        son_aciklama = son_hareket.get('aciklama', '')
        son_aciklama_detay = PTT_DURUM_KODLARI.get(son_durum_kodu, f"Bilinmeyen Kod ({son_durum_kodu})")
        
        # Fallback için de benzer format
        durum_baslik = "Tebliğ Edildi" if son_aciklama == "TESLİM EDİLDİ" else ("İade Edildi" if son_aciklama == "İADE" else "Son Durum")
        
        print(f"Durum: {durum_baslik} -- {son_aciklama_detay} -- {son_tarih}")
                
    if not found_special and found_any_delivery:
        print("Standart teslim/iade işlemi.")
    elif not found_special and not found_any_delivery and not hareketler:
        print("Herhangi bir hareket bulunamadı.")


def main():
    import argparse
    import sys
    
    # Windows konsolunda Türkçe karakter sorunu için
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    
    # Argüman okuyucu (GitHub için)
    parser = argparse.ArgumentParser()
    parser.add_argument('barkod', nargs='?', help='Barkod No')
    args = parser.parse_args()
    
    # --- GITHUB MODU (Otomatik) ---
    if args.barkod:
        # print(f"Otomatik Sorgu: {args.barkod}")  <-- Bu satırı kapattım, sadece sonuç yazsın.
        kargo_verisi = ptt_kargo_sorgula(args.barkod)
        if kargo_verisi:
            kargo_bilgilerini_yazdir(kargo_verisi)
        else:
            # Hata durumunda boş çıktı veya özel hata kodu basabiliriz, şimdilik sessiz.
            pass
        return
    else:
        # Argüman yoksa hata
        print("HATA: Barkod numarası argüman olarak verilmeli!")
        sys.exit(1)

if __name__ == "__main__":
    main()
