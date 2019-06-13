
/**
 * Jquery Ajax GET请求
 */
function getbigimg() {
    $.ajax({
        type: "get",
        // dataType: "json",
        url: "/home/getbigimg",
        dataType: "json",
        success: function(data){
            for(var i in data){
                $("#demo ul").append('<li data-target="#demo" data-slide-to="'+i+'" class="'+(i == 0? "active" : "")+'"></li>');
                $("#demo .carousel-inner").append('<div class="carousel-item '+(i == 0? "active" : "")+'"><img src="'+data[i].imgpath+'"><div class="info carousel-caption"><h1>"'+data[i].title+'"</h1><p>"'+data[i].content+'"</p></div>');    
            }
            
            $("#demo").append('<a class="carousel-control-prev" href="#demo" data-slide="prev"><span class="carousel-control-prev-icon"></span></a><a class="carousel-control-next" href="#demo" data-slide="next"><span class="carousel-control-next-icon"></span></a>');

        }
    });
}


// 局部刷新的方式
// function login(){
//     $.ajax({
//         type: "get",
//         // dataType: "json",
//         url: "/home/login",
//         dataType: "html",
//         success: function(data){
//             $("html").html("");
//             $("html").append(data);
//         }
//     });
// }



$("#login").on("click",()=>{
    window.location = "/home/login";
})
getbigimg();