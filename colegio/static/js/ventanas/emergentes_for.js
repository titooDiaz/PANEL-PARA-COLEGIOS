function showVentana(modal, pk) {
    const ventana = document.getElementById(modal+pk);
    ventana.classList.remove('hidden');
}

function closeVentana(modal,pk) {
const ventana = document.getElementById(modal+pk);
ventana.classList.add('hidden');
}


// EJEMPLO:

// {% for corte in cortes %}
//         <div class="items-center bg-white border-4 border-gray-200 rounded-lg sm:flex p-4 block shadow-2xl hover:scale-105 duration-300 ease-in-out">
//             <div class="block w-full">
//                 <h5 class="font-mono font-bold text-gray-900 text-9xl text-center">{{corte.corte_num}}</h5>
//                 <p class="font-mono font-bold text-gray-900 text-lg text-center">{{corte.fecha_inicio}} - {{corte.fecha_fin}}</p>
//                 <div class="mt-2 flex">
//                   <button onclick="showVentana('information', '{{corte.pk}}')" type="button" id="active_information" class="myButton font-semibold text-white px-2 rounded-lg bg-orange-600 border-l border-r border-t border-4 border-orange-800 hover:scale-105 transition duration-300 ease-in-out focus:border focus:mt-1 py-2 text-center text-lg w-full">Editar Fechas</button>
//                 </div>
//             </div>
//         </div>

//         <div id="information{{corte.pk}}" class="hidden fixed left-0 top-0 z-50 w-full h-screen bg-[#5858587c]">
                            
//             <div class="flex items-center justify-center min-h-screen">
//                 <div class="bg-white border-2 border-black p-4 rounded-lg">
//                     <button onclick="closeVentana('information', '{{corte.pk}}')" class="hover:cursor-pointer w-full flex justify-end items-center py-1 px-2 text-red-500">
//                         <p class="mr-4">cerrar</p>
//                         <i class="fa-solid fa-circle-xmark"></i>
//                     </button>
                    
//                     <div class="mb-4">
//                         <h5 class="flex text-2xl"><span class="time_locate text-center w-full"></span></h5> <!--Localizacion del usuario actual-->
//                         <h5 class="flex text-2xl"><span class="time_zone hidden text-center w-full">{{request.user.time_zone}}</span></h5> <!--localizacion de hora al crear al usuario-->
                    
//                     </div>

//                     {{actividades.zona_horaria}}
//                     <p class="text-sm mt-4">
//                         ACTIVO: 
//                         <br>
//                         ZONA HORARIA LOCAL (<span id="time_locate"></span>)
//                         <br>
                        
//                         <br>
//                         DESACTIVO: 
//                         <br>
//                         ZONA HORARIA CON QUE FUISTE CREADO (<span>{{ request.user.time_zone }}</span>)
//                     </p> 
//                 </div> 
//             </div>
            
//         </div>
//     {% endfor %}