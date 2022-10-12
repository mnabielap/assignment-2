# Proyek Django PBP

Pemrograman Berbasis Platform (CSGE602022) - diselenggarakan oleh Fakultas Ilmu Komputer Universitas Indonesia, Semester Ganjil 2022/2023

Muhammad Nabiel Andityo Purnomo - 2106750465

## Tugas 6 - Javascript dan AJAX

### Link to Deployed App

[LINK HEROKU](https://assignment-pbp-nabiel.herokuapp.com/todolist/)

### Jelaskan perbedaan antara *asynchronous programming* dengan *synchronous programming*

*Asynchronous programming* memungkinkan lebih banyak hal untuk dilakukan pada saat yang sama dan biasanya digunakan untuk meningkatkan 
pengalaman pengguna dengan menyediakan *quick-loading flow* yang mudah. *Synchronous programming* paling baik digunakan dalam *reactive systems*. 
Meskipun lebih mudah bagi *developer* untuk membuat kode dan dikenali oleh setiap bahasa pemrograman, sinkronisasi membutuhkan banyak sumber 
daya dan dapat memperlambat segalanya.

Dengan kata lain, *Asynchronous* adalah *multi-thread*, yang berarti operasi atau program dapat berjalan secara paralel. *Synchronous* adalah *single-thread*, 
jadi hanya satu operasi atau program yang akan berjalan pada satu waktu. *Asynchronous* tidak memblokir, yang berarti akan mengirim banyak permintaan ke server. 
*Synchronous* memblokir, itu hanya akan mengirim server satu permintaan pada satu waktu dan akan menunggu permintaan itu dijawab oleh server.

### Dalam penerapan JavaScript dan AJAX, terdapat penerapan paradigma *Event-Driven Programming*. Jelaskan maksud dari paradigma tersebut dan sebutkan salah satu contoh penerapannya pada tugas ini.

*Event-driven programming* adalah paradigma pemrograman di mana eksekusi program ditentukan oleh *event user* terbaru seperti (*mouse clicks*, penekanan tombol), 
*sensor output*, atau *message passing* yang lewat dari program lain. Dalam program ini terdapat event listener klik yang mendengarkan tombol dengan id tertentu untuk 
melakukan fungsi tertentu. *Event-driven programming* adalah paradigma dominan yang digunakan dalam GUI dan aplikasi lain (misalnya, aplikasi 
web JavaScript) yang berpusat pada melakukan tindakan tertentu dalam menanggapi masukan pengguna. Misalnya dalam penerapan tugas ini, yaitu *button* "Create Task".

### Jelaskan penerapan *asynchronous programming* pada AJAX.
1. Tambahkan `<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>` ke *header html*.
2. Tambahkan tag `<script>` di dalam *html body* Anda.
3. Tulis sintaks ajax JQuery di dalam skrip Anda, seperti `$.ajax()` ke `POST`, `DELETE`, dll.
4. Ajax akan mendengarkan *event listener* yang Anda tulis dalam skrip untuk melakukan tindakan yang Anda inginkan.
5. Tindakan dan respon/data tersebut akan diproses secara *asynchronous* di server.
6. Sehingga data akan ditampilkan di halaman tanpa perlu di-*refresh*.

### Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.

#### AJAX GET

1. __Buatlah view baru yang mengembalikan seluruh data task dalam bentuk JSON.__<br>
	Dapat dilakukan dengan menambahkan fungsi berikut di `views.py`:<br>
	```python
	@login_required(login_url='/todolist/login/')
	def show_todolist_json(request):
		data = Task.objects.filter(user=request.user).order_by('id')
		return HttpResponse(serializers.serialize("json", data), content_type="application/json")
	```
2. __Buatlah path `/todolist/json` yang mengarah ke view yang baru kamu buat.__<br>
	Dapat dilakukan dengan menambahkan berikut di `urlpatterns` yang mengarah ke fungsi `show_todolist_json`:<br>
	```python
	urlpatterns = [
		...
		path('json/', show_todolist_json, name='show_todolist_json'),
	]
	```
3. __Lakukan pengambilan task menggunakan AJAX GET.__<br>
	Pada step ini, saya menggunakan AJAX getJSON untuk mengambil data json dari database. Lalu saya menggunakan `$.each(json, function (index, val) {...}`
	untuk menampilkan setiap card yang ada dengan implementasi lebih lanjut dalam `todolist.html` bagian `displayCards` dalam `<script>`
	
#### AJAX POST

1. __Buatlah sebuah tombol `Add Task` yang membuka sebuah modal dengan form untuk menambahkan task.__<br>
	Berikut adalah implementasi step ini dengan navbar, potongan code ini saya tambahkan ke dalam body html<br>
	```html
	<nav class="navbar px-3 mb-3" style="background-image: url('https://img.freepik.com/free-vector/white-gray-geometric-pattern-background-vector_53876-136510.jpg?w=1380&t=st=1664620923~exp=1664621523~hmac=9a3ab8d25bc3d7a311af1708b5c510a1bbd937612ff69604ac8752e84fb18f57');">
		<span class="navbar-text mb-0 h5 text-black">Signed in as {{user.username}}</span>
		<a class="navbar-brand" href="https://id.wikipedia.org/wiki/Fakultas_Ilmu_Komputer_Universitas_Indonesia">
			<img src="https://upload.wikimedia.org/wikipedia/id/thumb/c/c3/Makara_of_Fasilkom_UI.svg/1200px-Makara_of_Fasilkom_UI.svg.png" width="120" height="45" alt="">
		</a>
		<div class="btn-group" role="group">
			<button class="btn btn-primary me-3 navbar-btn" type="button" name="create-task" id="modalButton" style="border-radius: 5px;">
				Create Task
			</button>
			<form action="{% url 'todolist:logout' %}">
				{% csrf_token %}
				<button type="submit" class="btn btn-outline-danger navbar-btn">Logout</button>
			</form>
		</div>
	</nav>
	```
2. __Buatlah view baru untuk menambahkan task baru ke dalam database.__<br>
	Pada step ini, saya menambahkan potongan code berikut ke dalam `views.py`<br>
	```python
	@login_required(login_url='/todolist/login/')
	def create_task_ajax(request):

		if request.method == "POST":
			title = request.POST['title']
			description = request.POST['description']
			new_item = Task.objects.create(user=request.user, title=title, description=description)
			return JsonResponse({'error': False, 'msg':'Successful'})
		
		return redirect('todolist:show_todolist')
	```
3. __Buatlah path `/todolist/add` yang mengarah ke view yang baru kamu buat.__<br>
	Dapat dilakukan dengan menambahkan berikut di `urlpatterns` yang mengarah ke fungsi `create_task_ajax`:<br>
	```python
	urlpatterns = [
		...
		path('add/', create_task_ajax, name='create_task_ajax'),
	]
	```
4. __Hubungkan form yang telah kamu buat di dalam modal kamu ke path `/todolist/add`__<br>
	```html
	<div class="modal fade" id="formModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title" id="exampleModalLabel">Create Task</h3>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<form id="createTaskForm">
					{% csrf_token %}
					<div class="modal-body">
						<fieldset>
							<input class="form-control mb-3" type="text" placeholder="Task Title" name="title">
							<textarea class="form-control mb-3" rows="3" placeholder="Description"
								name="description"></textarea>
						</fieldset>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
						<button type="submit" class="btn btn-primary btnClick">Submit</button>
					</div>
				</form>

			</div>
		</div>
	</div>
	```
5. __Tutup modal setelah penambahan task telah berhasil dilakukan.__<br>
	Implementasi hal ini ada di script, `$("#formModal").modal('hide');`<br>
6. __Lakukan refresh pada halaman utama secara asinkronus untuk menampilkan list terbaru tanpa reload seluruh page.__<br>
	Dapat dilakukan dengan 
	```
	$(document).ready(function)
	
	The ready() method can only be used on the current document, so no selector is required:
	$(function)

	Parameter	Description
	function	Required. Specifies the function to run after the document is loaded
	```
	yang berada di dalam tag `script`, dimana `function` tersebut adalah *function* yang akan di *run* ketika *document loaded*.
	Didalamnya saya berikan pemanggilan fungsi `displayCards` untuk menampilkan *card* ketika `getJSON` sukses dipanggil.
	
## Credits

Template ini dibuat berdasarkan [PBP Ganjil 2021](https://gitlab.com/PBP-2021/pbp-lab) yang ditulis oleh Tim Pengajar Pemrograman Berbasis Platform 2021 ([@prakashdivyy](https://gitlab.com/prakashdivyy)) dan [django-template-heroku](https://github.com/laymonage/django-template-heroku) yang ditulis oleh [@laymonage, et al.](https://github.com/laymonage). Template ini dirancang sedemikian rupa sehingga mahasiswa dapat menjadikan template ini sebagai awalan serta acuan dalam mengerjakan tugas maupun dalam berkarya.