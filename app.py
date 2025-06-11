import streamlit as st
import pandas as pd
import numpy as np
import joblib # Untuk memuat model dan preprocessor yang sudah dilatih
import io # Untuk membaca file dari BytesIO

# --- Mappings untuk fitur kategorikal (diambil dari penjelasan variabel Anda) ---
marital_status_map = {
    1: 'Lajang', 2: 'Menikah', 3: 'Janda/Duda', 4: 'Bercerai', 5: 'Serikat Faktanya', 6: 'Terpisah Secara Hukum'
}

application_mode_map = {
    1: 'Fase 1 - Kontingen Umum', 2: 'Peraturan No. 612/93', 5: 'Fase 1 - Kontingen Khusus (Pulau Azores)',
    7: 'Pemilik Kursus Pendidikan Tinggi Lainnya', 10: 'Peraturan No. 854-B/99', 15: 'Siswa Internasional (Sarjana)',
    16: 'Fase 1 - Kontingen Khusus (Pulau Madeira)', 17: 'Fase 2 - Kontingen Umum', 18: 'Fase 3 - Kontingen Umum',
    26: 'Peraturan No. 533-A/99, item b2) (Rencana Berbeda)', 27: 'Peraturan No. 533-A/99, item b3 (Institusi Lain)',
    39: 'Usia di atas 23 Tahun', 42: 'Transfer', 43: 'Pergantian Jurusan',
    44: 'Pemegang Diploma Spesialisasi Teknologi', 51: 'Pergantian Institusi/Jurusan',
    53: 'Pemegang Diploma Siklus Pendek', 57: 'Pergantian Institusi/Jurusan (Internasional)'
}

course_map = {
    33: 'Biofuel Production Technologies', 171: 'Animation and Multimedia Design', 8014: 'Social Service (evening attendance)',
    9003: 'Agronomy', 9070: 'Communication Design', 9085: 'Veterinary Nursing', 9119: 'Informatics Engineering',
    9130: 'Equinculture', 9147: 'Management', 9238: 'Social Service', 9254: 'Tourism', 9500: 'Nursing',
    9556: 'Oral Hygiene', 9670: 'Advertising and Marketing Management', 9773: 'Journalism and Communication',
    9853: 'Basic Education', 9991: 'Management (evening attendance)'
}

daytime_evening_attendance_map = {
    1: 'Siang', 0: 'Malam'
}

previous_qualification_map = {
    1: 'Pendidikan Menengah', 2: 'Pendidikan Tinggi - Sarjana Muda', 3: 'Pendidikan Tinggi - Gelar',
    4: 'Pendidikan Tinggi - Magister', 5: 'Pendidikan Tinggi - Doktor', 6: 'Frekuensi Pendidikan Tinggi',
    9: 'Tahun ke-12 Sekolah - Tidak Selesai', 10: 'Tahun ke-11 Sekolah - Tidak Selesai',
    12: 'Lainnya - Tahun ke-11 Sekolah', 14: 'Tahun ke-10 Sekolah', 15: 'Tahun ke-10 Sekolah - Tidak Selesai',
    19: 'Pendidikan Dasar Siklus 3 (Tahun ke-9/10/11) atau Setara',
    38: 'Pendidikan Dasar Siklus 2 (Tahun ke-6/7/8) atau Setara', 39: 'Kursus Spesialisasi Teknologi',
    40: 'Pendidikan Tinggi - Gelar (Siklus 1)', 42: 'Kursus Teknik Tinggi Profesional',
    43: 'Pendidikan Tinggi - Magister (Siklus 2)'
}

nacionality_map = {
    1: 'Portugis', 2: 'Jerman', 6: 'Spanyol', 11: 'Italia', 13: 'Belanda', 14: 'Inggris',
    17: 'Lituania', 21: 'Angola', 22: 'Cape Verdean', 24: 'Guinean', 25: 'Mozambik',
    26: 'Santomean', 32: 'Turki', 41: 'Brazil', 62: 'Rumania', 100: 'Moldova (Republik)',
    101: 'Meksiko', 103: 'Ukraina', 105: 'Rusia', 108: 'Kuba', 109: 'Kolombia'
}

