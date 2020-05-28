import 'morris.js/morris.js'

$(document).ready(function(){
    flujoUsuarios(flujo);
    // flujoTrenes(trenes);
})

const flujoUsuarios =()=>{
    $.ajax({
        url:"",
        data:,
        success:function(r){
            if(r.resultado=="error"){
                document.getElementById("FlujoDeUsuarios").innerHTML="Sin datos por el momento"
            }else{
                document.getElementById("FlujoDeUsuarios").innerHTML="Los datos estan en camino"
            }
        }
    })
}

const graficas = (flujo)=>{
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

