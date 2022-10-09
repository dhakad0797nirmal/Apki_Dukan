
    $(()=>{
        $('.quantity').click(function(ev){

            var p_id=String($(this).attr('id'))
            //send data to ajax for valiadtion
            var p_size=1;
            $.ajax({
                url : 'http://127.0.0.1:5000/get_cart_detail',
                type : 'POST',
                data : {action:"add one", p_id:p_id,p_size:p_size},
                success : function(response){
                   if (response=="do login")
                   {
                       window.location.href="http://127.0.0.1:5000/login"
                   }
                   else if(response=="success"){
                       $("#"+p_id).html('<div class="alert alert-success" role="alert">the deal is addedd check it out!</div>')
                       $("#"+p_id).hide()
                       $("#"+p_id).show(500)
                       setTimeout(function(){
                        $("#"+p_id).fadeOut('slow')
                       },1000)
                       $("#buy"+String(p_id)).html('<a href="/bag"><button type="button"   class="btn btn-success">buy now</button></a>')//change here
                   }
                   else{
                       location.reload();
                   }
                }
                });
        });
    });