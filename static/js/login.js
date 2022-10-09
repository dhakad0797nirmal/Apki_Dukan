
    
function logvalid()
{
    var pss=document.getElementById("uid").value; 
    if(isNaN(pss))//if mobile no has alphabets.
        {       
                document.getElementById('spl').innerHTML="*Mobile number can only contains digits.";
                return false;
        }
        if(pss.length != 10)//if mobile no. length is not 10.
        {
                document.getElementById('spl').innerHTML="*Mobile number should be of 10 digits.";
                return false;
        }
        $.ajax({
          url:"/auth_login",
          data:{u_id:pss},
          type:'POST',
          success:function(response){
            if(response=="authenticated"){
              location.href='/'
            }
            else if(response=="incorrect"){
              document.getElementById('spl').innerHTML="*Incorrect mobile number!!";
              return false;
            }
          }
        })
      
        
}

function info()
{
        var name=document.getElementById("uname").value;
        
        var pss=document.getElementById("umob1").value;
        var Cpss=document.getElementById("umob2").value;
        
        if(!isNaN(name))//if name contains numbers
        {
                //alert("Name can only contains alphabets.");
                document.getElementById('sp1').innerHTML="*Name can only contains alphabets.";
                return false;
        }
        if(name.length<3)//if length of name is less than 3.
        {       
                document.getElementById('sp1').innerHTML="*Name should have atleast 5 alphabets.";
                return false;
        }
        
        if(name.length >20)//if length of name is less than 3.
        {
                document.getElementById('sp1').innerHTML="*it should not conatian more than  20 alphabets.";
                return false;
        }
        if(isNaN(pss))//if mobile no has alphabets.
        {       
                document.getElementById('sp1').innerHTML="";
                document.getElementById('sp2').innerHTML="*Mobile number can only contains digits.";
                return false;
        }
        if(pss.length != 10)//if mobile no. length is not 10.
        {
            document.getElementById('sp1').innerHTML="";
                document.getElementById('sp2').innerHTML="*Mobile number should be of 10 digits.";
                return false;
        }
        
        if(pss != Cpss)//password and conf. password do not match.
        {
                document.getElementById('sp1').innerHTML="";
                document.getElementById('sp2').innerHTML="";
                document.getElementById('sp3').innerHTML="*Both Mobile number must be same.";
                return false;
        }
        $.ajax({
          url:"/signup",
          data:{u_id:pss,u_name:name},
          type:'POST',
          success:function(response){
            if(response=="authenticated"){
              location.href='/'
            }
            else if(response=="existing user"){
              document.getElementById('sp1').innerHTML="*existing user please try another number!!";
              return false;
            }
          }
        })
}