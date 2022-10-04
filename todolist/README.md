# Proyek Django PBP

Pemrograman Berbasis Platform (CSGE602022) - diselenggarakan oleh Fakultas Ilmu Komputer Universitas Indonesia, Semester Ganjil 2022/2023

Muhammad Nabiel Andityo Purnomo - 2106750465

- [Tugas 4](#tugas-4---pengimplementasian-form-dan-autentikasi-menggunakan-django)
- [Tugas 5](#tugas-5---web-design-using-html-css-and-css-framework)

## Tugas 4 - Pengimplementasian Form dan Autentikasi Menggunakan Django

### Link to Deployed App

[LINK HEROKU](https://assignment-pbp-nabiel.herokuapp.com/todolist/)

### Apa kegunaan `{% csrf_token %}` pada elemen `<form>`? Apa yang terjadi apabila tidak ada potongan kode tersebut pada elemen `<form>`?

CSRF merupakan kepanjangan dari Cross Site Request Forgery. Seperti namanya, CSRF adalah sejenis serangan terhadap situs yang kebanyakan 
dilakukan oleh situs lain (jahat), atau terkadang oleh pengguna (jahat) di situs tersebut.

Untuk menghidari hal tersebut, Django memiliki tag `{% csrf_token %}` untuk menghindari serangan berbahaya. Ini menghasilkan token di sisi 
server saat merender halaman dan memastikan untuk memeriksa ulang token ini untuk setiap permintaan yang masuk kembali. Jika permintaan 
yang masuk tidak berisi token, permintaan tersebut tidak akan dieksekusi.

Sebuah situs biasanya mengidentifikasi pengguna yang diautentikasi dengan menyimpan cookie dengan header dan konten yang mewakili pengguna 
tertentu di browser mereka. Penyerang menggunakan ini untuk mengakses kredensial pengguna untuk melakukan serangan mereka.
Oleh karena itu, jika tidak ada `{% csrf_token %}` dalam elemen form tersebut, situs-situs berbahaya dapat menggunakan dan memanfaatkan 
data-data yang dimiliki pengguna yang sedang menggunakan website kita dalam pengisian form yang mengatasnamakan *user* target.

### Apakah kita dapat membuat elemen `<form>` secara manual (tanpa menggunakan generator seperti `{{ form.as_table }}`)? Jelaskan secara gambaran besar bagaimana cara membuat `<form>` secara manual.

Kita dapat membuat form secara manual dengan cara berikut ini. Pertama-tama, kita diharuskan untuk menyediakan variabel untuk
menyimpan data yang diberikan di form. Dalam tempate HTML kita dapat memanfaatkan tag `<input>`. Tentu saja, tidak lupa untuk
memberikan tag `{% csrf_token %}` dan juga `<form>` untuk menghidari *attacker*. Selanjutnya, dalam file `views.py`, kita dapat
membuat request dari form yang telah diisi *user* dengan potongan code `request.POST.get(data)` yang disimpan kedalam variabel 
di *function* `create_task`. Setelah itu, dibawahnya dapat ditambahkan perintah `Task.objects.create` untuk membuat object dari
task. Dan tentunya, di simpan dengan menggunakan `task.save()`.

### Jelaskan proses alur data dari submisi yang dilakukan oleh pengguna melalui HTML form, penyimpanan data pada database, hingga munculnya data yang telah disimpan pada template HTML.

Proses alur data yang terjadi adalah pertama-tama *user* mengisi dan mengirimkan data mereka melalui form. Lalu, ketika
CSRF token sesuai, maka server tersebut akan mengolah dan menerima data dari *user* dalam hal ini `views.py` akan 
menerima data dari form tersebut dan melakukan `task.save()` agar data tersebut dapat disimpan ke dalam database django. 
Selanjutnya, data-data tersebut yang terdapat pada database akan diambil agar dapat ditampilkan ke dalam template HTML.

### Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.

1. Membuat suatu aplikasi baru bernama `todolist` di proyek tugas Django yang sudah digunakan sebelumnya.

	Dilakukan dengan perintah pada CMD.
	
	`env\Scripts\activate.bat` 
	untuk mengaktifkan environment
	
	`python manage.py startapp todolist`
	untuk membuat app baru

2. Menambahkan path `todolist` sehingga pengguna dapat mengakses http://localhost:8000/todolist.
	
	Pertama, tambahkan app baru dalam `proyek_django/settings.py`
	```python
	INSTALLED_APPS = [
		...
		'todolist',
	]
	```
	Lalu, data alamat routing tersebut dapat ditambahkan dalam `proyek_django/urls.py`
	```python
	urlpatterns = [
		...
		path('todolist/', include('todolist.urls')),
	]
	```
	
3. Membuat sebuah model Task yang memiliki atribut sebagai berikut:

	Step ini dapat dilakukan dengan menambahkan model Task dalam `todolist/models.py` dengan kode.
	```python
	class Task(models.Model):
		user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) # user yang membuat task
		date = models.DateField(auto_now=True)			# alokasi untuk merepresentasikan tanggal dibuatnya task
		title = models.CharField(max_length=250)		# alokasi untuk menampung string pendek dari judul
		description = models.TextField()			# alokasi untuk menampung string panjang dari deskripsi
		is_finished = models.BooleanField(default=False)	# alokasi untuk mengampung status task (boolean) merupakan bonus
	```
	
4. Mengimplementasikan form registrasi, login, dan logout agar pengguna dapat menggunakan `todolist` dengan baik.

	Untuk form registrasi, saya menggunakan `UserCreationForm` dalam `views.py` untuk membuat form registrasi. Selanjutnya untuk 
	bagian login, saya lakukan di dalam fungsi `views.py` dengan `authenticate` yang akan melakukan validasi berdasarkan data yang telah di register,
	ketika *user* tersebut sudah melakukan registrasi dan password sesuai maka login sukses dan langsung ditujukan ke halaman utama `todolist`. 
	Lalu, untuk bagian `logout` saya melakukan logout request dan delete cookie yang dibuat saat pada `login` dan redirect kembali ke halaman `login`
	
5. Membuat halaman utama `todolist` yang memuat username pengguna, tombol `Tambah Task Baru`, tombol `logout`, serta tabel berisi tanggal pembuatan task, judul task, dan deskripsi task.

	Hal ini saya lakukan dengan membuat template terlebih dahulu untuk halaman utama todolist dengan nama
	`todolist.html` yang berisi *button*-*button* untuk melakukan aksi penambahan task, update task, dan
	delete task.
	
	*Button*-*button* tersebut akan mengarahkan url mana yang akan dituju ketika *user* mengklik tombol tersebut.
	Misalnya ketika *user* mengklik `Create Task` maka akan otomatis ke halaman `create_task` untuk membuat 
	task, begitu juga untuk tombol `update-task` dan `delete-task`. Dimana `update-task` akan mengarahkan ke url
	`update-task/id` yang akan *invert* is_finished dari task lalu kembali ke page `todolist` utama. Jika tombol 
	`delete-task` juga akan mengarahkan ke url `delete-task/id` dan menghapus object dari task tersebut.
	
6. Membuat halaman form untuk pembuatan task. Data yang perlu dimasukkan pengguna hanyalah judul task dan deskripsi task.

	Pada step ini saya menggunakan `ModelForm` untuk memetakan model Task berdasarkan `models.py` 
	yang merupakan data yang akan diisi *user* ketika membuat task baru. Dalam file `forms.py`
	saya membuat fields yang berisi `title` dan `description` yang akan diminta ketika mengisi form `create-task`. 
	Setelah mengisi form, objek task setiap *user* nantinya akan ditampilkan pada halaman utama
	`todolist`. Dimana `forms.py` tersebut berisi
	```python
	class TaskForm(ModelForm):
		class Meta:
			model = Task
			fields = ['title', 'description']
	```
	
7. Membuat routing sehingga beberapa fungsi dapat diakses melalui URL berikut:

	Membuat routing tersebut dapat dilakukan dengan mengambahkan `urlpatterns` pada `todolist/urls.py` dengan
	```python
	urlpatterns = [
		path('', show_todolist, name='show_todolist'),		# berisi halaman utama yang memuat tabel task.
		path('register/', register, name='register'),		# berisi form registrasi akun.
		path('login/', login_user, name='login'),		# berisi form login
		path('logout/', logout_user, name='logout'),		# mekanisme logout
		path('create-task/', create_task, name='create_task'),	# berisi form pembuatan task
		path('delete-task/<int:id>/', delete_task, name='delete-task'),		# mekanisme delete task
		path('update-task/<int:id>', update_status, name='update-task'),	# mekanisme update status task
	]
	```
	
8. Melakukan deployment ke Heroku terhadap aplikasi yang sudah kamu buat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
	
	Pada tahap ini, saya hanya melakukan *push* ke github karena konfigurasi *secret* sudah dilakukan
	pada assignment sebelumnya. Lalu, menunggu *github action* dalam melakukan *deployment* ke Heroku.
	Setelah berhasil, maka terdapat tanda *checklist* berwarna hijau di atas *repository* kita.
	Dengan demikian, aplikasi `todolist` sudah dapat diakses pada website https://assignment-pbp-nabiel.herokuapp.com/todolist/
	
9. Membuat dua akun pengguna dan tiga dummy data menggunakan model Task pada akun masing-masing di situs web Heroku.

	Hal ini dapat diimplementasikan dengan cara *user* membuat akun melalui halaman registrasi. Setelah itu, login dan
	masuk ke halaman utama `todolist` untuk membuat tiga task dalam form `create-task` pada akun masing-masing dengan jumlah
	dua akun.

## Tugas 5 - Web Design Using HTML, CSS, and CSS Framework

### Apa perbedaan dari Inline, Internal, dan External CSS? Apa saja kelebihan dan kekurangan dari masing-masing style?

Perbedaan utama antara *inline CSS* dan *external CSS* adalah bahwa *inline CSS* diproses lebih cepat karena hanya memerlukan 
browser untuk mengunduh 1 file sedangkan menggunakan *external CSS* akan memerlukan pengunduhan file HTML dan CSS secara terpisah.
Untuk perbedaan lebih rinci saya paparkan dibawah ini<br>

- __Internal CSS:__<br>
*Internal* atau *embedded CSS* mengharuskan kita untuk menambahkan tag `<style>` di bagian `<head>` dokumen HTML kita. *Style CSS* ini adalah 
metode yang efektif untuk menata satu halaman. Namun, menggunakan *style* ini untuk beberapa halaman memakan waktu karena kita perlu 
menempatkan *CSS rules* di setiap halaman situs web kita.<br>
	```html
	<!DOCTYPE html>
	<html>
		<head>
			<style>
			body {
				background-color: blue;
			}
			h1 {
				color: red;
				padding: 60px;
			} 
			</style>
		</head>
		<body>

			<h1>PBP Tutorials</h1>
			<p>This is our paragraph.</p>

		</body>
	</html>
	```
	
- __External CSS:__<br>
Dengan external CSS, kita akan menautkan halaman web kita ke file `.css` eksternal, yang dapat dibuat oleh editor teks apa pun di perangkat kita 
(mis., Notepad ). Jenis CSS ini adalah metode yang lebih efisien, terutama untuk menata situs web besar. Dengan mengedit satu file `.css`, kita 
dapat mengubah seluruh situs sekaligus.<br><br>
Cara untuk mengaplikasikan *external CSS* ini adalah
1. Buat file `.css` baru dengan editor teks, dan tambahkan *style rules*. Sebagai contoh:<br>
	```html
	.xleftcol {
	   float: left;
	   width: 33%;
	   background:#809900;
	}
	.xmiddlecol {
	   float: left;
	   width: 34%;
	   background:#eff2df;
	}
	```<br>
2. Di bagian `<head>` file HTML kita tambahkan referensi ke file `.css` eksternal kita tepat setelah tag `<title>`:<br>
	`<link rel="stylesheet" type="text/css" href="style.css" />`
	
- __Inline CSS:__<br>
*Inline CSS* digunakan untuk menata elemen HTML tertentu. Untuk *sytle CSS* ini, kita hanya perlu menambahkan *style attribute* ke setiap tag HTML, tanpa menggunakan *selector*.
Jenis CSS ini sangat tidak disarankan, karena setiap tag HTML perlu ditata secara individual. Mengelola situs web kita mungkin menjadi terlalu sulit jika kita hanya menggunakan *Inline CSS*.
Namun, *Inline CSS* dalam HTML dapat berguna dalam beberapa situasi. Misalnya, dalam kasus di mana kita tidak memiliki akses ke file CSS atau perlu menerapkan gaya untuk satu elemen saja.<br>
Berikut merupakan contoh *inline CSS* ke tag `<p>` dan `<h1>`:<br>
	```html
	<!DOCTYPE html>
	<html>
		<body style="background-color:black;">

			<h1 style="color:white;padding:30px;">PBP Tutorials</h1>
			<p style="color:white;">Something usefull here.</p>

		</body>
	</html>
	```

### Jelaskan tag HTML5 yang kamu ketahui.

Berikut merupakan tag dalam HTML5 yang sering dipakai
1. __CSS dan JS__ <br>
	Untuk melampirkan *file* css dan javascript sebagai *design* dan agar website terlihat menarik<br>
	```html
	<link rel="stylesheet" href="style.css" />
	<script src="script.js"></script>
	```
2. __*Semantics*__<br>
	Di HTML5 kita memiliki struktur semantik seperti `<header>`, `<footer>`, dan `<nav>` untuk contoh kode seperti ini.<br>
	```html
	<header>
		...
	</header>
	<nav>
		<ul>...</ul>
	</nav>
	<footer>
		...
	</footer>
	```
3. __*Article* dan *Section*__<br>
	```html
	<section>
	....
	</section>
	```
	*section tag* digunakan untuk mendefinisikan elemen html seperti header dan footer dan lainnya.<br>
	```html
	<article>
	...
	</article>
	```
	*article tag* digunakan untuk mendefinisikan konten independen tertentu<br>
4. __*Input types, attributes and forms*__<br>
	*input type* dan *attributes* baru telah diperkenalkan di HTML 5<br>
	```html
	<form>
		<input name="name" required placeholder="Your name" pattern="[A-z]{7}" />
	 
		<input type="email" name="email" required placeholder="email@inwebson.com"/>
	 
		<input type="url" name="url" placeholder="Homepage URL"/>
	 
		<input type="number" name="age" min="18" max="99" />
		
	<textarea name="desc" placeholder="Describe yourself here..."></textarea>
	  
	   <input type="submit" value="Submit" />
	</form>
	```
5. __*HTML5 editable content*__ <br>
	HTML5 memiliki atribut baru, sekarang kita dapat mengedit konten dengan menambahkan atribut *contenteditable* ke dalamnya.<br>
	```html
	<div contenteditable="true">
		content for editing
	</div>
	```
6.  __*Local Storage*__<br>
	Dengan fungsi ini, pengguna dapat mengakses data secara lokal dalam browser web. Sebelum pengguna HTML5 menyimpan data di cookie dengan setiap permintaan server.<br>
	```html
	<script>
		localStorage.variableName = "value";
		alert(localStorage.variableName);
		localStorage.removeItem("variableName");
		alert(localStorage.variableName);
	</script>
	```

### Jelaskan tipe-tipe CSS selector yang kamu ketahui.

*CSS selectors* digunakan untuk memilih konten yang ingin diberikan *style*. Selector adalah bagian dari *CSS rule set*. 
Selektor CSS memilih elemen HTML sesuai dengan *id, class, type, attribute etc*.

Ada beberapa jenis *CSS selectors*. di antaranya adalah:<br>
1. __*CSS Element Selector*__<br>
Selektor elemen memilih elemen HTML berdasarkan nama.<br>
2. __*CSS Id Selector*__<br>
Selector id memilih atribut id dari elemen HTML untuk memilih elemen tertentu. Id selalu unik di dalam halaman sehingga dipilih untuk memilih satu elemen unik. Itu ditulis dengan karakter hash (#), diikuti oleh id elemen.
3. __*CSS Class Selector*__<br>
Selektor kelas memilih elemen HTML dengan atribut kelas tertentu. Digunakan dengan karakter titik. (simbol titik penuh) diikuti dengan nama kelas.<br>
4. __*CSS Universal Selector*__<br>
Selektor universal digunakan sebagai karakter wildcard. Ini memilih semua elemen pada halaman.<br>
5. __*CSS Group Selector*__<br>
*Grouping selector* digunakan untuk memilih semua elemen dengan definisi *style* yang sama. *Grouping selector* digunakan untuk meminimalkan kode. Koma digunakan untuk memisahkan setiap selektor dalam pengelompokan.<br>

### Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.

1. __Kustomisasi templat HTML yang telah dibuat pada Tugas 4 dengan menggunakan CSS atau CSS framework (seperti Bootstrap, Tailwind, Bulma) dengan ketentuan sebagai berikut:__<br>
	Untuk semua template dari setiap halaman, saya memberikan tag <head> untuk mengambil css dari bootstrap, Misal dalam halaman login<br>
	```html
	<head>
		<meta charset="utf-8"> 													// untuk menerjemahkan karakter di dalam HTML sebagai UTF-8
		<meta name="viewport" content="width=device-width, initial-scale=1">	// agar page tersebut responsive dan dapat di lihat di semua device
		<title>Login</title>													// field judul
		<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
	</head>
	```
	Setelah itu, saya juga mengambil file JS untuk membuat konten web yang dinamis dan interaktif seperti aplikasi dan browser. Dengan cara<br>
	```html
	<body>
		<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
		...
	</body>
	```
	Selanjutnya dalam setiap halaman saya juga membuat navbar dengan button tertentu. Dalam setiap bagian dari halaman tersebut saya juga menambahkan background image agar tampilan menjadi lebih menarik.<br>
	Lalu, dalam setiap page juga saya membuat container dengan style `align-items: center;` agar setiap item ditampilkan di tengah. <br>
	Dalam setiap page saya juga memberikan attribute margin atau padding untuk menyesuaikan item tersebut agar menarik dilihat user. <br>
	Tentu dalam setiap form harus diberikan `{% csrf_token %}` untuk memberikan proteksi data. <br>
	Dalam page todolist, saya menampilkan form sebagai cards dan membuat fitur berwarna hijau ketika task tersebut sudah selesai dan berwarna merah ketika task tersebut belum selesai. <br>
	Pada bagian bonus, saya membuat efek ketika melakukan hover pada cards di halaman utama todolist dengan cara menambahkan *style* berikut ini.<br>
	```html
	<style>
		.card:hover {
			transform: scale(1.02);
		  }
		...
	</style>
	```
	
2. __Membuat keempat halaman yang dikustomisasi menjadi responsive.__<br>
	*Responsive web design* adalah sebuah metode atau pendekatan sistem web desain yang bertujuan memberikan pengalaman berselancar yang optimal dalam berbagai perangkat, baik mobile maupun komputer.<br>
	Untuk mengaplikasikan hal tersebut saya menambahkan potongan kode berikut ini dalam tag `<head>`<br>
	`<meta name="viewport" content="width=device-width, initial-scale=1">`


## Credits

Template ini dibuat berdasarkan [PBP Ganjil 2021](https://gitlab.com/PBP-2021/pbp-lab) yang ditulis oleh Tim Pengajar Pemrograman Berbasis Platform 2021 ([@prakashdivyy](https://gitlab.com/prakashdivyy)) dan [django-template-heroku](https://github.com/laymonage/django-template-heroku) yang ditulis oleh [@laymonage, et al.](https://github.com/laymonage). Template ini dirancang sedemikian rupa sehingga mahasiswa dapat menjadikan template ini sebagai awalan serta acuan dalam mengerjakan tugas maupun dalam berkarya.