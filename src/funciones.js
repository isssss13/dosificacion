import 'morris.js/morris.js'
import * as Swal from 'sweetalert2'

$(document).ready(function(){
    flujoUsuarios();
    setInterval(flujoUsuarios,60000)
    // flujoTrenes(trenes);
})

const flujoUsuarios =()=>{
    $.ajax({
        method:'POST',
        headers: { "X-CSRFToken": token },
        url:"/graficas",
        data:{ dato : estacion },
        datatype: "json",
        success:function(r){
            if(r.resultado=="error"){
                document.getElementById("FlujoDeUsuarios").innerHTML="Sin datos por el momento"
            }else{
                const flujo=[
                    { hour: r.fec[0], value: r.graf[0] },
                    { hour: r.fec[1], value: r.graf[1] },
                    { hour: r.fec[2], value: r.graf[2] },
                    { hour: r.fec[3], value: r.graf[3] },
                    { hour: r.fec[4], value: r.graf[4] },
                    { hour: r.fec[5], value: r.graf[5] },
                    { hour: r.fec[6], value: r.graf[6] },
                    { hour: r.fec[7], value: r.graf[7] },
                    { hour: r.fec[8], value: r.graf[8] },
                    { hour: r.fec[9], value: r.graf[9] },
                    { hour: r.fec[10], value: r.graf[10] },
                    { hour: r.fec[11], value: r.graf[11] },
                ];
                graficas(flujo);
                // document.getElementById("FlujoDeUsuarios").innerHTML="Los datos estan en camino"
            }
        }
    })
}

const graficas = (flujo)=>{
    document.getElementById("FlujoDeUsuarios").innerHTML=""
    let datos=flujo
    new Morris.Area({
    element: 'FlujoDeUsuarios',
    data: flujo,
    xkey: ['hour'],
    ykeys: ['value'],
    xLabels:['15min'],
    labels: ['Personas'],
    gridTextColor:['#000000'],
    lineColors:['#f48405'],
    }).on('click',properties=>{
        console.log(datos)
    });
}
// const flujoTrenes= (trenes) => {
//     let datos=trenes
//     new Morris.Area({
//         element: 'Trenes',
//         data: trenes,
//         xkey: ['date'],
//         ykeys: ['value'],
//         xLabels:['day'],
//         labels: ['Trenes'],
//         gridTextColor:['#000000'],
//         lineColors:['#f48405'],
//     }).on('click',properties=>{
//         console.log(datos)
//     })

// }



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