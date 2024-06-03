import streamlit as st
import sqlite3
import random
import pickle
import numpy as np
import os

# Fungsi untuk membuat database dan tabel pengguna
def create_usertable():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, email TEXT, password TEXT)')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan pengguna baru ke database
def add_user(username, email, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, email, password) VALUES (?,?,?)', (username, email, password))
    conn.commit()
    conn.close()

# Fungsi untuk memverifikasi login pengguna
def login_user(email, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE email =? AND password = ?', (email, password))
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk memeriksa apakah email sudah terdaftar
def check_email_exists(email):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE email =?', (email,))
    data = c.fetchall()
    conn.close()
    return data

def main():
    st.markdown("""
        <style>
            .stApp {
                background-color: #A7E6FF;
            }
            .main-title {
                font-size: 3em;
                color: #4CAF50;
                text-align: center;
                margin-bottom: 20px;
            }
            .sidebar-title {
                font-size: 1.5em;
                color: #FF5733;
                margin-bottom: 10px;
            }
            .tab-content {
                padding: 20px;
                background-color: #F0F0F0;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .chat-bot {
                font-size: 1.2em;
                color: #333;
            }
            .input-box {
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    st.header("Jantungers", anchor=None)

    if st.session_state.logged_in:
        tabs = ["Informasi Gagal Jantung", "Chat Bot", "Prediksi Penyakit Jantung", "Pola Hidup Sehat", "Logout"]
        tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)

        with tab1:
            show_gagal_jantung_info()
        with tab2:
            show_chat_bot()
        with tab3:
            show_heart_disease_prediction()
        with tab4:
            show_healthy_lifestyle()
        with tab5:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.success("You have been logged out.")
                st.experimental_rerun()  # Rerun the app to reflect the logged-out state
    else:
        show_login()

def show_gagal_jantung_info():
    st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
    st.title("Informasi Penyakit Gagal Jantung")

    image_path = 'gagal jantung.webp'
    if os.path.exists(image_path):
        st.image(image_path, caption='Penyakit Gagal Jantung', use_column_width=True)
    else:
        st.error(f"Image file not found at path: {image_path}")

    st.header("Apa itu Gagal Jantung?")
    st.write("""
    Gagal jantung adalah kondisi di mana jantung tidak dapat memompa darah sebagaimana mestinya. Hal ini dapat terjadi karena berbagai alasan, termasuk penyakit jantung koroner, tekanan darah tinggi, dan kondisi lainnya yang melemahkan jantung.
    """)

    st.header("Gejala Gagal Jantung")
    st.write("""
    Gejala gagal jantung bisa bervariasi tergantung pada seberapa parah kondisinya, termasuk:
    - Sesak napas saat beraktivitas atau saat berbaring
    - Kelelahan dan kelemahan
    - Pembengkakan pada kaki, pergelangan kaki, dan kaki
    - Detak jantung cepat atau tidak teratur
    - Batuk atau mengi yang terus-menerus
    - Peningkatan kebutuhan untuk buang air kecil di malam hari
    """)

    st.header("Penyebab Gagal Jantung")
    st.write("""
    Penyebab umum gagal jantung meliputi:
    - Penyakit jantung koroner
    - Serangan jantung
    - Tekanan darah tinggi
    - Penyakit katup jantung
    - Kerusakan otot jantung (kardiomiopati)
    - Miokarditis
    - Cacat jantung bawaan
    - Gangguan irama jantung
    """)

    st.header("Pencegahan Gagal Jantung")
    st.write("""
    Beberapa langkah yang dapat membantu mencegah gagal jantung termasuk:
    - Mengelola kondisi medis yang mendasarinya, seperti hipertensi, diabetes, dan penyakit jantung koroner
    - Mengonsumsi makanan sehat dengan diet rendah garam dan lemak jenuh
    - Berolahraga secara teratur
    - Menghindari merokok dan mengurangi konsumsi alkohol
    - Memantau dan mengelola tingkat stres
    """)

    st.write("Untuk informasi lebih lanjut, kunjungi situs web resmi [Kementerian Kesehatan Republik Indonesia](https://www.kemkes.go.id/).")

    st.write("**Sumber**: Informasi ini disusun berdasarkan data dari berbagai sumber medis dan kesehatan.")
    st.markdown("</div>", unsafe_allow_html=True)

def show_chat_bot():
    st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
    st.title("Chatbot")

    # Definisikan dictionary untuk respons
    responses = {
        "halo": [
            "Halo! Ada yang bisa saya bantu?",
            "Hai! Bagaimana kabarmu hari ini?",
            "Selamat datang! Ada pertanyaan?"
        ],
        "saran untuk pencegahan gagal jantung": [
            "Untuk pencegahan gagal jantung, sebaiknya Anda menjaga pola makan sehat, rutin berolahraga, dan menghindari merokok.",
            "Pastikan Anda memantau tekanan darah dan kadar kolesterol secara teratur, serta berkonsultasi dengan dokter Anda secara rutin.",
            "Menghindari konsumsi alkohol berlebihan dan mengelola stres juga penting dalam pencegahan gagal jantung."
        ],
        "bantu saya": [
            "Tolong berikan rekomendasi vitamin yang bagus.",
            "Berikan saya rekomendasi vitamin."
        ],
        "saran untuk rekomendasi vitamin": [
            "Vitamin C baik untuk sistem kekebalan tubuh.",
            "Vitamin D penting untuk kesehatan tulang.",
            "Vitamin B kompleks membantu fungsi otak dan energi."
        ],
        "saran untuk rekomendasi obat": [
            "Konsultasikan dengan dokter untuk obat yang tepat sesuai dengan kondisi Anda.",
            "Pastikan untuk mengikuti dosis yang dianjurkan oleh dokter.",
            "Selalu baca informasi pada kemasan obat dan tanyakan apoteker jika ada yang tidak jelas."
        ],
        "terima kasih": [
            "Sama-sama!",
            "Senang bisa membantu!",
            "Terima kasih kembali!"
        ],
        "selamat tinggal": [
            "Sampai jumpa!",
            "Selamat tinggal! Semoga hari Anda menyenangkan!",
            "Sampai bertemu lagi!"
        ]
    }

    # Simpan riwayat percakapan
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Input dari pengguna
    user_input = st.text_input("Masukkan pesan Anda:")

    # Tampilkan respons berdasarkan input pengguna
    if user_input:
        user_input = user_input.lower()
        st.session_state.history.append(f"Anda: {user_input}")

        if user_input in responses:
            response = random.choice(responses[user_input])
        else:
            response = "Maaf, saya tidak mengerti pertanyaan Anda."

        st.session_state.history.append(f"Bot: {response}")

    # Tampilkan riwayat percakapan
    if st.session_state.history:
        for line in st.session_state.history:
            st.write(line)
    st.markdown("</div>", unsafe_allow_html=True)

def show_heart_disease_prediction():
    st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
    # Load saved model and scaler
    model = pickle.load(open('penyakit_jantung.sav', 'rb'))
    scaler = pickle.load(open('scaler.sav', 'rb'))

    # Streamlit app
    st.title("Prediksi Resiko Penyakit Jantung")

    # Judul web
    usia = st.sidebar.slider("Usia", 20, 100, 50)

    # Input fitur jenis kelamin
    jenis_kelamin = st.sidebar.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

    # Input fitur anemia
    anemia = st.sidebar.selectbox("Anemia", ["Tidak", "Ya"])

    # Input fitur creatinine_phosphokinase
    creatinine_phosphokinase = st.sidebar.number_input("Creatinine Phosphokinase")

    # Input fitur diabetes
    diabetes = st.sidebar.selectbox("Diabetes", ["Tidak", "Ya"])

    # Input fitur pecahan_injeksi
    pecahan_injeksi = st.sidebar.number_input("Pecahan Injeksi")

    # Input fitur tekanan_darah_tinggi
    tekanan_darah_tinggi = st.sidebar.selectbox("Tekanan Darah Tinggi", ["Tidak", "Ya"])

    # Input fitur trombosit
    trombosit = st.sidebar.number_input("Trombosit")

    # Input fitur kebiasaan_merokok
    kebiasaan_merokok = st.sidebar.selectbox("Kebiasaan Merokok", ["Tidak", "Ya"])

    # Input fitur waktu
    waktu = st.sidebar.number_input("Waktu")

    # Input fitur serum_kreatinin
    serum_kreatinin = st.sidebar.number_input("Serum Kreatinin")

    # Input fitur serum_sodium
    serum_sodium = st.sidebar.number_input("Serum Sodium")

    if st.sidebar.button("Prediksi"):
        # Konversi input categorical menjadi numerik
        jenis_kelamin = 1 if jenis_kelamin == "Laki-laki" else 0
        anemia = 1 if anemia == "Ya" else 0
        diabetes = 1 if diabetes == "Ya" else 0
        tekanan_darah_tinggi = 1 if tekanan_darah_tinggi == "Ya" else 0
        kebiasaan_merokok = 1 if kebiasaan_merokok == "Ya" else 0

        # Konversi input menjadi array numpy
        data = np.array([[usia, jenis_kelamin, anemia, creatinine_phosphokinase, diabetes, pecahan_injeksi, tekanan_darah_tinggi, trombosit, kebiasaan_merokok, waktu, serum_kreatinin, serum_sodium]])

        # Normalisasi input data
        data_normalized = scaler.transform(data)

        # Prediksi resiko penyakit jantung
        prediction = model.predict(data_normalized)

        # Tampilkan hasil prediksi
        if prediction[0] == 0:
            st.write("Resiko Penyakit Jantung: Rendah")
        else:
            st.write("Resiko Penyakit Jantung: Tinggi")
    st.markdown("</div>", unsafe_allow_html=True)

def show_healthy_lifestyle():
    st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
    st.title("Pola Hidup Sehat")

    st.header("Pentingnya Pola Hidup Sehat")
    st.write("""
    Menjaga pola hidup sehat sangat penting untuk mencegah berbagai penyakit, termasuk penyakit jantung. Berikut adalah beberapa tips untuk menjalani pola hidup sehat:
    - Konsumsi makanan bergizi seimbang
    - Rutin berolahraga
    - Hindari kebiasaan merokok dan konsumsi alkohol berlebihan
    - Kelola stres dengan baik
    - Jaga berat badan ideal
    """)

    st.header("Makanan Sehat untuk Jantung")
    st.write("""
    Makanan yang baik untuk kesehatan jantung meliputi:
    - Buah-buahan dan sayuran
    - Ikan berlemak (seperti salmon, makarel)
    - Kacang-kacangan dan biji-bijian
    - Minyak zaitun
    - Gandum utuh
    - Produk susu rendah lemak
    """)

    st.header("Aktivitas Fisik yang Dianjurkan")
    st.write("""
    Olahraga yang dianjurkan untuk kesehatan jantung meliputi:
    - Jalan cepat
    - Bersepeda
    - Berenang
    - Yoga
    - Latihan kekuatan (seperti angkat beban)
    """)
    st.markdown("</div>", unsafe_allow_html=True)

def show_login():
    st.title("Login")
    st.write("Selamat datang di web biasa aja kami")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            create_usertable()
            user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.experimental_rerun()  # Rerun the app to reflect the logged-in state
            else:
                st.error("Incorrect email or password")
        else:
            st.error("Please enter email and password")

    st.write("Belum punya akun? [Daftar](#)")

    if st.button("Daftar"):
        username = st.text_input("Username", key="reg_username")
        email_reg = st.text_input("Email", key="reg_email")
        password_reg = st.text_input("Password", type="password", key="reg_password")

        if username and email_reg and password_reg:
            create_usertable()
            if check_email_exists(email_reg):
                st.error("Email already registered. Please login.")
            else:
                add_user(username, email_reg, password_reg)
                st.success("Registration successful! Please login.")
                st.experimental_rerun()  # Rerun the app to show the login screen
        else:
            st.error("Please fill out all fields")

if __name__ == '__main__':
    main()
