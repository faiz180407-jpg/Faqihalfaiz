from IPython.display import display, Image
from IPython.display import HTML, display
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand
display(HTML("""
<style>

.marquee-container {
    width: 100%;
    overflow: hidden;
    background-color: #000000;
    color: #7FFF00;
    border-radius: 10px;
    padding: 12px 0;
    box-sizing: border-box;
    font-family: "Times New Roman", serif;
    font-size: 30px;
    font-weight: bold;
    line-height: 1.2;
    /* Efek cahaya */} """
))


# 1. Pilih style

plt.style.use('dark_background')

#plt.style.use('default')
# 2. Buat data dan grafik seperti biasa

import numpy as np # Asumsi numpy sudah di-import sebelumnya, namun wajib ada untuk np.linspace
x = np.linspace(0, 10, 100)
y = np.cos(x)

plt.plot(x, y)
plt.title("Grafik dengan Style")
plt.show()


#1. data
x = [1,2,3,4,5]
y = [3,5,-77,19,12]

# 2. buat grafik
plt.plot(x,y)

# Judul
plt.title("GRAFIK SIMPLE")
plt.xlabel ('nilaiX')
plt.ylabel('NilaiY')

#3. Menampilkan Chart
plt.show()

# available styles
plt.style.available # Menampilkan daftar semua style yang tersedia : SHFT+ENTER

plt.style.use('dark_background')


# numpy.random

x, y = rand(2, 100)

plt.scatter(x,y)
plt.show()


# Data
bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei']
Penjualan = [150, 200, 180, 250, 125]

# 8x4 inci adalah ukuran yang kecil dan tidak full screen
plt.figure(figsize=(8, 5))

plt.bar(bulan, Penjualan, color='blue') #barh
plt.title('Penjualan per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah')

# Menambahkan nilai angka di ujung setiap batang (opsional tapi sangat disarankan)
for i, nilai in enumerate(Penjualan):
    plt.text(nilai +2 , i, str(nilai), va='center', fontsize=14, color='blue', fontweight='bold')

# color='red'

plt.show()


# Data
bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli']
penjualan = [150, 200, 180, 250, 125, 220, 130]

plt.figure(figsize=(6, 4)) #inchi

# Membuat grafik dengan palette warna yang lebih modern
sns.barplot(x=bulan, y=penjualan)

plt.title('Penjualan per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Penjualan')

plt.show()



# Data
bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli']
penjualan = [150, 200, 180, 250, 125, 220, 130]

plt.figure(figsize=(8, 4)) # Diperlebar sedikit agar 7 bulan muat dengan rapi

# 1. Buat Grafik Batang
sns.barplot(x=bulan, y=penjualan)

# 2. Tambahkan Garis Tren (Menghubungkan puncak batang)
# range(len(bulan)) menghasilkan [0, 1, 2, 3, 4, 5, 6] sebagai posisi sumbu X
plt.plot(
    range(len(bulan)), # Posisi X (tengah setiap batang)
    penjualan,         # Posisi Y (nilai penjualan)
    color='red',       # Warna garis
    marker='o',        # Tambahkan titik bulat di setiap persimpangan
    linestyle='-',     # Gaya garis (solid)
    linewidth=2,       # Ketebalan garis
    label='Garis Tren' # Nama untuk legenda
)

# 3. Kustomisasi Tampilan
plt.title('Penjualan per Bulan dengan Garis Tren', fontsize=12, fontweight='bold')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penjualan')
plt.legend() # Menampilkan kotak legenda

plt.tight_layout()
plt.show()

