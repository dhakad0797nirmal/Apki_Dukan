$(()=>{
    //js for modal and selecting address start
  var address_id={}
  var current_html=null
  var name_error=true
  var pin_error=true
  var city_error=true
  var address_error=false
  var number_error=true
  var name=''
  var city=''
  var pin=''
  var address=''
  var number=''
  var current_selected=null
  var previos_selected=null
  var current_state=null
  for(var i=0;i<$('.w3-card').length;i++){
    address_id[$('.w3-card')[i].id]=0
  }

  var check=Object.getOwnPropertyNames(address_id)
  if(check.length==0)
  {
    $('#placeorder').hide()
  }
 
  $('#exampleModalLong').on('hidden.bs.modal',function(ev){
      
    if(current_html!=null){
      $('#pricing').html(current_html)
      
      recreate()
      for(var i=0;i<$('.w3-card').length;i++)
    {
     $('#'+ $('.w3-card')[i].getAttribute('id')).removeClass('selected')
    }
    }
    if(current_selected!=null)
      {
        $('#'+current_selected).removeClass('selected')
        previos_selected.removeClass('selected')
        current_selected=null
        previos_selected=null
      }
   
  })
  function recreate(){
    if(check.length==0)
  {
    $('#placeorder').hide()
  }
  current_state="select_address"
    var formate=/^[0-9]+$/;
    $('#addressadder').click(function(ev){
      current_state="form_address"
      $('#placeorder').show()
    $('#exampleModalLongTitle').html("Enter address")
    current_html=$('#pricing').html()
    $('#pricing').html('<form  id="formsubmit"><div class="form-row"><div class="form-group col-md-6"><label for="inputEmail4">Name</label><input type="text" class="form-control" required id="name" placeholder="enter name " pattern="[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]"></div></div><div class="form-group"><label for="inputAddress">Address</label><input type="text" class="form-control" id="address" placeholder="1234 Main St"></div><div class="form-group"><label for="inputAddress2">Mobile no.</label><input type="text" class="form-control" id="number" placeholder="10 digit phone number"></div><div class="form-row"><div class="form-group col-md-6"><label for="inputCity">City</label><input type="text" class="form-control" id="city" pattern="[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]"></div><div class="form-group col-md-2"><label for="inputZip">pin</label><input type="text" class="form-control" id="pin" pattern="[1234567890]"></div></div></form>')//here we have to push code for form  
    $('#name').keyup(function(ev){
      var val=$('#name').val()
      val=val.replace(/[0-9]/g,'')
      $('#name').val(val)
      
        
    })
    $('#city').keyup(function(ev){
      var val=$('#city').val()
      val=val.replace(/[0-9]/g,'')
      $('#city').val(val)
      
        
    })
    $('#pin').keyup(function(ev){
      
      var val=$('#pin').val()
      val=val.replace(/\D/g,'')
      $('#pin').val(val)
     
        
    })
    $('#number').keyup(function(ev){
      var val=$('#number').val()
      val=val.replace(/\D/g,'')
      $('#number').val(val)
    
        
     
    })

  })
   //here code for choosing the address
  
  $('.w3-card').click(function(ev){
    for(var i=0;i<$('.w3-card').length;i++)
    {
     $('#'+ $('.w3-card')[i].getAttribute('id')).removeClass('selected')
    }
    current_selected=$(ev.currentTarget).attr('id')

    if (current_selected in address_id==false)
    {
      window.location.reload()
    }
    if(previos_selected==null)
    $('#'+current_selected).addClass('selected')
    else{
      previos_selected.removeClass('selected')
      $('#'+current_selected).addClass('selected')
    }
    previos_selected=$('#'+current_selected)
  })
  }

  recreate();



  $('#placeorder').click(function(ev){
    
     var action=null
     if(current_state=="form_address"){
      var val=$('#name').val()
      name=val.replace(/[0-9]/g,'')
      $('#name').val(val)
       val=$('#city').val()
      city=val.replace(/[0-9]/g,'')
      $('#city').val(val)
       val=$('#pin').val()
      pin=val.replace(/\D/g,'')
      $('#pin').val(val)
       val=$('#number').val()
      number=val.replace(/\D/g,'')
      $('#number').val(val)
      var address=$('#address').val()
      if(name.length<=3 || name.length>=20)
      {
        alert("name only contains characters and should be of range 3 to 20 in length")
        return
      }
      if(city.length<=3 || city.length>=20)
      {
        alert("city only  contains characters and should be of range 3 to 20 in length")
        return
      }
      if(number.length!=10 )
      {
        alert("mobile number only contains digits and should be of 10 digits")
        return
      }
      if(pin.length!=6 )
      {
        alert("pin only contain digit and should be of 6 digits")
        return
      }
      if(address.length<=3 || address.length>=100){
        alert("address length should be in between 3 to 100 characters")
        return
      }
      $.ajax({
        url:'/save_address',
        type:'POST',
        data:{action:"set_and_update",name:name,number:number,address:address,pin:pin,city:city},
        success:function(response){
          if(response=="success"){
          alert("order is confirm successfully")
          window.location.replace('/user_account_orders')
          }
          else if(response=="failed")
          {
            window.location.replace('/login')
          }
          else
        {
          window.location.reload()
        }
        },
        error:function(err){
          window.location.reload()
        }
      })
     }
     else if(current_state=="select_address"){  
       //check lgana h dictionary m ek hi element selected ho
       //check lhgana ki id main dictionary se match honi chahiye
       //server p check krna h ki id address table m lie krti h ki nhi
       if(current_selected==null){
         alert("please select addresss")
         for(var i=0;i<$('.w3-card').length;i++)
         {
          $('#'+ $('.w3-card')[i].getAttribute('id')).removeClass('selected')
         }
         return
         }
       if (current_selected in address_id==false){
         current_selected=null
         previos_selected=null
        {
         $('#'+ $('.w3-card')[i].getAttribute('id')).removeClass('selected')
        }
         window.location.reload()
       }
       else{
         $.ajax({
          url:'/save_address',
        type:'POST',
        data:{action:"select_address",a_id:current_selected},
        success:function(response){
          if(response=="success"){
          alert("congratulations!! order is confirm successfully")
          window.location.replace('/user_account_orders')
          }
          else if(response=="failed")
          {
            window.location.replace('/login')
          }
          else{
            window.location.reload()
          }
        },
        error:function(err){
          window.location.reload()
        }
         })
       }
       
     }
     
   })



    //js for modal and selecting addess end
    $('#alertkro').hide()
    $('#showalert').hide()
    var product_total_amt = document.getElementById('product_total_amt');
    var shipping_charge = document.getElementById('shipping_charge');
    var total_cart_amt = document.getElementById('total_cart_amt');
    var len=$('.list').length
    var dict={}
    totals_price=0;
    for(var i=0;i<len;i++){
        
        var id=String($('.list')[i].getAttribute('id'))
        var size=parseInt($('#'+String(id)+'textbox').val())
        var lst=[]
        lst.push(size)
        lst.push(parseInt($('#'+String(id) +"itemval").html()))
        dict[id]=lst
        totals_price+=parseInt($('#'+String(id) +"itemval").html())*size
        $('#'+String(id)+'itemval').html(parseInt($('#'+String(id) +"itemval").html())*size)
    }
    console.log(dict)
    if(totals_price==0){
        $('#alertkro').text("cart is empty")
        $('#alertkro').show(500)
        $('#checkout').hide()
    }
    if(totals_price<500){
        $('#checkout').hide()
        $('#alertkro').text("shop for atleast 500 ")
        $('#alertkro').show(500)
    }
    product_total_amt.innerHTML=totals_price
    total_cart_amt.innerHTML=totals_price
    $('.remove').click(function(ev){
        var id=ev.currentTarget.getAttribute('id')
        id=parseInt(id)
        totals_price=totals_price-(parseInt(dict[parseInt(id)][0])*parseInt(dict[parseInt(id)][1]))
        delete dict[id]
        $("#"+id).hide(500)
        $('#'+id).html("")
        product_total_amt.innerHTML=totals_price
        total_cart_amt.innerHTML=totals_price
        if(totals_price==0){
        $('#alertkro').text("cart is empty")
        $('#alertkro').show(500)
        $('#checkout').hide()
        }
        if(totals_price<500){
        $('#alertkro').text("shop for atleast 500")
        $('#alertkro').show(500)
        $('#checkout').hide() 
        }
        if(totals_price>500){
            $('#alertkro').hide()
            $('#checkout').show() 
        }
        $.ajax({
            url:'/remove_item',
            data:{p_id:id},
            type:'POST',
            success:function(response){
                if (response=="login")
                {
                    window.location.replace('/login')
                }
                if(response=="success"){
                    
                }
                
            }
        })

    
    })
    $('.plus').click(function(ev){
        //this is minus
        var id=ev.currentTarget.getAttribute('id')
        var p_id=parseInt(id)
        dict[p_id][0]+=1
        $('#'+p_id+"textbox").val(dict[p_id][0])
        $('#'+p_id+"itemval").html(dict[p_id][0]*dict[p_id][1])
        totals_price=totals_price+dict[p_id][1]
        product_total_amt.innerHTML=totals_price
        total_cart_amt.innerHTML=totals_price
        if(totals_price==0){
        $('#alertkro').text("cart is empty")
        $('#alertkro').show(500)
        $('#checkout').hide()
        }
        if(totals_price<500){
        $('#alertkro').text("shop for atleast 500")
        $('#alertkro').show(500)
        $('#checkout').hide() 
        }
        if(totals_price>500){
            $('#alertkro').hide()
            $('#checkout').show() 
        }
    })
    $('.minus').click(function(ev){
        //this is minus
        var id=ev.currentTarget.getAttribute('id')
        var p_id=parseInt(id)
        if (dict[p_id][0]==0){
            alert("Negative quantity not allowed")
            return
        }
        dict[p_id][0]-=1
        $('#'+p_id+"textbox").val(dict[p_id][0])
        $('#'+p_id+"itemval").html(dict[p_id][0]*dict[p_id][1])
        totals_price=totals_price-dict[p_id][1]
        product_total_amt.innerHTML=totals_price
        total_cart_amt.innerHTML=totals_price
        if(totals_price==0){
        $('#alertkro').text("cart is empty")
        $('#alertkro').show(500)
        $('#checkout').hide()
        }
        if(totals_price<500){
        $('#alertkro').text("shop for atleast 500")
        $('#alertkro').show(500)
        $('#checkout').hide() 
        }
        if(totals_price>500){
            $('#alertkro').hide()
            $('#checkout').show() 
        }
    });
    $('#checkout').click(function(ev){
        dict2=JSON.stringify(dict)
        if(totals_price==0 || totals_price<0)
        {
            $('#showalert').text("Not allowed to procced with empty cart")
            $('#showalert').show(500)
            $('#showalert').hide(1000)
            
            return
        }
        if(totals_price<500){
            $('#showalert').text("please make order of atleast 500rs")
            $('#showalert').show(500)
            $('#showalert').hide(1000)
            return
        }
        $.ajax({
            url:'/save_cart',
            data:{dict:dict2},
            type:'POST',
            success:function(response){
                //window.location.replace('/checkout/order_summary')
            }
        })
        
    })
    
})
