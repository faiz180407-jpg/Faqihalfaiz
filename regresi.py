import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import plotly.graph_objects as go
import plotly.io as pio
url = "https://raw.githubusercontent.com/Alam-A99/DATAAKSI/refs/heads/main/dataset_fiskal_97_hipoFull.csv"

# Membaca dataset
df = pd.read_csv(url, sep=None, engine='python')

# Memfilter semua baris yang mengandung teks "Kediri" (tidak peka huruf besar/kecil)
kediri_data = df[df.apply(lambda row: row.astype(str).str.contains('Kediri', case=False).any(), axis=1)]

# Menampilkan hasil
print("Kota Kediri:")
display(kediri_data)




# Memaksa Plotly untuk merender grafik interaktif langsung di dalam sel Google Colab
pio.renderers.default = 'colab'

# -----------------------------------------------------------------------------------------
# 1. MEMBACA DATA ASLI DARI GITHUB (KOTA KEDIRI)

url = 'https://raw.githubusercontent.com/Alam-A99/DATAAKSI/main/dataset_fiskal_97_hipoFull.csv'
df_all = pd.read_csv(url)

# Menentukan kolom wilayah dan menyaring khusus Kota Kediri
kolom_kota = 'Kota' if 'Kota' in df_all.columns else [c for c in df_all.columns if 'kota' in c.lower() or 'kab' in c.lower()][0]
df = df_all[df_all[kolom_kota].astype(str).str.contains('Kediri', case=False, na=False)].copy()

print(f"Total data Kota Kediri yang dianalisis: {len(df)} baris.\n")

# -----------------------------------------------------------------------------------------
# 2. MODEL REGRESI & UJI ASUMSI KLASIK

X = df[['bm_pendidikan', 'bm_perlindungan_sosial']]
Y = df['KEMISKINAN']
X_sm = sm.add_constant(X)
model = sm.OLS(Y, X_sm).fit()

# Menampilkan Summary OLS
print(model.summary())

print("\n" + "="*50)
print("FUNGSI REGRESI (Data Asli):")
print(f"Y = {model.params['const']:.4f} + {model.params['bm_pendidikan']:.4f}(BM_Pendidikan) - {abs(model.params['bm_perlindungan_sosial']):.4f}(BM_Sosial)")
print("="*50)

print("\nHASIL UJI ASUMSI KLASIK")
# 1. Normalitas
shapiro_stat, shapiro_p = stats.shapiro(model.resid)
print(f"- Normalitas (Shapiro-Wilk) P-Value: {shapiro_p:.4f} (>0.05 = Lolos)")

# 2. Multikolinearitas (VIF)
vif_data = pd.DataFrame()
vif_data["Variabel"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(f"- Multikolinearitas (VIF)            : {vif_data['VIF'].max():.4f} (<10 = Lolos)")

# 3. Heteroskedastisitas
bp_test = sms.het_breuschpagan(model.resid, model.model.exog)
print(f"- Heteroskedastisitas (BP) P-Value   : {bp_test[1]:.4f} (>0.05 = Lolos)")

# 4. Autokorelasi
dw_value = sm.stats.stattools.durbin_watson(model.resid)
print(f"- Autokorelasi (Durbin-Watson)       : {dw_value:.4f} (Mendekati 2 = Lolos)\n")

# --------------------------------------------------------------------------------
# 3. VISUALISASI 3D INTERAKTIF

# Membuat grid bidang regresi berdasarkan rentang data asli
x_range = np.linspace(df['bm_pendidikan'].min(), df['bm_pendidikan'].max(), 20)
y_range = np.linspace(df['bm_perlindungan_sosial'].min(), df['bm_perlindungan_sosial'].max(), 20)
x_grid, y_grid = np.meshgrid(x_range, y_range)

# Menghitung prediksi Z untuk permukaan bidang
z_grid = model.params['const'] + (model.params['bm_pendidikan'] * x_grid) + (model.params['bm_perlindungan_sosial'] * y_grid)

# Inisialisasi Plotly Figure
fig = go.Figure()

# Menambahkan Bidang Regresi Permukaan
fig.add_trace(go.Surface(
    x=x_grid,
    y=y_grid,
    z=z_grid,
    name='Bidang Regresi',
    colorscale='viridis',
    opacity=0.8,
    showscale=False
))

# Menambahkan Titik Data Aktual Asli
fig.add_trace(go.Scatter3d(
    x=df['bm_pendidikan'],
    y=df['bm_perlindungan_sosial'],
    z=df['KEMISKINAN'],
    mode='markers',
    name='Data Aktual',
    marker=dict(size=6, color='red', line=dict(color='white', width=1))
))

# Mengatur Tampilan Layout Grafik
fig.update_layout(
    title=f"Plot Bidang Regresi 3D: Kemiskinan terhadap BM Pendidikan & BM Sosial (Kota Kediri) | R² = {model.rsquared:.2f}",
    template='plotly_dark',
    scene=dict(
        xaxis_title='BM Pendidikan',
        yaxis_title='BM Perlindungan Sosial',
        zaxis_title='Kemiskinan'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Menampilkan kanvas interaktif di bawah sel Colab
fig.show()