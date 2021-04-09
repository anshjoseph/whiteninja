var cod = document.getElementById("cod");
var ff = document.getElementById("ff");
var pg = document.getElementById("pg");
var cod_con = document.getElementById("cod_write");
var ff_con = document.getElementById("ff_write");
var pg_con = document.getElementById("pg_write");
var submit = document.getElementById("sub_btn")
if(cod_con != null){
    cod_con.style.display= "none";
}
if (ff_con != null){
    ff_con.style.display = "none";
}
if ( pg_con != null){
    pg_con.style.display = "none";
}
submit.style.display = "none";
function cod_chbox(){
    if (cod.checked){
        cod_con.style.display = "block";
        submit.style.display = "block";
    }
    else{
        cod_con.style.display = "none";
        submit.style.display = "none";
    }
}
function ff_chbox(){
    if(ff.checked){
        ff_con.style.display = "block"
        submit.style.display = "block";
    }
    else{
        ff_con.style.display = "none"
        submit.style.display = "none";
    }
    
}
function pg_chbox(){
    if(pg.checked){
        pg_con.style.display = "block";
        submit.style.display = "block";
    }
    else{
        pg_con.style.display = "none"
        submit.style.display = "none";
    }
    
}


