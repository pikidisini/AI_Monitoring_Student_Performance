# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

### Permasalahan Bisnis
Jumlah dropout yang tinggi ini tentunya menjadi salah satu masalah yang besar untuk sebuah institusi pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang mungkin akan melakukan dropout sehingga dapat diberi bimbingan khusus.

### Cakupan Proyek
Proyek ini bertujuan untuk:
1.  Melakukan analisis data eksploratif (EDA) pada dataset mahasiswa untuk mengidentifikasi pola dan faktor-faktor yang mungkin berkorelasi dengan status dropout.
2.  Melakukan pra-pemrosesan data yang diperlukan agar data siap digunakan untuk pemodelan machine learning.
3.  Mengembangkan model klasifikasi machine learning untuk memprediksi kemungkinan seorang mahasiswa akan dropout.
4.  Mengevaluasi performa model yang telah dibangun dan melakukan tuning hyperparameter untuk optimasi.
5.  Membuat dashboard interaktif untuk memvisualisasikan data siswa dan hasil analisis, guna memudahkan pihak institut dalam memonitor dan mengambil keputusan.

### Persiapan

Sumber data: [Student Performance Data Set](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv)

Dataset disediakan oleh Jaya Jaya Institut dalam file `data.csv`. Dataset ini berisi 37 kolom yang mencakup berbagai informasi mengenai mahasiswa, termasuk data demografi, status pendaftaran, kualifikasi sebelumnya, informasi akademik per semester (jumlah SKS yang diambil, dievaluasi, disetujui, dan nilai), serta data ekonomi makro. Variabel target adalah kolom 'Status' yang memiliki tiga kategori: Dropout, Enrolled, dan Graduate.

Setup environment:

```
pip install -r requirements.txt
```
# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

### Permasalahan Bisnis
Jumlah dropout yang tinggi ini tentunya menjadi salah satu masalah yang besar untuk sebuah institusi pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi secepat mungkin siswa yang mungkin akan melakukan dropout sehingga dapat diberi bimbingan khusus.

### Cakupan Proyek
Proyek ini bertujuan untuk:
1.  Melakukan analisis data eksploratif (EDA) pada dataset mahasiswa untuk mengidentifikasi pola dan faktor-faktor yang mungkin berkorelasi dengan status dropout.
2.  Melakukan pra-pemrosesan data yang diperlukan agar data siap digunakan untuk pemodelan machine learning.
3.  Mengembangkan model klasifikasi machine learning untuk memprediksi kemungkinan seorang mahasiswa akan dropout.
4.  Mengevaluasi performa model yang telah dibangun dan melakukan tuning hyperparameter untuk optimasi.
5.  Membuat dashboard interaktif menggunakan Metabase untuk memvisualisasikan data siswa dan hasil analisis.
6.  Mengembangkan prototipe solusi machine learning yang siap digunakan user menggunakan Streamlit dan melakukan deployment ke Streamlit Community Cloud.

### Persiapan

Sumber data: Sumber data: [Student Performance Data Set](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv)Untuk kemudahan, Anda dapat menginstal pustaka Python menggunakan `pip install -r requirements.txt` (pastikan Anda membuat file `requirements.txt` yang sesuai).

## Business Dashboard (Metabase)
Dashboard interaktif telah dibuat menggunakan **Metabase** untuk membantu Jaya Jaya Institut dalam memahami data dan memonitor performa siswa.

**Kredensial Akses Metabase (Contoh):**
*   Email: `root@mail.com`
*   Password: `root123`

**Deskripsi Dashboard:**
Dashboard ini menampilkan beberapa visualisasi utama, antara lain:
-   **Ringkasan Status Mahasiswa**: Pie chart yang menampilkan proporsi mahasiswa berdasarkan status akhir mereka (Dropout, Enrolled, Graduate).
-   **Status Pembayaran SPP berdasarkan Status Mahasiswa**: Bar chart yang membandingkan status kelunasan SPP (Tuition fees up to date) untuk setiap kategori status mahasiswa.
-   **Status Penerima Beasiswa berdasarkan Status Mahasiswa**: Bar chart yang menunjukkan perbandingan jumlah penerima beasiswa dan bukan penerima beasiswa untuk setiap status mahasiswa.
-   **Rata-rata SKS yang Disetujui (Semester 1 & 2) berdasarkan Status Mahasiswa**: Bar chart yang membandingkan rata-rata jumlah SKS yang disetujui pada semester pertama dan kedua untuk masing-masing status mahasiswa.
-   **Perbandingan Rata-rata Nilai (Semester 1 & 2) berdasarkan Status Mahasiswa**: Bar chart yang membandingkan rata-rata nilai akademik pada semester pertama dan kedua untuk setiap status mahasiswa.
-   **Distribusi Usia Saat Pendaftaran berdasarkan Status Mahasiswa**: Bar chart yang menunjukkan distribusi usia mahasiswa saat pertama kali mendaftar, dikelompokkan berdasarkan status akhir mereka.


**Ekspor Dashboard dan Database Instance dari Metabase:**
Setelah membuat dashboard, Anda dapat mengekspor dashboard beserta database instance dari container Metabase. Asumsikan nama container yang Anda buat adalah `metabase`, jalankan perintah berikut di terminal Anda:
```bash
# Untuk menjalankan analisis dan pelatihan model:
1.  **Pastikan Environment Siap**: Instal semua pustaka Python yang tercantum di bagian "Setup environment".
2.  **Unduh Dataset**: Pastikan file `data.csv` berada dalam direktori yang sama dengan file notebook `notebook.ipynb`.
3.  **Jalankan Jupyter Notebook**: Buka dan jalankan semua sel kode dalam file `notebook.ipynb`. Ini akan melakukan proses dari pemuatan data, pra-pemrosesan, pelatihan model, hingga evaluasi.
4.  **Lihat Hasil**: Output dari setiap tahap, termasuk statistik data, visualisasi, metrik evaluasi model, dan fitur penting akan ditampilkan langsung di dalam notebook.
Ekspor database Metabase (akan menghasilkan file metabase.db.mv.db atau serupa)
docker cp metabase:/metabase.db.mv.db .

# Untuk mengekspor dashboard secara spesifik, biasanya dilakukan melalui antarmuka Metabase
# atau dengan mengekspor seluruh aplikasi data jika menggunakan fitur serialisasi.
# Pastikan Anda mengikuti panduan Metabase untuk backup dan restore yang paling sesuai.
# Perintah di atas adalah untuk mengambil file database utama Metabase.


Dataset disediakan oleh Jaya Jaya Institut dalam file `data.csv`. Dataset ini berisi 37 kolom yang mencakup berbagai informasi mengenai mahasiswa, termasuk data demografi, status pendaftaran, kualifikasi sebelumnya, informasi akademik per semester (jumlah SKS yang diambil, dievaluasi, disetujui, dan nilai), serta data ekonomi makro. Variabel target adalah kolom 'Status' yang memiliki tiga kategori: Dropout, Enrolled, dan Graduate.

Setup environment:

## Business Dashboard
Jelaskan tentang business dashboard yang telah dibuat. Jika ada, sertakan juga link untuk mengakses dashboard tersebut.

## Menjalankan Sistem Machine Learning
Jelaskan cara menjalankan protoype sistem machine learning yang telah dibuat. Selain itu, sertakan juga link untuk mengakses prototype tersebut.

```

```

## Conclusion
Jelaskan konklusi dari proyek yang dikerjakan.

### Rekomendasi Action Items
Berikan beberapa rekomendasi action items yang harus dilakukan perusahaan guna menyelesaikan permasalahan atau mencapai target mereka.
- action item 1
- action item 2
