$(()=>{


    var status=$("#status").html().toLocaleLowerCase()
    var o_id=$("#order_id").html().replace(/^\D+/g,'');
    
    //$("#p_name").show()
    //alert($("#p_name_al").attr('class'))
    $("#p_name_al").hide();
    if( status=="pending" || status=="accepted" || status=="shipped"){
       
        $("#button_placer").html('<span >   <button style="position:relative; width:200px;"  type="button" id="reject" class="btn btn-danger btn-sm" data-toggle="tooltip" data-placement="top" title="click here to cancel the order">cancel order</button></span>')
        
        
        $("#reject").click(function(){
            $("#p_name_al").show(100)
            $("#p_name_al").html("<b>the item is being rejected</b>")
            update_o_status("cancelled",String(o_id))
        });
    }
    
  
    function update_o_status(status,o_id)
    {
        $.ajax({
            url:"/update_order_id_client",
            type:"POST",
            data:{o_id:o_id,o_status:status},
            success:function(response){
                $("#p_name_al").show(1000);
                $("#reject").hide()
                $("status").text("Cancelled")
            }
        });
    }

});