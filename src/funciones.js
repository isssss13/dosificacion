import * as Swal from 'sweetalert2'

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

$("#addUsuarios").on('click',(e) =>{
    $.ajax({
        method:"POST",
        url:"/addusuarios",
        data:$('#agregarUsuarios').serialize(),
        success:function(r){
            Swal.fire({
                icon: r.resultado,
                title: r.text,
            }).then((result)=>{
                location.reload();
            })
        }
    });
});

$('#editUsuario').on('click',()=>{
    $.ajax({
        method:"POST",
        url:"/editusuarios",
        data:$('#usuario_edit').serialize(),
        success:function(r){
            Swal.fire({
                icon: r.resultado,
                title: r.text,
            })
            if (r.resultado=='success'){
                $('#editUsuarios').modal('hide');
            }
        }
    });
});

$('#updatePass').on('click',()=>{
    let pass=$('#password').val()
    let passconf=$('#passwordconf').val()
    if (pass==passconf){
        $.ajax({
            method:"POST",
            url:"/passupd",
            data:$('#editarContrasena').serialize(),
            success:function(r){
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                }).then((result)=>{
                    $(location).attr('href',"/logout");
                })
            }
        });
    }else{
        Swal.fire({
            icon: 'warning',
            title: 'Contraseñas no coinciden',
        })        
    }   
});

$('#iniciarSesion').on('click',()=>{
    $.ajax({
        method:"POST",
        url:"/initsesion",
        data:$('#loginUsuario').serialize(),
        success:function(r){
            if (r.resultado=='success'){
                $(location).attr('href',"/");
            }else{
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                })
            }
        }
    });
});

$('#delUsuario').on('submit',(e)=>{
    e.preventDefault();
    $.ajax({
        method:"POST",
        url:"/eliminarUsuario",
        data:$('#delUsuario').serialize(),
        success:function(r){
            if (r.resultado=='success'){
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                }).then((result)=>{
                    location.reload();
                })
            }else{
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                })
            }
        }
    })    
})

$('#passUsuario').on('submit',(e)=>{
    e.preventDefault();
    $.ajax({
        method:"POST",
        url:"/restablecerPassword",
        data:$('#passUsuario').serialize(),
        success:function(r){
            if (r.resultado=='success'){
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                }).then((result)=>{
                    location.reload();
                })
            }else{
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                })
            }
        }
    })    
})

$('#PermisosUsuario').on('submit',(e)=>{
    e.preventDefault();
    $.ajax({
        method:"POST",
        url:"/cambiarPermisos",
        data:$('#PermisosUsuario').serialize(),
        success:function(r){
            if (r.resultado=='success'){
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                }).then((result)=>{
                    location.reload();
                })
            }else{
                Swal.fire({
                    icon: r.resultado,
                    title: r.text,
                })
            }
        }
    })
})