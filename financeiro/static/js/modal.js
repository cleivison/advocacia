/*create*/
jQuery(document).ready(function($){
	  $(".js-add-category").click(function () {
	    $.ajax({
	      url: '/add/categoria/',
	      type: 'get',
	      dataType: 'json',
	      beforeSend: function () {
	      	jQuery.noConflict(); 
	        $("#add-categoria-modal").modal("show");
	      },
	      success: function (data) {
	        $("#add-categoria-modal .modal-content").html(data.html_form);
	      }
	    });
	  });

	});


/*delete*/
jQuery(document).ready(function($){
	  $(".js-delete-conta").click(function () {
	    var btn = $(this);
	    $.ajax({
	      url: '/contas/pagar/deletar/'+btn.attr("id")+'/',
	      type: 'get',
	      dataType: 'json',
	      beforeSend: function () {
	      	jQuery.noConflict(); 
	        $("#delete-conta-modal").modal("show");
	      },
	      success: function (data) {
	        $("#delete-conta-modal .modal-content").html(data.html_form);
	      }
	    });
	  });

	});

    /*delete receber*/
    jQuery(document).ready(function($){
          $(".js-delete-conta-receber").click(function () {
            var btn = $(this);
            $.ajax({
              url: '/contas/receber/deletar/'+btn.attr("id")+'/',
              type: 'get',
              dataType: 'json',
              beforeSend: function () {
                jQuery.noConflict(); 
                $("#delete-conta-modal").modal("show");
              },
              success: function (data) {
                $("#delete-conta-modal .modal-content").html(data.html_form);
              }
            });
          });

        });