mothers_qualification_map = {
    1: 'Pendidikan Menengah - Tahun ke-12 Sekolah atau Setara', 2: 'Pendidikan Tinggi - Sarjana Muda',
    3: 'Pendidikan Tinggi - Gelar', 4: 'Pendidikan Tinggi - Magister', 5: 'Pendidikan Tinggi - Doktor',
    6: 'Frekuensi Pendidikan Tinggi', 9: 'Tahun ke-12 Sekolah - Tidak Selesai',
    10: 'Tahun ke-11 Sekolah - Tidak Selesai', 11: 'Tahun ke-7 (Lama)', 12: 'Lainnya - Tahun ke-11 Sekolah',
    14: 'Tahun ke-10 Sekolah', 18: 'Kursus Perdagangan Umum',
    19: 'Pendidikan Dasar Siklus 3 (Tahun ke-9/10/11) atau Setara', 22: 'Kursus Teknik-Profesional',
    26: 'Tahun ke-7 Sekolah', 27: 'Siklus 2 Kursus SMA Umum', 29: 'Tahun ke-9 Sekolah - Tidak Selesai',
    30: 'Tahun ke-8 Sekolah', 34: 'Tidak Diketahui', 35: 'Tidak Bisa Membaca atau Menulis',
    36: 'Bisa Membaca Tanpa Lulus Tahun ke-4 Sekolah',
    37: 'Pendidikan Dasar Siklus 1 (Tahun ke-4/5) atau Setara',
    38: 'Pendidikan Dasar Siklus 2 (Tahun ke-6/7/8) atau Setara', 39: 'Kursus Spesialisasi Teknologi',
    40: 'Pendidikan Tinggi - Gelar (Siklus 1)', 41: 'Kursus Studi Tinggi Spesialis',
    42: 'Kursus Teknik Tinggi Profesional', 43: 'Pendidikan Tinggi - Magister (Siklus 2)',
    44: 'Pendidikan Tinggi - Doktor (Siklus 3)'
}

fathers_qualification_map = {
    1: 'Pendidikan Menengah - Tahun ke-12 Sekolah atau Setara', 2: 'Pendidikan Tinggi - Sarjana Muda',
    3: 'Pendidikan Tinggi - Gelar', 4: 'Pendidikan Tinggi - Magister', 5: 'Pendidikan Tinggi - Doktor',
    6: 'Frekuensi Pendidikan Tinggi', 9: 'Tahun ke-12 Sekolah - Tidak Selesai',
    10: 'Tahun ke-11 Sekolah - Tidak Selesai', 11: 'Tahun ke-7 (Lama)', 12: 'Lainnya - Tahun ke-11 Sekolah',
    13: 'Kursus SMA Pelengkap Tahun ke-2', 14: 'Tahun ke-10 Sekolah', 18: 'Kursus Perdagangan Umum',
    19: 'Pendidikan Dasar Siklus 3 (Tahun ke-9/10/11) atau Setara', 20: 'Kursus SMA Pelengkap',
    22: 'Kursus Teknik-Profesional', 25: 'Kursus SMA Pelengkap - Tidak Selesai', 26: 'Tahun ke-7 Sekolah',
    27: 'Siklus 2 Kursus SMA Umum', 29: 'Tahun ke-9 Sekolah - Tidak Selesai',
    30: 'Tahun ke-8 Sekolah', 31: 'Kursus Umum Administrasi dan Perdagangan', 33: 'Akuntansi dan Administrasi Tambahan',
    34: 'Tidak Diketahui', 35: 'Tidak Bisa Membaca atau Menulis',
    36: 'Bisa Membaca Tanpa Lulus Tahun ke-4 Sekolah',
    37: 'Pendidikan Dasar Siklus 1 (Tahun ke-4/5) atau Setara',
    38: 'Pendidikan Dasar Siklus 2 (Tahun ke-6/7/8) atau Setara', 39: 'Kursus Spesialisasi Teknologi',
    40: 'Pendidikan Tinggi - Gelar (Siklus 1)', 41: 'Kursus Studi Tinggi Spesialis',
    42: 'Kursus Teknik Tinggi Profesional', 43: 'Pendidikan Tinggi - Magister (Siklus 2)',
    44: 'Pendidikan Tinggi - Doktor (Siklus 3)'
}

