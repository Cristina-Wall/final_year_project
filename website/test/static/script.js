// function pass_values() {
//     var pass_to_python = new Number(7)
 
//     $.ajax({
//         type:'POST',
//         contentType:'application/json;charset-utf-08',
//         dataType:'json',
//         url:'http://127.0.0.1:5000/pass_val?value='+pass_to_python ,
//         success:function (data) {
//             var reply=data.reply;
//             if (reply=="success") {
//                 return;
//             }
//             else{
//                 alert("some error ocured in session agent")
//             }
//         }
//     });
// }

function sendData() { 
    var value = document.getElementById('input').value; 
    $.ajax({ 
        url: '/process', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 'value': value }), 
        success: function(response) { 
            document.getElementById('output').innerHTML = response.result; 
        }, 
        error: function(error) { 
            console.log(error); 
        } 
    }); 
} 