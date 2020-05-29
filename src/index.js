import 'morris.js/morris.js'

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
                console.log(r.fec)
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