mothers_occupation_map = {
    0: 'Pelajar', 1: 'Perwakilan Kekuasaan Legislatif dan Badan Eksekutif, Direktur, Direktur dan Manajer Eksekutif',
    2: 'Spesialis dalam Aktivitas Intelektual dan Ilmiah', 3: 'Teknisi dan Profesi Tingkat Menengah',
    4: 'Staf Administrasi', 5: 'Pekerja Layanan Pribadi, Keamanan dan Keselamatan, dan Penjual',
    6: 'Petani dan Pekerja Terampil di Pertanian, Perikanan, dan Kehutanan',
    7: 'Pekerja Terampil di Industri, Konstruksi, dan Pengrajin',
    8: 'Operator Instalasi dan Mesin dan Pekerja Perakitan', 9: 'Pekerja Tidak Terampil',
    10: 'Profesi Angkatan Bersenjata', 90: 'Situasi Lain', 99: '(Kosong)',
    122: 'Profesional Kesehatan', 123: 'Guru', 125: 'Spesialis Teknologi Informasi dan Komunikasi (TIK)',
    131: 'Teknisi dan Profesi Tingkat Menengah Ilmu Pengetahuan dan Teknik',
    132: 'Teknisi dan Profesional Tingkat Menengah Kesehatan',
    134: 'Teknisi Tingkat Menengah dari Layanan Hukum, Sosial, Olahraga, Budaya, dan Sejenisnya',
    141: 'Pekerja Kantor, Sekretaris Umum, dan Operator Pemrosesan Data',
    143: 'Operator Data, Akuntansi, Statistik, Keuangan, dan Layanan Terkait Registri',
    144: 'Staf Pendukung Administrasi Lainnya', 151: 'Pekerja Layanan Pribadi', 152: 'Penjual',
    153: 'Pekerja Perawatan Pribadi dan Sejenisnya',
    171: 'Pekerja Konstruksi Terampil dan Sejenisnya, Kecuali Elektrik',
    173: 'Pekerja Terampil di Percetakan, Manufaktur Instrumen Presisi, Perhiasan, Pengrajin, dan Sejenisnya',
    175: 'Pekerja di Pemrosesan Makanan, Pengerjaan Kayu, Pakaian, dan Industri dan Kerajinan Lainnya',
    191: 'Pekerja Kebersihan', 192: 'Pekerja Tidak Terampil di Pertanian, Produksi Hewan, Perikanan, dan Kehutanan',
    193: 'Pekerja Tidak Terampil di Industri Ekstraktif, Konstruksi, Manufaktur, dan Transportasi',
    194: 'Asisten Persiapan Makanan'
}

