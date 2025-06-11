# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

### Permasalahan Bisnis

1. Tingginya angka dropout mahasiswa menjadi tantangan serius bagi Jaya Jaya Institut karena dapat memengaruhi reputasi, kualitas pendidikan, dan efisiensi operasional institusi.
2. Belum adanya solusi berbasis teknologi seperti sistem prediksi yang dapat mendukung pengambilan keputusan dalam manajemen pendidikan.
3. Ketiadaan alat bantu analisis dan visualisasi yang dapat digunakan pihak manajemen untuk memonitor kondisi mahasiswa secara real-time dan berbasis data.

### Cakupan Proyek

Proyek ini bertujuan untuk:

1.  Melakukan analisis mengidentifikasi pola dan faktor-faktor yang berkontribusi terhadap risiko dropout.
2.  Mengembangkan prototipe aplikasi machine learning prediktif berbasis Streamlit untuk memudahkan staf akademik mengevaluasi risiko dropout berdasarkan hasil prediksi model.
3.  Membangun dashboard interaktif menggunakan Metabase untuk menyajikan visualisasi data mahasiswa dan hasil analisis dropout

### Persiapan

Sumber data: Sumber data: [Student Performance Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv)

#### Setup environment:

##### Windows

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

##### Linux/Mac

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

##### Conda

```
conda create --name attrition-ds python=3.10.6
conda activate attrition-ds
pip install -r requirements.txt
```

## Business Dashboard (Metabase)

Dashboard interaktif telah dibuat menggunakan **Metabase** untuk membantu Jaya Jaya Institut dalam memahami data dan memonitor performa siswa. Dashboard ini dibuat menggunakan Metabase. Dashboard beserta database instance telah di ekspor pada `metabase.db.mv.db` yang disimpan pada direktori `metabase-data` dan telah disediakan file `docker-compose.yml` pada direktori utama untuk menjalankan dashboard.

### Menjalankan Dashboard Metabase Docker

1. Install Docker Download & install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Buka CMD di direktori tempat file `docker-compose.yml` berada
3. Jalankan Metabase Container
   ```
   docker-compose up
   ```
4. Buka di Browser: http://localhost:3000
5. Untuk menghentikan Container tekan `Ctrl + c` pada CMD
6. Untuk menghapus container
   ```
   docker-compose down
   ```

**Kredensial Akses Metabase (Contoh):**

- Email: `root@mail.com`
- Password: `root123`

**Deskripsi Dashboard:**
Dashboard ini menampilkan beberapa visualisasi utama, antara lain:

- **Ringkasan Status Mahasiswa**: Pie chart yang menampilkan proporsi mahasiswa berdasarkan status akhir mereka (Dropout, Enrolled, Graduate).
- **Status Pembayaran SPP berdasarkan Status Mahasiswa**: Bar chart yang membandingkan status kelunasan SPP (Tuition fees up to date) untuk setiap kategori status mahasiswa.
- **Status Penerima Beasiswa berdasarkan Status Mahasiswa**: Bar chart yang menunjukkan perbandingan jumlah penerima beasiswa dan bukan penerima beasiswa untuk setiap status mahasiswa.
- **Rata-rata SKS yang Disetujui (Semester 1 & 2) berdasarkan Status Mahasiswa**: Bar chart yang membandingkan rata-rata jumlah SKS yang disetujui pada semester pertama dan kedua untuk masing-masing status mahasiswa.
- **Perbandingan Rata-rata Nilai (Semester 1 & 2) berdasarkan Status Mahasiswa**: Bar chart yang membandingkan rata-rata nilai akademik pada semester pertama dan kedua untuk setiap status mahasiswa.
- **Distribusi Usia Saat Pendaftaran berdasarkan Status Mahasiswa**: Bar chart yang menunjukkan distribusi usia mahasiswa saat pertama kali mendaftar, dikelompokkan berdasarkan status akhir mereka.

## Menjalankan Sistem Machine Learning

Model yang terlatih telah di deploy menggunakan streamlit dan siap digunakan untuk melakukan prediksi pada data baru. Data bisa dimasukan secara manual atau mengunggah file berekstensi '.csv' dengan format kolom / fitur yang sesuai dengan data yang digunakan untuk melatih model. Untuk mengakses aplikasinya, anda dapat mengunjungi laman dibawah ini:

