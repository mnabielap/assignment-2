# Proyek Django PBP

Pemrograman Berbasis Platform (CSGE602022) - diselenggarakan oleh Fakultas Ilmu Komputer Universitas Indonesia, Semester Ganjil 2022/2023

Muhammad Nabiel Andityo Purnomo - 2106750465

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
data-data yang dimiliki pengguna yang sedang menggunakan website kita dalam pengisian form yang mengatasnamakan user target.

### Apakah kita dapat membuat elemen `<form>` secara manual (tanpa menggunakan generator seperti `{{ form.as_table }}`)? Jelaskan secara gambaran besar bagaimana cara membuat `<form>` secara manual.

Kita dapat membuat form secara manual dengan cara berikut ini. Pertama-tama, kita diharuskan untuk menyediakan variabel untuk
menyimpan data yang diberikan di form. Dalam tempate HTML kita dapat memanfaatkan tag `<input>`. Tentu saja, tidak lupa untuk
memberikan tag `{% csrf_token %}` dan juga `<form>` untuk menghidari *attacker*. Selanjutnya, dalam file `views.py`, kita dapat
membuat request dari form yang telah diisi user dengan potongan code `request.POST.get(data)` yang disimpan kedalam variabel 
di *function* `create_task`. Setelah itu, dibawahnya dapat ditambahkan perintah `Task.objects.create` untuk membuat object dari
task. Dan tentunya, di simpan dengan menggunakan `task.save()`.

### Jelaskan proses alur data dari submisi yang dilakukan oleh pengguna melalui HTML form, penyimpanan data pada database, hingga munculnya data yang telah disimpan pada template HTML.

Proses alur data yang terjadi adalah pertama-tama user mengisi dan mengirimkan data mereka melalui form. Lalu, ketika
CSRF token sesuai, maka server tersebut akan mengolah dan menerima data dari user dalam hal ini `views.py` akan 
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
		date = models.DateField(auto_now=True)				# alokasi untuk merepresentasikan tanggal dibuatnya task
		title = models.CharField(max_length=250)			# alokasi untuk menampung string pendek dari judul
		description = models.TextField()					# alokasi untuk menampung string panjang dari deskripsi
		is_finished = models.BooleanField(default=False)	# alokasi untuk mengampung status task (boolean) merupakan bonus
	```
	
4. Mengimplementasikan form registrasi, login, dan logout agar pengguna dapat menggunakan `todolist` dengan baik.

	Untuk form registrasi, saya menggunakan `UserCreationForm` dalam `views.py` untuk membuat form registrasi. Selanjutnya untuk 
	bagian login, saya lakukan di dalam fungsi `views.py` dengan `authenticate` yang akan melakukan validasi berdasarkan data yang telah di register,
	ketika user tersebut sudah melakukan registrasi dan password sesuai maka login sukses dan langsung ditujukan ke halaman utama `todolist`. 
	Lalu, untuk bagian `logout` saya melakukan delete cookie yang dibuat saat pada `login` dan redirect kembali ke halaman `login`
	
5. Membuat halaman utama `todolist` yang memuat username pengguna, tombol `Tambah Task Baru`, tombol `logout`, serta tabel berisi tanggal pembuatan task, judul task, dan deskripsi task.

	Hal ini saya lakukan dengan membuat template terlebih dahulu untuk halaman utama todolist dengan nama
	`todolist.html` yang berisi *button*-*button* untuk melakukan aksi penambahan task, update task, dan
	delete task.
	
	*Button*-*button* tersebut akan mengarahkan url mana yang akan dituju ketika user mengklik tombol tersebut.
	Misalnya ketika user mengklik `Create Task` maka akan otomatis ke halaman `create_task` untuk membuat 
	task, begitu juga untuk tombol `update-task` dan `delete-task`. Dimana `update-task` akan mengarahkan ke url
	`update-task/id` yang akan *invert* is_finished dari task lalu kembali ke page `todolist` utama. Jika tombol 
	`delete-task` juga akan mengarahkan ke url `delete-task/id` dan menghapus object dari task tersebut.
	
6. Membuat halaman form untuk pembuatan task. Data yang perlu dimasukkan pengguna hanyalah judul task dan deskripsi task.

	Pada step ini saya menggunakan `ModelForm` untuk memetakan model Task berdasarkan `models.py` 
	yang merupakan data yang akan diisi user ketika membuat task baru. Dalam file `forms.py`
	saya membuat fields yang berisi `title` dan `description` yang akan diminta ketika mengisi form `create-task`. 
	Setelah mengisi form, objek task setiap user nantinya akan ditampilkan pada halaman utama
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
		path('', show_todolist, name='show_todolist'),	# berisi halaman utama yang memuat tabel task.
		path('register/', register, name='register'),	# berisi form registrasi akun.
		path('login/', login_user, name='login'),		# berisi form login
		path('logout/', logout_user, name='logout'),	# mekanisme logout
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

	Hal ini dapat diimplementasikan dengan cara user membuat akun melalui halaman registrasi. Setelah itu, login dan
	masuk ke halaman utama `todolist` untuk membuat tiga task dalam form `create-task` pada akun masing-masing dengan jumlah
	dua akun.


## Credits

Template ini dibuat berdasarkan [PBP Ganjil 2021](https://gitlab.com/PBP-2021/pbp-lab) yang ditulis oleh Tim Pengajar Pemrograman Berbasis Platform 2021 ([@prakashdivyy](https://gitlab.com/prakashdivyy)) dan [django-template-heroku](https://github.com/laymonage/django-template-heroku) yang ditulis oleh [@laymonage, et al.](https://github.com/laymonage). Template ini dirancang sedemikian rupa sehingga mahasiswa dapat menjadikan template ini sebagai awalan serta acuan dalam mengerjakan tugas maupun dalam berkarya.
