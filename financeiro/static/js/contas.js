/*esconde e mostra o input de parcelas quando selecionado a opção correta*/
	window.onload = function(){
	    document.getElementById('id_forma_pagamento').onchange = function() {
	        if(this.value == 'Cartão de credito' || this.value == 'Cheque')
	            document.getElementById('n_parcela').style.display = "block";
	        else if(this.value == 'á vista' || this.value == 'Boleto')
	            document.getElementById('n_parcela').style.display = "none";
	    };
	/*esconde e mostra o input das categorias das contas quando selecionado a opção correta*/
	    document.getElementById('id_conta_fixa').onchange = function() {
	        if(this.value == 2 )
	            document.getElementById('category_conta').style.display = "block";
	        else if(this.value == 3 )
	            document.getElementById('category_conta').style.display = "none";
	    };
	};
	
	/*mascaras dos campos input */
    jQuery.noConflict();
    jQuery(function($){
       $("#id_vencimento").mask("99/99/9999").datepicker({dateFormat: 'dd/mm/yyyy',autoClose:true});
    });
    jQuery(function($){
    /*mascara de dinheiro */
    $('#id_valor_total').priceFormat({
        prefix: 'R$ ',
        centsSeparator: ',',
        thousandsSeparator: '.'
                               }); 
    $('#id_valor_entrada').priceFormat({
        prefix: 'R$ ',
        centsSeparator: ',',
        thousandsSeparator: '.'
                               });    
    });


