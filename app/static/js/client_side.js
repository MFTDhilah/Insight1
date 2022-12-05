$(document).ready(function(){
  
  // -[Animasi Scroll]---------------------------
  
  $(".navbar a, footer a[href='#halamanku']").on('click', function(event) {
    if (this.hash !== "") {
      event.preventDefault();
      var hash = this.hash;
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 900, function(){
        window.location.hash = hash;
      });
    } 
  });
  
  $(window).scroll(function() {
    $(".slideanim").each(function(){
      var pos = $(this).offset().top;
      var winTop = $(window).scrollTop();
        if (pos < winTop + 600) {
          $(this).addClass("slide");
        }
    });
  });

  
  // -[Prediksi Model]---------------------------
  
  // Fungsi untuk memanggil API ketika tombol prediksi ditekan
  $("#prediksi_submit").click(function(e) {
    e.preventDefault();
	
	// Set data pengukuran bunga iris dari input pengguna
  var input_gre = $("#nilai_gre").val(); 
	var input_toefl  = $("#nilai_toefl").val(); 
	var input_rating = $("#nilai_rating").val(); 
	var input_sop  = $("#nilai_sop").val(); 
  var input_lor  = $("#nilai_lor").val(); 
  var input_cgpa  = $("#nilai_cgpa").val(); 
  var input_research = $("#nilai_research").val(); 
	// Panggil API dengan timeout 1 detik (1000 ms)
    setTimeout(function() {
	  try {
			$.ajax({
			  url  : "/api/deteksi",
			  type : "POST",
			  data : {"gre" : input_gre,
					  "toefl"  : input_toefl,
					  "rating" : input_rating,
					  "sop"  : input_sop,
            "lor" : input_lor,
					  "cgpa"  : input_cgpa,
            "research" : input_research,
			         },
			  success:function(res){
				// Ambil hasil prediksi spesies dan path gambar spesies dari API
				res_data_prediksi     = res['prediksi']
				res_gambar_prediksi   = res['gambar_prediksi']
        res_kategori_prediksi = res['kategori']
				
				// Tampilkan hasil prediksi ke halaman web
			    generate_prediksi(res_data_prediksi, res_gambar_prediksi, res_kategori_prediksi); 
			  }
			});
		}
		catch(e) {
			// Jika gagal memanggil API, tampilkan error di console
			console.log("Gagal !");
			console.log(e);
		} 
    }, 1000)
    
  })
    
  // Fungsi untuk menampilkan hasil prediksi model
  function generate_prediksi(data_prediksi, gambar_prediksi, kategori_prediksi) {
    var str="";
    str += "<h3>Hasil Prediksi </h3>";
    str += "<br>";
    str += "<img src='" + gambar_prediksi + "' width=\"700\" height=\"300\"></img>"
    str += "<h3>" + data_prediksi + "</h3>";
    str += "<h3>" + kategori_prediksi + "</h3>";
    $("#hasil_prediksi").html(str);
  }  
  
})
  
