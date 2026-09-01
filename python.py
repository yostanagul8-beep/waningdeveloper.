        import tkinter as tk
import random
import math
import winsound
import threading
import time

# --- KONFIGURASI MUSIK (Jingle Bells) ---
# Format: (Frekuensi dalam Hz, Durasi dalam milidetik)
JINGLE_BELLS = [
    (659, 200), (659, 200), (659, 400), # E E E
    (659, 200), (659, 200), (659, 400), # E E E
    (659, 200), (784, 200), (523, 300), (587, 100), (659, 800), # E G C D E
    (698, 200), (698, 200), (698, 300), (698, 100), # F F F F
    (698, 200), (659, 200), (659, 200), (659, 100), (659, 100), # F E E E E
    (659, 200), (587, 200), (587, 200), (659, 200), (587, 400), (784, 400) # E D D E D G
]

def putar_musik():
    while True:
        for freq, duration in JINGLE_BELLS:
            try:
                if freq <= 37:
                    time.sleep(duration / 1000.0)
                else:
                    winsound.Beep(freq, duration)
                time.sleep(0.05) # Jeda antar nada
            except:
                return # Keluar jika aplikasi ditutup

def bunyikan_ledakan():
    try:
        winsound.Beep(150, 150)
    except:
        pass

# --- KELAS ANIMASI UTAMA ---
class AnimasiNatal:
    def __init__(self, root):
        self.root = root
        self.root.title("Selamat Hari Natal & Tahun Baru!")
        self.lebar = 800
        self.tinggi = 600
        
        # Canvas utama dengan latar belakang malam gelap
        self.canvas = tk.Canvas(root, width=self.lebar, height=self.tinggi, bg="#050510", highlightthickness=0)
        self.canvas.pack()
        
        self.partikel_kembang_api = []
        self.lampu_pohon = []
        
        # Jalankan tahap pertama: Kembang Api
        self.mulai_kembang_api()
        
        # Jalankan musik secara asynchronous agar tidak mengganggu jalannya animasi
        self.thread_musik = threading.Thread(target=putar_musik, daemon=True)
        self.thread_musik.start()

    # --- TAHAP 1: ANIMASI KEMBANG API ---
    def mulai_kembang_api(self):
        for _ in range(3): # Membuat 3 titik ledakan acak
            cx = random.randint(150, self.lebar - 150)
            cy = random.randint(100, self.tinggi - 300)
            warna = random.choice(["#FF3366", "#FFFF33", "#33FF33", "#33CCFF", "#FF9933", "#FF33FF"])
            
            # Bunyi efek ledakan kembang api
            threading.Thread(target=bunyikan_ledakan, daemon=True).start()
            
            # Membuat 36 partikel menyebar melingkar
            for i in range(36):
                sudut = math.radians(i * 10)
                kecepatan = random.uniform(3, 7)
                vx = math.cos(sudut) * kecepatan
                vy = math.sin(sudut) * kecepatan
                
                p = self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=warna, outline="")
                self.partikel_kembang_api.append({'id': p, 'vx': vx, 'vy': vy, 'alpha': 1.0})
                
        self.update_kembang_api(0)

    def update_kembang_api(self, hitungan_frame):
        partikel_aktif = False
        for p in self.partikel_kembang_api:
            if p['alpha'] > 0:
                self.canvas.move(p['id'], p['vx'], p['vy'])
                p['vy'] += 0.05 # Efek gravitasi jatuh kebawah
                p['alpha'] -= 0.015 # Memudar gradual
                
                if p['alpha'] <= 0:
                    self.canvas.delete(p['id'])
                else:
                    partikel_aktif = True
                    
        if partikel_aktif and hitungan_frame < 70:
            self.root.after(30, lambda: self.update_kembang_api(hitungan_frame + 1))
        else:
            # Hapus sisa kembang api, lanjut gambar pohon natal
            for p in self.partikel_kembang_api:
                self.canvas.delete(p['id'])
            self.gambar_pohon_natal()

    # --- TAHAP 2: GAMBAR POHON NATAL & LAMPU KEDIP ---
    def gambar_pohon_natal(self):
        # Menggambar Batang
        self.canvas.create_rectangle(375, 450, 425, 520, fill="#5C4033", outline="")
        
        # Menggambar Daun Pohon (3 Lapisan Segitiga)
        self.canvas.create_polygon(400, 180, 310, 300, 490, 300, fill="#0B6623", outline="") # Atas
        self.canvas.create_polygon(400, 260, 270, 390, 530, 390, fill="#0B6623", outline="") # Tengah
        self.canvas.create_polygon(400, 340, 230, 470, 570, 470, fill="#074E1D", outline="") # Bawah
        
        # Menggambar Bintang Emas di Puncak
        self.gambar_bintang(400, 175, 5, 20, 8, fill="#FFD700")
        
        # Koordinat titik-titik penempatan lampu hias
        koordinat_lampu = [
            (400, 220), (370, 260), (430, 260), (390, 280), (410, 280),
            (400, 300), (350, 340), (450, 340), (320, 370), (480, 370), (380, 360), (420, 360),
            (400, 400), (330, 430), (470, 430), (280, 450), (520, 450), (370, 440), (430, 440), (300, 420), (500, 420)
        ]
        
        for cx, cy in koordinat_lampu:
            id_lampu = self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="#FFFF00", outline="")
            self.lampu_pohon.append(id_lampu)
            
        # Jalankan loop kedipan lampu hias
        self.kedipkan_lampu()
        
        # Siapkan wadah teks, lanjut jalankan efek pengetikan teks ucapan
        self.teks_tujuan = "SELAMAT HARI NATAL & TAHUN BARU!"
        self.id_teks = self.canvas.create_text(400, 560, text="", font=("Courier New", 20, "bold"), fill="#FFFFFF")
        self.efek_ketik_teks(0)

    def gambar_bintang(self, x, y, spikes, r_outer, r_inner, fill):
        points = []
        angle = math.pi / spikes
        for i in range(2 * spikes):
            r = r_outer if i % 2 == 0 else r_inner
            curr_angle = i * angle - math.pi / 2
            points.append(x + math.cos(curr_angle) * r)
            points.append(y + math.sin(curr_angle) * r)
        self.canvas.create_polygon(points, fill=fill, outline="")

    def kedipkan_lampu(self):
        daftar_warna = ["#FF3333", "#33FF33", "#3333FF", "#FFFF33", "#FF33FF", "#33FFFF"]
        for lampu in self.lampu_pohon:
            warna_acak = random.choice(daftar_warna)
            self.canvas.itemconfig(lampu, fill=warna_acak)
        # Berulang setiap 300ms
        self.root.after(300, self.kedipkan_lampu)

    # --- TAHAP 3: TEKS TYPEWRITER (PER HURUF) ---
    def efek_ketik_teks(self, indeks):
        if indeks <= len(self.teks_tujuan):
            teks_sekarang = self.teks_tujuan[:indeks]
            self.canvas.itemconfig(self.id_teks, text=teks_sekarang)
            # Kecepatan ketikan huruf (150ms per huruf)
            self.root.after(150, lambda: self.efek_ketik_teks(indeks + 1))

# --- MEMULAI APLIKASI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimasiNatal(root)
    root.mainloop()

                         