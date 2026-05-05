"""Luffy Was Here"""
import os, flask, sys, socket, colorama
from pynput.keyboard import Key, Controller
from typing import Optional

keyboard = Controller()

class Server:
    """Ana Sunucu Sınıfı"""
    def __init__(self, host: Optional[str] = '0.0.0.0', port: Optional[int] = 5000):
        """
        Sunucu sınıfını başlatır; işletim sistemini algılar, ağ ayarlarını yapar, 
        yönetici yetkilerini kontrol eder ve Flask rotalarını tanımlar.
        """
        self.platform = self._get_platform()
        self.host = host 
        self.port = self._adjust_port(start_port=port)
        self.ip = self._get_ip()
        self.server = flask.Flask('remote-pulse')
        self.is_super_user = True if self.platform == 'windows' else os.geteuid() == 0
        if not self.is_super_user: 
            print(colorama.Fore.RED + "Uyarı: Restart komutu için yönetici hakları gerekiyor. sudo ile çalıştırmayı deneyin." + colorama.Style.RESET_ALL)
        self._setup_routes()

    def _get_platform(self):
        """
        Kodun çalıştığı işletim sistemini tespit ederek 'mac', 'windows' 
        veya 'other' değerlerinden birini döndürür.
        """
        if sys.platform.lower() == 'darwin': return 'mac'
        elif sys.platform.lower() == 'win32': return 'windows'
        else: return 'other'

    def _setup_routes(self):
        """
        Web tarayıcısı üzerinden gelecek istekleri (kapatma, kilitleme, medya kontrolü vb.) 
        ilgili Python fonksiyonlarına bağlayan URL rotalarını tanımlar.
        """
        self.server.add_url_rule('/', 'index', self.index)
        self.server.add_url_rule('/action/shutdown', 'shutdown', self.shutdown, methods=["post"])
        self.server.add_url_rule('/action/lock', 'lock', self.lock, methods=["post"])
        self.server.add_url_rule('/action/restart', 'restart', self.restart, methods=["post"])
        self.server.add_url_rule('/action/play-pouse', 'play-pouse', self.play_pouse, methods=["post"])
        self.server.add_url_rule('/action/mute-unmute', 'mute-unmute', self.mute_unmute, methods=["post"])

    def _get_ip(self):
        """
        Cihazın yerel ağdaki (LAN) aktif IP adresini tespit eder. 
        İnternete çıkış yapılamazsa varsayılan olarak '127.0.0.1' döndürür.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            """Google dnsine paket gönderip ipyi alır"""
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def _adjust_port(self, start_port: int) -> int:
        """
        Belirlenen portun kullanımda olup olmadığını kontrol eder. 
        Eğer port doluysa, boş bir port bulana kadar port numarasını 
        100'er artırarak denemeye devam eder.
        """
        port = start_port
        host = self.host
        while True:
            # Geçici bir soket oluşturup portu dinlemeye çalışıyoruz
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind((host, port))
                    # Eğer hata vermezse port boştur
                    return port
                except OSError:
                    # Port doluysa 100 artır ve döngüye devam et
                    print(f"[*] Port {port} kullanımda, {port + 100} portu deneniyor...")
                    port += 100
    
    """ Routelar """
    def index(self):
        """Ana kontrol sayfasını (arayüzü) yükler."""
        return flask.render_template('index.html')
    
    def lock(self):
        """İşletim sistemine göre ekran kilitleme komutunu çalıştırır."""
        if self.platform == 'mac': os.system('pmset displaysleepnow')
        elif self.platform == 'windows': os.system('rundll32.exe user32.dll,LockWorkStation')
        else: os.system('xlock') # Linux ve diğer sistemler için
        return flask.render_template('action.html', action_message="Ekran Kilitlendi!")
    
    def shutdown(self):
        """Bilgisayarı tamamen kapatma komutunu tetikler."""
        if self.platform == 'mac': os.system('shutdown -h now')
        elif self.platform == 'windows': os.system('shutdown /s /t 0')
        else: os.system('shutdown -h now') # Linux ve diğer sistemler için
        return flask.render_template('action.html', action_message="Bilgisayar Kapatılıyor!")

    def restart(self):
        """Yönetici izni varsa bilgisayarı yeniden başlatır."""
        if self.is_super_user:
            if self.platform == 'mac': os.system('shutdown -r now')
            elif self.platform == 'windows': os.system('shutdown /r /t 0')
            else: os.system('shutdown -r now') # Linux ve diğer sistemler için
            return flask.render_template('action.html', action_message="Bilgisayar Yeniden Başlatılıyor!")
        else:
            return flask.render_template('error.html', error_message="Yeniden başlatma işlemi için yönetici hakları gerekiyor.")

    def play_pouse(self):
        """Klavye simülasyonu yaparak medyayı oynatır veya duraklatır."""
        keyboard.press(Key.media_play_pause); keyboard.release(Key.media_play_pause)
        return flask.render_template('action.html', action_message="İstek Başarılı!")

    def mute_unmute(self):
        """Sesi tamamen kapatır veya açar."""
        if self.platform == 'mac': os.system('osascript -e "set volume output muted not (output muted of (get volume settings))"')
        elif self.platform == 'windows': keyboard.press(Key.media_volume_mute); keyboard.release(Key.media_volume_mute)
        return flask.render_template('action.html', action_message="İstek Başarılı!")    

    def run(self):
        """Sunucuyu belirtilen IP ve port üzerinden yayına alır."""
        print(colorama.Fore.CYAN + 'Sunucu şu adreste yayında: http://{}:{}'.format(self.ip, self.port) + colorama.Style.RESET_ALL)
        self.server.run(host=self.host, port=self.port)
    
if __name__ == '__main__': 
    Sunucu = Server()
    Sunucu.run()
"""Luffy Was Here"""