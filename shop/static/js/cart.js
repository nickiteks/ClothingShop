var updateBtns = document.getElementsByClassName('update-cart')
var updateSizes = document.getElementsByClassName('size')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'action:',action)

        console.log('USER:',user)
        if(user === 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}

function addCookieItem(productId,action){
     console.log('Not logged in ')

     if(action == 'delete'){
        delete cart[productId]
     }

     if(action == 'add'){
        if(cart[productId] === undefined){
            cart[productId] = {'quantity':1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
     }

     if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
     }

    console.log("Cart:",cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload();
}

function updateUserOrder(productId,action){
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action': action,'size':"XS"})
    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}


for(var i = 0; i < updateSizes.length; i++){
    updateSizes[i].addEventListener('change',function() {
    var productId = this.dataset.product
    var action = this.dataset.action
    if(user === 'AnonymousUser'){
            addCookieSize(productId,action)
        }else{
            ChangeSize(productId,action,i);
        }
    });
}

function ChangeSize(productId,action,index){
    var url = '/update_item/'
    var size;
    for(var i = 0; i < updateSizes.length; i++){
        var attr = updateSizes[i].dataset.product
        if(attr == productId){
            size = updateSizes[i].options[updateSizes[i].selectedIndex].text
        }
    }

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action': action,'size':size})
    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}

function addCookieSize(productId,action){
    console.log('Not logged in ')
    var size;
    for(var i = 0; i < updateSizes.length; i++){
        var attr = updateSizes[i].dataset.product
        if(attr == productId){
            size = updateSizes[i].options[updateSizes[i].selectedIndex].text
        }
    }
    if(action == 'size'){
        cart[productId] = {'size':size,'quantity':cart[productId]['quantity']}
    }

    console.log("Cart:",cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}