fathers_occupation_map = {
    0: 'Pelajar', 1: 'Perwakilan Kekuasaan Legislatif dan Badan Eksekutif, Direktur, Direktur dan Manajer Eksekutif',
    2: 'Spesialis dalam Aktivitas Intelektual dan Ilmiah', 3: 'Teknisi dan Profesi Tingkat Menengah',
    4: 'Staf Administrasi', 5: 'Pekerja Layanan Pribadi, Keamanan dan Keselamatan, dan Penjual',
    6: 'Petani dan Pekerja Terampil di Pertanian, Perikanan, dan Kehutanan',
    7: 'Pekerja Terampil di Industri, Konstruksi, dan Pengrajin',
    8: 'Operator Instalasi dan Mesin dan Pekerja Perakitan', 9: 'Pekerja Tidak Terampil',
    10: 'Profesi Angkatan Bersenjata', 90: 'Situasi Lain', 99: '(Kosong)',
    101: 'Perwira Angkatan Bersenjata', 102: 'Sersan Angkatan Bersenjata', 103: 'Personel Angkatan Bersenjata Lainnya',
    112: 'Direktur Layanan Administrasi dan Komersial', 114: 'Direktur Hotel, Katering, Perdagangan, dan Layanan Lainnya',
    121: 'Spesialis dalam Ilmu Fisika, Matematika, Teknik, dan Teknik Terkait', 122: 'Profesional Kesehatan',
    123: 'Guru', 124: 'Spesialis Keuangan, Akuntansi, Organisasi Administrasi, Hubungan Masyarakat dan Komersial',
    131: 'Teknisi dan Profesi Tingkat Menengah Ilmu Pengetahuan dan Teknik',
    132: 'Teknisi dan Profesional Tingkat Menengah Kesehatan',
    134: 'Teknisi Tingkat Menengah dari Layanan Hukum, Sosial, Olahraga, Budaya, dan Sejenisnya',
    135: 'Teknisi Teknologi Informasi dan Komunikasi', 141: 'Pekerja Kantor, Sekretaris Umum, dan Operator Pemrosesan Data',
    143: 'Operator Data, Akuntansi, Statistik, Keuangan, dan Layanan Terkait Registri',
    144: 'Staf Pendukung Administrasi Lainnya', 151: 'Pekerja Layanan Pribadi', 152: 'Penjual',
    153: 'Pekerja Perawatan Pribadi dan Sejenisnya', 154: 'Personel Layanan Perlindungan dan Keamanan',
    161: 'Petani Berorientasi Pasar dan Pekerja Terampil Pertanian dan Produksi Hewan',
    163: 'Petani, Peternak, Nelayan, Pemburu, dan Pengumpul, Subsisten',
    171: 'Pekerja Konstruksi Terampil dan Sejenisnya, Kecuali Elektrik',
    172: 'Pekerja Terampil di Metalurgi, Pengerjaan Logam, dan Sejenisnya',
    174: 'Pekerja Terampil di Listrik dan Elektronika',
    175: 'Pekerja di Pemrosesan Makanan, Pengerjaan Kayu, Pakaian, dan Industri dan Kerajinan Lainnya',
    181: 'Operator Pabrik Tetap dan Mesin', 182: 'Pekerja Perakitan',
    183: 'Pengemudi Kendaraan dan Operator Peralatan Bergerak',
    192: 'Pekerja Tidak Terampil di Pertanian, Produksi Hewan, Perikanan, dan Kehutanan',
    193: 'Pekerja Tidak Terampil di Industri Ekstraktif, Konstruksi, Manufaktur, dan Transportasi',
    194: 'Asisten Persiapan Makanan', 195: 'Penjual Jalanan (Kecuali Makanan) dan Penyedia Layanan Jalanan'
}
# --- Akhir Mappings ---

# Daftar kolom yang diharapkan (sesuai urutan dalam data training)
EXPECTED_COLUMNS = [
    'Marital_status', 'Application_mode', 'Application_order', 'Course',
    'Daytime_evening_attendance', 'Previous_qualification', 'Previous_qualification_grade',
    'Nacionality', 'Mothers_qualification', 'Fathers_qualification', 'Mothers_occupation',
    'Fathers_occupation', 'Admission_grade', 'Displaced', 'Educational_special_needs',
    'Debtor', 'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'Age_at_enrollment',
    'International', 'Curricular_units_1st_sem_credited', 'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations', 'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade', 'Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_credited', 'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_evaluations', 'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade', 'Curricular_units_2nd_sem_without_evaluations',
    'Unemployment_rate', 'Inflation_rate', 'GDP'
]

# Fungsi untuk memuat model dan preprocessor
@st.cache_resource # Menggunakan cache agar model tidak dimuat ulang setiap interaksi
def load_model_and_preprocessor():
    try:
        model = joblib.load('random_forest_model.pkl')
        preprocessor = joblib.load('preprocessor.pkl')
        label_encoder_status = joblib.load('label_encoder_status.pkl')
        return model, preprocessor, label_encoder_status
    except FileNotFoundError:
        st.error("Error: File model, preprocessor, atau label encoder tidak ditemukan.")
        st.info("Pastikan Anda telah melatih model dan menyimpan file-file .pkl dengan nama yang benar di direktori yang sama dengan `app.py`.")
        st.stop()
    except Exception as e:
        st.error(f"Error saat memuat file: {e}")
        st.stop()

# Memuat model, preprocessor, dan label encoder
model, preprocessor, label_encoder_status = load_model_and_preprocessor()

# Judul Aplikasi
st.title("Prediksi Status Mahasiswa Jaya Jaya Institut")