URL Aplikasi Streamlit: [Student Performance Monitor App](https://studentperformancemonitor.streamlit.app/)

Sebagai contoh, anda bisa menggunakan file data dummy `data_mahasiswa_baru.csv` yang tersedia di direktori utama untuk uji coba prediksi pada model yang telah dideploy ke streamlit.

## Conclusion

Proyek ini berhasil mengembangkan solusi untuk membantu Jaya Jaya Institut dalam memprediksi status mahasiswa, dengan fokus utama pada identifikasi mahasiswa yang berpotensi dropout.

1. Analisis data awal menunjukkan bahwa dataset tidak memiliki nilai yang hilang namun terdapat ketidakseimbangan kelas pada variabel target 'Status', di mana jumlah mahasiswa 'Graduate' paling banyak, diikuti 'Dropout', dan 'Enrolled'.

2. Model awal `RandomForestClassifier` (tanpa tuning ekstensif selain `class_weight='balanced'`) menunjukkan akurasi 100% pada data latih dan ~74.9% pada data uji. Ini mengindikasikan overfitting yang signifikan. Meskipun demikian, model ini menunjukkan kemampuan yang baik dalam membedakan kelas 'Dropout' dengan ROC AUC Score untuk kelas 'Dropout' sebesar 0.9099 pada data uji, dan recall sebesar 0.75. Namun, performa pada kelas 'Enrolled' sangat rendah (recall 0.27).

3. Setelah dilakukan hyperparameter tuning menggunakan `GridSearchCV` dengan parameter terbaik `{'max_depth': 10, 'min_samples_leaf': 4, 'min_samples_split': 2, 'n_estimators': 300}`, model `RandomForestClassifier` yang dioptimalkan menunjukkan akurasi ~74.8% pada data uji. Perbaikan signifikan terlihat pada recall kelas 'Enrolled' yang meningkat menjadi 0.62, dan presisi kelas 'Dropout' meningkat menjadi 0.81. Meskipun recall kelas 'Dropout' sedikit menurun menjadi 0.69, `macro avg f1-score` meningkat dari 0.65 menjadi 0.71, menunjukkan performa yang lebih seimbang antar kelas.

4. Analisis fitur penting dari model Random Forest (sebelum tuning) mengidentifikasi bahwa performa akademik di semester awal (jumlah SKS yang disetujui dan nilai semester 1 & 2) serta status pembayaran SPP (`Tuition_fees_up_to_date`) adalah prediktor yang sangat dominan. Fitur-fitur lain seperti nilai masuk, usia saat pendaftaran, dan status beasiswa juga menunjukkan kontribusi.

5. Dashboard telah berhasil dibuat menggunakan Metabase, yang menyajikan berbagai visualisasi seperti ringkasan status mahasiswa, status pembayaran SPP, status beasiswa, rata-rata SKS, perbandingan nilai semester, dan distribusi usia pendaftaran, semuanya dikelompokkan berdasarkan status mahasiswa. Dashboard ini dapat diakses dan dijalankan menggunakan Docker dengan kredensial yang telah disediakan.

6. Sebagai solusi machine learning yang siap digunakan, sebuah prototipe aplikasi web telah dikembangkan menggunakan Streamlit dan di-deploy ke Streamlit Community Cloud. Aplikasi ini memungkinkan pengguna untuk melakukan prediksi status mahasiswa baik dengan input manual maupun dengan mengunggah file CSV. Hasil prediksi, termasuk probabilitas untuk setiap kelas, dapat dilihat dan diunduh oleh pengguna.

Secara keseluruhan, proyek ini menyediakan alat bantu berbasis data (dashboard Metabase) untuk monitoring dan alat prediksi (aplikasi Streamlit) yang dapat digunakan oleh Jaya Jaya Institut untuk mengambil tindakan preventif terhadap mahasiswa yang berpotensi dropout.

### Rekomendasi Action Items

Berikut beberapa rekomendasi action items yang bisa dilakukan oleh Jaya Jaya Institut untuk menyelesaikan permasalahan bisnis dan mencapai target yang diinginkan:

1. **Mengembangkan program pendampingan akademik bagi mahasiswa berisiko tinggi:** Berdasarkan hasil prediksi model, mahasiswa dengan performa akademik rendah di semester awal dan status pembayaran SPP yang belum lunas memiliki risiko tinggi untuk dropout. Institusi dapat membuat program mentoring atau konseling khusus bagi mahasiswa dalam kategori ini untuk membantu mereka secara akademik maupun finansial.

2. **Meninjau kembali kebijakan keuangan dan beasiswa:** Salah satu faktor signifikan penyebab dropout adalah ketidakmampuan membayar SPP tepat waktu. Jaya Jaya Institut dapat mempertimbangkan skema pembayaran yang lebih fleksibel atau memperluas cakupan program beasiswa bagi mahasiswa yang memiliki performa baik namun terkendala secara finansial.

3. **Menggunakan dashboard Metabase secara rutin dalam evaluasi akademik:** Visualisasi data dari Metabase seperti status SPP, beasiswa, nilai akademik, dan distribusi usia dapat digunakan dalam rapat akademik berkala untuk mengidentifikasi pola dan kelompok mahasiswa yang membutuhkan perhatian khusus.
