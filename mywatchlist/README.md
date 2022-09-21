# Proyek Django PBP

Pemrograman Berbasis Platform (CSGE602022) - diselenggarakan oleh Fakultas Ilmu Komputer Universitas Indonesia, Semester Ganjil 2022/2023

Muhammad Nabiel Andityo Purnomo - 2106750465

## Tugas 3 - Pengimplementasian Data Delivery Menggunakan Django

### Link to Deployed App

[LINK HEROKU](https://assignment-pbp-nabiel.herokuapp.com/mywatchlist/)

### Definisi HTML, XML, and JSON
- **HTML** adalah Singkatan dari "Hypertext Markup Language" yang merupakan bahasa standar pemrogaman yang digunakan untuk membuat halaman atau tampilan *website*, yang diakses melalui internet. 
- **XML** adalah kepanjangan dari Extensible Markup Language adalah bahasa *markup* dan *format file* untuk menyimpan, mentransmisikan, dan merekonstruksi *arbitrary data*.
- **JSON** adalah kepanjangan dari JavaScript Object Notation adalah format file standar terbuka dan format pertukaran data yang menggunakan teks yang dapat dibaca manusia untuk menyimpan dan mengirimkan objek data yang terdiri dari pasangan atribut-nilai dan *arrays*.

### Perbedaan HTML, XML, and JSON

HTML dan XML keduanya akan membungkus konten dalam tag, tetapi XML lebih ketat mengenai tag mana yang dapat digunakan kapan dan di mana. Oleh karena itu, XML biasanya bertanggung jawab untuk mengirim dan 
menerima data dan HTML biasanya bertanggung jawab untuk memformat dan menampilkan data. JSON memiliki tujuan yang mirip dengan XML, tetapi JSON lebih populer daripada XML karena aplikasi web dikembangkan menggunakan bahasa seperti JavaScript dan JSON adalah cara menyusun informasi 
dengan cara yang dapat lebih mudah dan lancar berinteraksi dengan bahasa-bahasa tersebut. Selain itu, XML dan JSON difokuskan untuk transfer data sedangkan HTML difokuskan untuk tampilan. 

Dengan demikian dapat disimpulkan, Dalam menampilkan data, JSON menggunakan notasi objek JavaScript untuk merepresentasikan data, sedangkan XML merepresentasikan data dalam bentuk element tree, hampir sama seperti HTML. 
HTML merepresentasikan data dalam bentuk element tree, tetapi data yang direpresentasikan lebih ditujukan untuk ditampilkan pada web browser.

### Mengapa memerlukan data delivery pada platform

Sebuah platform dapat menggunakan data dari banyak tujuan, jadi kita perlu memiliki pengiriman data untuk mempermudah pengiriman data ke banyak platform. Demikian, penggunaan *data delivery* seperti JSON, XML, dan 
HTML dapat mempermudah pekerjaan para *developer* karena file JSON, XML, dan HTML dapat dibaca oleh manusia. Dalam hal ini, *data delivery* sangat dibutuhkan di dalam proses kerja platform, karena jika tidak ada 
mekanisme ini maka data dari *database* JSON tidak bisa ditampilkan di sisi *front-end*. *Data delivery* disini berguna sebagai *dynamic content* yang terus berubah-ubah mengikuti *database* terkini.

### Step-by-step implementation

1. Pertama-tama saya membuat aplikasi baru oleh command yang telah disiapkan django, yakni `python manage.py startapp mywatchlist`

2. Setelah itu, saya menambahkan `mywatchlist` ke dalam `INSTALLED_APPS` pada `project_django/settings.py`
	```
	INSTALLED_APPS = [
		...
		'mywatchlist',
	]
	```
	
3. Lalu, saya menambahkan `urlpatterns` yang ada di dalam file `project_django/urls.py`
	```
	urlpatterns = [
		...
		path('mywatchlist/', include('mywatchlist.urls')),
	]
	```
	
4. Selanjutnya saya membuat *routing* dalam `urlpatterns` untuk aplikasi `mywatchlist` dalam `mywatchlist/urls.py`
	```
	from django.urls import path
	from mywatchlist.views import show_html, show_xml, show_json

	urlpatterns = [
		path('', show_html, name='watchlist'),
		path('html/', show_html, name='show_html'),
		path('xml/', show_xml, name='show_xml'),
		path('json/', show_json, name='show_json'),
	]
	```
	File `urls.py` akan melakukan routing berdasarkan kemauan pengguna.
	
5. Selanjutnya, saya menambahkan model pada file `mywatchlist/models.py`
	```
	from django.db import models
	from django.core.validators import MaxValueValidator, MinValueValidator

	class MyWatchlist(models.Model):
		watched = models.BooleanField()
		title = models.CharField(max_length=255)
		rating = models.IntegerField(
			validators=[MinValueValidator(1), MaxValueValidator(5)]
		)
		release_date = models.DateField()
		review = models.TextField()
	```
	Setelah melakukan perubahan kepada `mywatchlist/models.py`, saya jalan kan perintah
	`python manage.py makemigrations` dan `python manage.py migrate` untuk memigrasikan perubahan model ke database.
	
6. Langkah selanjutnya yang saya lakukan, yakni membuat fungsi `show_html`, `show_xml`, dan `show_json` pada file `mywatchlist/views.py`.

	Berguna untuk meng-*import* `MyWatchlist` dari `models.py`
	`from mywatchlist.models import MyWatchlist`
	Hal diatas menggunakan `MyWatchList` model dalam pengambilan data dari *database* `initial_movies_data.json`
	
	```
	def show_html(request):
		data = MyWatchlist.objects.all()
		watched = 0
		not_watched = 0
		for movie in data:
			if movie.watched:
				watched += 1
			else:
				not_watched += 1
		
		
		context = {
			'nama': 'Muhammad Nabiel Andityo Purnomo',
			'npm': '2106750465',
			'movie_watched': watched,
			'movie_not_watched':not_watched,
			'watchlist': data,
		}
		return render(request, 'mywatchlist.html', context)
	```
	Fungsi `show_html` me-*render* template `mywatchlist.html` dengan data yang dikirim didalam *dictionary* `context`.
	 
	```
	def show_xml(request):
		data = MyWatchlist.objects.all()
		return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
	```
	Fungsi `show_xml` berguna untuk membuat data berformat xml dengan data yang diambil dari database
	
	```
	def show_json(request):
		data = MyWatchlist.objects.all()
		return HttpResponse(serializers.serialize("json", data), content_type="application/json")
	```
	Fungsi `show_json` berguna untuk merender data berformat json dengan data yang diambil dari database.
	
7. Step selanjutnya, saya membuat json file sebagai *database* didalam `mywatchlist/fixtures/` yang bernama `initial_movies_data.json` dan saya isi sebagai data movie watchlist.
Salah satu contohnya adalah:
	```
	[
		{
			"model": "mywatchlist.mywatchlist",
			"pk": 1,
			"fields": {
				"watched": true,
				"title": "Avengers Endgame",
				"rating": 4,
				"release_date": "2019-04-24",
				"review": "This film is an emotional rollercoaster with some of the coolest superhero plot lines ever drawn up. It's straight up the most epic Marvel film that will probably ever be created."
			}
		},
		...
	]
	```
	
8. Lalu, saya membuat template `mywatchlist.html` yang berada dalam `mywatchlist/templates/`.
Gunanya untuk menjadikan tampilan webpage kepada pengguna.

9. Membuat test unit untuk mengecek apakah terdapat masalah, dengan cara
	- membuat fungsi didalam file `mywatchlist/tests.py` untuk *response test* setiap *page* dari mywatchlist
	- menjalankan command `python manage.py collectstatic` to gather all static files into a folder called staticfiles in our project root directory.
	- menjalankan command `python manage.py test mywatchlist` untuk memulai menjalankan *response test*

10. Untuk load data dari database `initial_movies_data.json`, saya menggunakan `command`
	`python manage.py loaddata initial_movies_data.json`
	
11. Menambahkan command diatas kedalam `Procfile` agar Heroku dapat membaca file database.

12. Deploy to Heroku.
Karena menggunakan *repository* assignment-2 maka deploy cukup dilakukan dengan push to github.
Lalu, membuka tab `Actions` dan dalam bagian workflow lakukan `Re-run all jobs` dengan menunggu kurang dari 5 menit 
akhirnya aplikasi saya dapat ditampilkan dengan alamat https://assignment-pbp-nabiel.herokuapp.com/mywatchlist/

### Postman Screenshot

#### Response HTML Page 
![postman-html](https://github.com/mnabielap/assignment-2/blob/main/img/postman-html.png)

#### Response JSON Page
![postman-json](https://github.com/mnabielap/assignment-2/blob/main/img/postman-json.png)

#### Response XML Page
![postman-xml](https://github.com/mnabielap/assignment-2/blob/main/img/postman-xml.png) 

## Credits

Template ini dibuat berdasarkan [PBP Ganjil 2021](https://gitlab.com/PBP-2021/pbp-lab) yang ditulis oleh Tim Pengajar Pemrograman Berbasis Platform 2021 ([@prakashdivyy](https://gitlab.com/prakashdivyy)) dan [django-template-heroku](https://github.com/laymonage/django-template-heroku) yang ditulis oleh [@laymonage, et al.](https://github.com/laymonage). Template ini dirancang sedemikian rupa sehingga mahasiswa dapat menjadikan template ini sebagai awalan serta acuan dalam mengerjakan tugas maupun dalam berkarya.