# Deskripsi
st.write("""
Aplikasi ini memprediksi status akhir mahasiswa (Dropout, Enrolled, atau Graduate).
Anda bisa memasukkan data secara manual atau mengunggah file CSV.
""")

# --- Pilihan Input (Manual vs. Upload CSV) ---
prediction_mode = st.radio(
    "Pilih Mode Prediksi:",
    ('Input Manual', 'Upload CSV File'),
    index=0 # Default ke Input Manual
)

input_df = pd.DataFrame() # Inisialisasi DataFrame kosong

if prediction_mode == 'Input Manual':
    st.sidebar.header("Masukkan Data Mahasiswa:")

    def user_input_features():
        # Menggunakan selectbox dengan label deskriptif dan value numerik
        # (kode input manual yang sama dari versi sebelumnya)
        marital_status_label = st.sidebar.selectbox('Status Pernikahan', options=list(marital_status_map.values()))
        marital_status = [k for k, v in marital_status_map.items() if v == marital_status_label][0]

        application_mode_label = st.sidebar.selectbox('Mode Aplikasi', options=list(application_mode_map.values()))
        application_mode = [k for k, v in application_mode_map.items() if v == application_mode_label][0]

        application_order = st.sidebar.slider('Urutan Aplikasi', 0, 9, 1)

        course_label = st.sidebar.selectbox('Program Studi (Course)', options=list(course_map.values()))
        course = [k for k, v in course_map.items() if v == course_label][0]

        daytime_evening_attendance_label = st.sidebar.selectbox('Kehadiran (Siang/Malam)', options=list(daytime_evening_attendance_map.values()))
        daytime_evening_attendance = [k for k, v in daytime_evening_attendance_map.items() if v == daytime_evening_attendance_label][0]

        previous_qualification_label = st.sidebar.selectbox('Kualifikasi Sebelumnya', options=list(previous_qualification_map.values()))
        previous_qualification = [k for k, v in previous_qualification_map.items() if v == previous_qualification_label][0]

        previous_qualification_grade = st.sidebar.slider('Nilai Kualifikasi Sebelumnya', 95.0, 190.0, 130.0)

        nacionality_label = st.sidebar.selectbox('Kewarganegaraan', options=list(nacionality_map.values()))
        nacionality = [k for k, v in nacionality_map.items() if v == nacionality_label][0]

        mothers_qualification_label = st.sidebar.selectbox('Kualifikasi Ibu', options=list(mothers_qualification_map.values()))
        mothers_qualification = [k for k, v in mothers_qualification_map.items() if v == mothers_qualification_label][0]

        fathers_qualification_label = st.sidebar.selectbox('Kualifikasi Ayah', options=list(fathers_qualification_map.values()))
        fathers_qualification = [k for k, v in fathers_qualification_map.items() if v == fathers_qualification_label][0]

        mothers_occupation_label = st.sidebar.selectbox('Pekerjaan Ibu', options=list(mothers_occupation_map.values()))
        mothers_occupation = [k for k, v in mothers_occupation_map.items() if v == mothers_occupation_label][0]

        fathers_occupation_label = st.sidebar.selectbox('Pekerjaan Ayah', options=list(fathers_occupation_map.values()))
        fathers_occupation = [k for k, v in fathers_occupation_map.items() if v == fathers_occupation_label][0]

        admission_grade = st.sidebar.slider('Nilai Penerimaan', 95.0, 190.0, 130.0)

        displaced_label = st.sidebar.selectbox('Pindahan (Displaced)', ('Tidak', 'Ya'))
        displaced = 1 if displaced_label == 'Ya' else 0

        educational_special_needs_label = st.sidebar.selectbox('Kebutuhan Pendidikan Khusus', ('Tidak', 'Ya'))
        educational_special_needs = 1 if educational_special_needs_label == 'Ya' else 0

        debtor_label = st.sidebar.selectbox('Memiliki Hutang (Debtor)', ('Tidak', 'Ya'))
        debtor = 1 if debtor_label == 'Ya' else 0

        tuition_fees_up_to_date_label = st.sidebar.selectbox('SPP Lunas', ('Belum Lunas', 'Lunas'))
        tuition_fees_up_to_date = 1 if tuition_fees_up_to_date_label == 'Lunas' else 0

        gender_label = st.sidebar.selectbox('Jenis Kelamin', ('Perempuan', 'Laki-laki'))
        gender = 1 if gender_label == 'Laki-laki' else 0

        scholarship_holder_label = st.sidebar.selectbox('Penerima Beasiswa', ('Tidak', 'Ya'))
        scholarship_holder = 1 if scholarship_holder_label == 'Ya' else 0

        age_at_enrollment = st.sidebar.slider('Usia Saat Pendaftaran', 17, 70, 20)
        international_label = st.sidebar.selectbox('Mahasiswa Internasional', ('Tidak', 'Ya'))
        international = 1 if international_label == 'Ya' else 0

        curricular_units_1st_sem_credited = st.sidebar.slider('SKS Diakui Sem 1', 0, 20, 0)
        curricular_units_1st_sem_enrolled = st.sidebar.slider('SKS Diambil Sem 1', 0, 26, 6)
        curricular_units_1st_sem_evaluations = st.sidebar.slider('Evaluasi Sem 1', 0, 45, 8)
        curricular_units_1st_sem_approved = st.sidebar.slider('SKS Lulus Sem 1', 0, 26, 5)
        curricular_units_1st_sem_grade = st.sidebar.slider('Nilai Sem 1', 0.0, 18.875, 12.0)
        curricular_units_1st_sem_without_evaluations = st.sidebar.slider('SKS Tanpa Evaluasi Sem 1', 0, 12, 0)
        curricular_units_2nd_sem_credited = st.sidebar.slider('SKS Diakui Sem 2', 0, 19, 0)
        curricular_units_2nd_sem_enrolled = st.sidebar.slider('SKS Diambil Sem 2', 0, 23, 6)
        curricular_units_2nd_sem_evaluations = st.sidebar.slider('Evaluasi Sem 2', 0, 33, 8)
        curricular_units_2nd_sem_approved = st.sidebar.slider('SKS Lulus Sem 2', 0, 20, 5)
        curricular_units_2nd_sem_grade = st.sidebar.slider('Nilai Sem 2', 0.0, 18.571, 12.0)
        curricular_units_2nd_sem_without_evaluations = st.sidebar.slider('SKS Tanpa Evaluasi Sem 2', 0, 12, 0)
        unemployment_rate = st.sidebar.slider('Tingkat Pengangguran', 7.6, 16.2, 11.5)
        inflation_rate = st.sidebar.slider('Tingkat Inflasi', -0.8, 3.7, 1.2)
        gdp = st.sidebar.slider('GDP', -4.06, 3.51, 0.0)

        data = {
            'Marital_status': marital_status,
            'Application_mode': application_mode,
            'Application_order': application_order,
            'Course': course,
            'Daytime_evening_attendance': daytime_evening_attendance,
            'Previous_qualification': previous_qualification,
            'Previous_qualification_grade': previous_qualification_grade,
            'Nacionality': nacionality,
            'Mothers_qualification': mothers_qualification,
            'Fathers_qualification': fathers_qualification,
            'Mothers_occupation': mothers_occupation,
            'Fathers_occupation': fathers_occupation,
            'Admission_grade': admission_grade,
            'Displaced': displaced,
            'Educational_special_needs': educational_special_needs,
            'Debtor': debtor,
            'Tuition_fees_up_to_date': tuition_fees_up_to_date,
            'Gender': gender,
            'Scholarship_holder': scholarship_holder,
            'Age_at_enrollment': age_at_enrollment,
            'International': international,
            'Curricular_units_1st_sem_credited': curricular_units_1st_sem_credited,
            'Curricular_units_1st_sem_enrolled': curricular_units_1st_sem_enrolled,
            'Curricular_units_1st_sem_evaluations': curricular_units_1st_sem_evaluations,
            'Curricular_units_1st_sem_approved': curricular_units_1st_sem_approved,
            'Curricular_units_1st_sem_grade': curricular_units_1st_sem_grade,
            'Curricular_units_1st_sem_without_evaluations': curricular_units_1st_sem_without_evaluations,
            'Curricular_units_2nd_sem_credited': curricular_units_2nd_sem_credited,
            'Curricular_units_2nd_sem_enrolled': curricular_units_2nd_sem_enrolled,
            'Curricular_units_2nd_sem_evaluations': curricular_units_2nd_sem_evaluations,
            'Curricular_units_2nd_sem_approved': curricular_units_2nd_sem_approved,
            'Curricular_units_2nd_sem_grade': curricular_units_2nd_sem_grade,
            'Curricular_units_2nd_sem_without_evaluations': curricular_units_2nd_sem_without_evaluations,            'Unemployment_rate': unemployment_rate,
            'Inflation_rate': inflation_rate,
            'GDP': gdp
        }
        
        features = pd.DataFrame(data, index=[0])
        return features

    input_df = user_input_features()

