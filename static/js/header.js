$(()=>{
    let suggestions = [];// getting all required elements
    const searchWrapper = document.querySelector(".search-input");
    const inputBox = searchWrapper.querySelector("input");
    const suggBox = searchWrapper.querySelector(".autocom-box");
    const icon = searchWrapper.querySelector(".icon");
    let linkTag = searchWrapper.querySelector("a");
    let webLink;
    
    // if user press any key and release
    inputBox.onkeyup = (e)=>{
        let userData = e.target.value; //user enetered data
        let emptyArray = [];
        if(userData){
            $.ajax({
              url:"/search_this",
              type:'POST',
              data:{p_name:userData},
              success:function(response){
                if(response!="none")
                {
                  response=JSON.parse(response)
                }
                else
                response=[]
                suggestions=[]
                
                for(var i=0;i<response.length;i++){
                  list=[]
                  list.push(response[i].p_name)
                  list.push(response[i].p_id)
                  suggestions.push(list)
                }
                emptyArray = suggestions.filter((data)=>{
                //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
                return data
            });
            emptyArray = emptyArray.map((data)=>{
                // passing return data inside li tag
                var link="/search_product/"+parseInt(data[1]) 
                return data = `<a style="text-decoration: none;" href="${link} "><li>`+ data[0] +'</li></a>';//here we have to change the ip
            });
            searchWrapper.classList.add("active"); //show autocomplete box
            showSuggestions(emptyArray);
            
              }
            });
          
          
            
        }else{
            searchWrapper.classList.remove("active"); //hide autocomplete box
        }
    }
    
    
    
    function showSuggestions(list){
        let listData;
        if(!list.length){
            userValue = inputBox.value;
            listData = '<li>'+ userValue +'</li>';
        }else{
            listData = list.join('');
        }
        suggBox.innerHTML = listData;
    }
})
    