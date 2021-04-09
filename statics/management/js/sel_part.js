form = document.getElementById("form")

function submit_req(arg){
    inp = document.getElementById("inp_tt");
    inp.setAttribute("value",arg)
    form.submit();
}