elif prediction_mode == 'Upload CSV File':
    st.subheader("Unggah File CSV untuk Prediksi Massal")
    st.info("Pastikan file CSV Anda menggunakan **titik koma (`;`)** sebagai pemisah, dan memiliki semua kolom yang diharapkan seperti contoh data yang diberikan, kecuali kolom 'Status'.")
    
    uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            # Menggunakan io.StringIO untuk membaca file yang diunggah
            # Penting: gunakan delimiter ';'
            input_df = pd.read_csv(uploaded_file, sep=';')
            st.write("Data yang Diunggah:")
            st.dataframe(input_df)

            # Validasi kolom
            missing_cols = [col for col in EXPECTED_COLUMNS if col not in input_df.columns]
            if missing_cols:
                st.error(f"Error: File CSV tidak memiliki semua kolom yang diharapkan. Kolom yang hilang: {', '.join(missing_cols)}")
                st.info(f"Pastikan kolom-kolom berikut ada dan sesuai namanya: {', '.join(EXPECTED_COLUMNS)}")
                input_df = pd.DataFrame() # Set kosong agar tidak dilanjutkan
            else:
                # Pastikan urutan kolom sesuai dengan EXPECTED_COLUMNS
                input_df = input_df[EXPECTED_COLUMNS]

        except pd.errors.ParserError:
            st.error("Error: Tidak dapat membaca file CSV. Pastikan formatnya benar dan menggunakan titik koma (`;`) sebagai pemisah.")
            input_df = pd.DataFrame()
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memuat file: {e}")
            input_df = pd.DataFrame()


