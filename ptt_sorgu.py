import requests
import json
from datetime import datetime
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
    
    print("=" * 50)
    print("PTT KARGO BİLGİLERİ")
    print("=" * 50)
    
    print(f"almaHaberFlag: {kargo.get('almaHaberFlag')}")
    print(f"almaHaberFlagSpecified: {kargo.get('almaHaberFlagSpecified')}")
    print(f"errorMessage: {kargo.get('errorMessage')}")
    print(f"errorState: {kargo.get('errorState')}")
    print(f"errorStateSpecified: {kargo.get('errorStateSpecified')}")
    print(f"hareketDongu: {kargo.get('hareketDongu')}")
    
    kabul = kargo.get('kabul', {})
    print("\nKABUL BİLGİLERİ:")
    print(f"agirlik: {kabul.get('agirlik')}")
    print(f"alici: {kabul.get('alici')}")
    print(f"alici_adres: {kabul.get('alici_adres')}")
    print(f"barkod_no: {kabul.get('barkod_no')}")
    print(f"damga_vergisi: {kabul.get('damga_vergisi')}")
    print(f"deger_konulmus_bedeli: {kabul.get('deger_konulmus_bedeli')}")
    print(f"desi: {kabul.get('desi')}")
    print(f"ekhizmetler: {kabul.get('ekhizmetler')}")
    print(f"gonderici: {kabul.get('gonderici')}")
    print(f"gonderici_adres: {kabul.get('gonderici_adres')}")
    print(f"gumruge_sunma_ucreti: {kabul.get('gumruge_sunma_ucreti')}")
    print(f"gumruk_vergisi: {kabul.get('gumruk_vergisi')}")
    print(f"kabul_isyeri: {kabul.get('kabul_isyeri')}")
    print(f"kabul_tarihi: {kabul.get('kabul_tarihi')}")
    print(f"kabul_tarihiSpecified: {kabul.get('kabul_tarihiSpecified')}")
    print(f"odeme_sarti_bedeli: {kabul.get('odeme_sarti_bedeli')}")
    print(f"odeme_tipi: {kabul.get('odeme_tipi')}")
    print(f"reserve1: {kabul.get('reserve1')}")
    print(f"reserve2: {kabul.get('reserve2')}")
    print(f"reserve3: {kabul.get('reserve3')}")
    print(f"reserve4: {kabul.get('reserve4')}")
    print(f"reserve5: {kabul.get('reserve5')}")
    print(f"toplam_yd_ucret: {kabul.get('toplam_yd_ucret')}")
    print(f"ucret: {kabul.get('ucret')}")
    print(f"yd_iade_ucreti: {kabul.get('yd_iade_ucreti')}")
    
    sondurum = kargo.get('sondurum', {})
    print("\nSON DURUM BİLGİLERİ:")
    print(f"ahk_durum_aciklama: {sondurum.get('ahk_durum_aciklama')}")
    print(f"ahk_teslim_alan: {sondurum.get('ahk_teslim_alan')}")
    print(f"ahk_teslim_tarihi: {sondurum.get('ahk_teslim_tarihi')}")
    print(f"mazb_dosya_no: {sondurum.get('mazb_dosya_no')}")
    print(f"mazb_durum_aciklama: {sondurum.get('mazb_durum_aciklama')}")
    print(f"mazb_islem_tarihi: {sondurum.get('mazb_islem_tarihi')}")
    print(f"son_durum_aciklama: {sondurum.get('son_durum_aciklama')}")
    print(f"son_islem_saati: {sondurum.get('son_islem_saati')}")
    print(f"son_islem_tarihi: {sondurum.get('son_islem_tarihi')}")
    print(f"sozl_durum_aciklama: {sondurum.get('sozl_durum_aciklama')}")
    print(f"sozl_teslim_alan: {sondurum.get('sozl_teslim_alan')}")
    print(f"sozl_teslim_tarihi: {sondurum.get('sozl_teslim_tarihi')}")
    print(f"teslim_alan: {sondurum.get('teslim_alan')}")
    print(f"teslim_durum_aciklama: {sondurum.get('teslim_durum_aciklama')}")
    print(f"teslim_tarihi: {sondurum.get('teslim_tarihi')}")
def main():
    print("PTT Kargo Takip Sistemi")
    print("=" * 30)
    
    while True:
        barkod_no = input("Barkod numarasını girin (çıkmak için 'q'): ").strip()
        
        if barkod_no.lower() == 'q':
            print("Program sonlandırıldı.")
            break
        
        if not barkod_no:
            print("Barkod numarası boş olamaz!")
            continue
        
        print(f"Sorgulanıyor: {barkod_no}")
        
        kargo_verisi = ptt_kargo_sorgula(barkod_no)
        
        if kargo_verisi:
            kargo_bilgilerini_yazdir(kargo_verisi)
        else:
            print("Kargo bilgileri alınamadı!")
        
        print("\n" + "=" * 50)
if __name__ == "__main__":
    main()
