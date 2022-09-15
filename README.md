# Proyek Django PBP

Pemrograman Berbasis Platform (CSGE602022) - diselenggarakan oleh Fakultas Ilmu Komputer Universitas Indonesia, Semester Ganjil 2022/2023

Muhammad Nabiel Andityo Purnomo - 2106750465

## Tugas 2 - Membuat Aplikasi Katalog

### Link to Deployed App

[LINK HEROKU](https://assignment-2-nabiel.herokuapp.com/katalog/)

### Cara Kerja Django

![Bagan Django](https://github.com/mnabielap/assignment-2/blob/main/assignment2_img.gif)

Django didasarkan pada arsitektur MVT (Model-View-Template). Dimana, **MVT** adalah pola desain perangkat lunak untuk mengembangkan aplikasi web. Model akan bertindak sebagai *interface data developer*. Model ini akan bertanggung jawab untuk menjaga data. Ini adalah *logical data structure* di balik seluruh aplikasi dan diwakili oleh *database* (umumnya *database* relasional seperti MySql, Postgres). Views adalah user interface, apa yang user lihat di browser saat user me-*render* situs web. Itu diwakili oleh HTML atau dengan kata lain views merupakan tempat algoritma yang akan melakukan proses berdasarkan *request* dan *response* untuk menjalankan aplikasi tersebut. Template terdiri dari *static part* dari *output* HTML yang diinginkan serta beberapa sintaks khusus yang menjelaskan bagaimana *dynamic content* akan dimasukkan. 

Dalam pengaplikasinya dapat diawali oleh *request* dari *user* untuk aplikasi ini, file `urls.py` pada folder `project_django` akan melakukan routing berasal dari url *request* yang diterima ke *server*. Selanjutnya, jika aplikasi yang diminta *user*, seperti **katalog**, maka server akan dapat menampilkan aplikasi untuk *user*. Dalam folder katalog, terdapat `urls.py` yang bertugas untuk mengatur *routing* untuk url dengan nama prefix `katalog/`. Jika tidak ada tambahan, yang akan dipanggil adalah function `show_katalog()` dari file `views.py`. Function `show_katalog` akan memanggil data `CatalogItem` pada `models.py` dari data base yang berupa `.json`. Selanjutnya, function ini akan me-render file `katalog.html` yang berada dalam folder template yang akan digunakan sebagai `front-end` yang akan dilihat pengguna. Akhirnya, setelah semuanya telah dijalankan, user sekarang dapat melihat aplikasi katalog dengan data yang tersedia.

### Penggunaan Virtual Environment

Virtual Environment adalah alat yang membantu menjaga `dependencies` tetap diperlukan dan proyek tetap terisolasi. Jika kita ingin menginstal new library dan menulis `pip install name_of_library` di terminal tanpa mengaktifkan environment, semua paket akan diinstal secara global yang bukan *good practice* jika kita bekerja dengan proyek yang berbeda di komputer kita.

Untuk membuat *environment* baru, buka terminal baru dan temukan folder tempat kita ingin menyimpan proyek kita. Di dalam direktori itu jalankan perintah `python -m venv name_of_the_environment`. Setelah membuat environment kita dapat mengaktifkannya dengan cara `env\Scripts\activate.bat`. Virtual Environment ini berguna jika kita tidak ingin menginstall *requirements* secara global atau hanya pada *project* yang ingin kita jalankan.

### Penjelasan Step-by-step

1. Membuat sebuah fungsi pada `views.py` yang dapat melakukan pengambilan data dari model dan dikembalikan ke dalam sebuah HTML.

Dalam mengerjakan tugas 2 ini, yang pertama saya lakukan adalah melakukan *fork* dengan cara `Use this template` berdasarkan repository awal yakni [Template Tugas 2](https://github.com/pbp-fasilkom-ui/assignment-repository). Setelah itu, saya melakukan *clone* terhadap *repository* saya yang telah di *fork* ke dalam lokal komputer. Lalu, didalam file `views.py` saya membuat fungsi `show_katalog()` yang berguna untuk mengambil data melalui `CatalogItem.objects.all()` yang di-*import* dari `/katalog/models` yang berisi model *setting* dan *item name* dari yang akan nantinya ditampilkan. Di dalam file `views.py` saya juga membuat sebuah *dictionary* bernama `context` yang nantinya akan ditampilkan kepada user melalui file HTML yang berisi nama, npm, dan list_catalog. Selanjutnya, melakukan return permanggilan function render dengan parameter `(request, 'katalog.html', context)`.

2. Membuat sebuah *routing* untuk memetakan fungsi yang telah kamu buat pada `views.py`

Dalam membuat *routing*, saya menambahkan *array* yang bernama `urlpatterns` yang berisi alamat path dari aplikasi dan pemanggilan fungsinya. Sebagai contoh, untuk path `katalog/` maka akan memanggil fungsi `show_katalog()` dari views. Selajutnya, saya memasukkan path `katalog/` ke dalam `project_django/urls.py` agar django dapat mendeteksi aplikasi katalog.

3. Memetakan data yang didapatkan ke dalam HTML dengan sintaks dari Django untuk pemetaan data template.

Untuk memetakan/menyambungkan data yang ada dalam file `initial_catalog_data.json` ke dalam file template `katalog.html`, saya menggunakan perintah `python manage.py loaddata initial_catalog_data.json` untuk memasukkan data tersebut ke dalam database Django lokal. Sedangkan untuk menampilkan data yang didapatkan dari json file ke HTML saya menggunakan syntax `{% for item in list_item %}` yang merupakan for loop dari file json dengan `CatalogItem`. Pada setiap iterasinya akan membuat sebuah baris yang berisikan data atribut. Selain itu, saya juga menampilkan nama dan NPM pada bagian atas tabel yang diambil dari context dalam `views.py`

4. Melakukan deployment ke Heroku terhadap aplikasi yang sudah kamu buat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.

Dalam melakukan deployment yang pertama saya lakukan adalah dengan membuat `new app` dari website Heroku dengan nama `assignment-2-nabiel`. Selanjutnya, saya membuat secret yang berada dalam settings repositori saya dengan nama `HEROKU_APP_NAME` yang disesuaikan dengan nama aplikasi yang ada dalam website Heroku, yakni `assignment-2-nabiel` dan `HEROKU_API_KEY` yang didapatkan dari Account Settings akun website Heroku. Setelah itu, saya membuka tab Actions dan dalam bagian workflow saya lakukan `Re-run all jobs` dengan menunggu kurang dari 5 menit akhirnya aplikasi saya dapat ditampilkan dengan alamat https://assignment-2-nabiel.herokuapp.com/katalog/ 

## Credits

Template ini dibuat berdasarkan [PBP Ganjil 2021](https://gitlab.com/PBP-2021/pbp-lab) yang ditulis oleh Tim Pengajar Pemrograman Berbasis Platform 2021 ([@prakashdivyy](https://gitlab.com/prakashdivyy)) dan [django-template-heroku](https://github.com/laymonage/django-template-heroku) yang ditulis oleh [@laymonage, et al.](https://github.com/laymonage). Template ini dirancang sedemikian rupa sehingga mahasiswa dapat menjadikan template ini sebagai awalan serta acuan dalam mengerjakan tugas maupun dalam berkarya.