# Hanya lanjutkan jika ada data untuk diproses
if not input_df.empty:
    # Preprocessing data input
    try:
        input_processed = preprocessor.transform(input_df)
    except Exception as e:
        st.error(f"Error saat preprocessing input: {e}. Pastikan tipe data kolom sesuai.")
        st.stop()


    # Melakukan prediksi
    if st.button('Prediksi Status'):
        try:
            prediction = model.predict(input_processed)
            prediction_proba = model.predict_proba(input_processed)

            # Mengubah hasil prediksi numerik kembali ke label asli
            predicted_status_labels = label_encoder_status.inverse_transform(prediction)

            # Menampilkan hasil
            st.subheader('Hasil Prediksi:')
            if prediction_mode == 'Input Manual':
                st.write(f"Status Mahasiswa Diprediksi: **{predicted_status_labels[0]}**")
                st.subheader('Probabilitas Prediksi:')
                proba_df = pd.DataFrame(prediction_proba, columns=label_encoder_status.classes_)
                st.write(proba_df)
            else: # Mode Upload CSV
                results_df = input_df.copy() # Salin input asli
                results_df['Predicted_Status'] = predicted_status_labels

                # Tambahkan kolom probabilitas
                proba_cols = [f'Proba_{cls}' for cls in label_encoder_status.classes_]
                proba_df_temp = pd.DataFrame(prediction_proba, columns=proba_cols)
                results_df = pd.concat([results_df.reset_index(drop=True), proba_df_temp], axis=1)

                st.success("Prediksi berhasil dilakukan!")
                st.dataframe(results_df)

                # Opsi untuk download hasil
                csv_output = results_df.to_csv(index=False, sep=';').encode('utf-8')
                st.download_button(
                    label="Download Hasil Prediksi sebagai CSV",
                    data=csv_output,
                    file_name="hasil_prediksi_mahasiswa.csv",
                    mime="text/csv",
                )

        except Exception as e:
            st.error(f"Error saat melakukan prediksi: {e}")

st.sidebar.markdown("---")
