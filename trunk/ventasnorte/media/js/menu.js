function menu(){
    var arr = location.pathname.split("/")
    switch (arr[1]){
        case "":
            $("#mnu_home").addClass("active")
            $("#a_home").addClass("active")
            break;
        case "autos":
            $("#mnu_autos").addClass("active")
            $("#a_autos").addClass("active")
            break;
        case "casas":
            $("#mnu_casas").addClass("active")
            $("#a_casas").addClass("active")
            break;
        case "about":
            $("#mnu_about").addClass("active")
            $("#a_about").addClass("active")
            break;
        case "contact":
            $("#mnu_contact").addClass("active")
            $("#a_contact").addClass("active")
            break;
        default:
            break;


    }
}

$( document ).ready( function() {
menu();
});
