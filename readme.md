# 🌐 RemotePulse

**RemotePulse**, bilgisayarınızı yerel ağ (LAN) üzerinden herhangi bir cihazla yönetmenizi sağlayan, Flask tabanlı bir uzaktan kontrol arayüzüdür. Tek bir dokunuşla bilgisayarınızı kilitleyebilir, kapatabilir veya medya içeriklerinizi yönetebilirsiniz.

---

## 🚀 Özellikler

*   **Çapraz Platform Desteği:** Windows ve macOS sistemlerinde sorunsuz çalışır.
*   **Akıllı Port Yönetimi:** Eğer varsayılan port doluysa, otomatik olarak bir sonraki boş portu bulur.
*   **Medya Kontrolü:** Oynat/Duraklat ve Sessiz/Sesi Aç özellikleri.
*   **Sistem Yönetimi:** Uzaktan Kilitleme, Yeniden Başlatma ve Kapatma.
*   **Dinamik IP Tespiti:** Sunucu başladığında yerel ağdaki adresini otomatik olarak gösterir.

---

## ⚖️ Lisans ve Katkı Kuralları

Bu proje **MIT** tabanlı özel bir lisansla korunmaktadır. Kod üzerinde değişiklik yapma ve bu değişiklikleri yayınlama hakkı geliştiricilerin onayına tabidir. 

**Değişiklik yapmak isterseniz:**
Lütfen önce bir **Issue** açarak bize bildirin. Onay sürecinin ardından yeni versiyonların yayınlanmasına izin verilecektir.

---

## 🛠️ Kurulum

Projeyi çalıştırmak için öncelikle gerekli kütüphaneleri yüklemeniz gerekmektedir. Terminalinizi veya CMD ekranınızı açıp şu komutu çalıştırın:
```bash
pip install -r requirements.txt
python3 remote-pulse.py
