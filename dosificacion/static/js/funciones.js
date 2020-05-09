$("#agrUsuarios").on('click',() =>{
    $("#newUsuarios").modal('show');
});

$("#menu-toggle").on('click',(e) =>{
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

$("#logout").on('click',()=> {
    Swal.fire({
        position:'top-end',
        title: 'Cerrar sesion?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.value) {
            $(location).attr('href',"/logout");
        }
    })
});

$("#home").on('click',(e) =>{
    $(location).attr('href',"/");
});

$("#addEstacion").on('click',(e) =>{
    $("#addLinea").modal('show');
    
});

$("#perfil").on('click',() =>{
    $("#userPerfil").modal('show');    
});

$("#editDatos").on('click',() =>{
    $("#editUsuarios").modal('show');    
});

$("#pass").on('click',() =>{
    $("#changepass").modal('show');    
});
