let cropper = null;

var cordenadasfoto;
var cordenadasbanner;
var img;
var cords = document.querySelector('.cords')

$('#input-file').on('change', () => {
    let image = document.getElementById('img-cropper')
    img = 'crop-image'
    let input = document.getElementById('input-file')

    let archivos = input.files
    let extensiones = input.value.substring(input.value.lastIndexOf('.'), input.value.lenght)
    

    if(!archivos || !archivos.length){        
        image.src = "";
        
        
    } else if(input.getAttribute('accept').split(',').indexOf(extensiones) < 0){
         alert('Debes seleccionar una imagen')
         

    } else {
        let imagenUrl = URL.createObjectURL(archivos[0])
        image.src = imagenUrl

        cropper = new Cropper(image, {
            aspectRatio: 1, // es la proporción en la que queremos que recorte en este caso 1:1
            preview: '.img-sample', // contenedor donde se va a ir viendo en tiempo real la imagen cortada
            zoomable: false, //Para que no haga zoom 
            viewMode: 1, //Para que no estire la imagen al contenedor
            responsive: false, //Para que no reacomode con zoom la imagen al contenedor
            dragMode: 'none', //Para que al arrastrar no haga nada
            ready(){ // metodo cuando cropper ya este activo, le ponemos el alto y el ancho del contenedor de cropper al 100%
                document.querySelector('.cropper-container').style.width = '100%'
                document.querySelector('.cropper-container').style.height = '100%'
            },
            crop: function(event) {
                console.log(event.detail.x);
                console.log(event.detail.y);
                console.log(event.detail.width);
                console.log(event.detail.height);
                console.log(event.detail.rotate);
                console.log(event.detail.scaleX);
                console.log(event.detail.scaleY);
                cordenadasfoto = `${Math.round(event.detail.x)},${Math.round(event.detail.y)},${Math.round(event.detail.width)},${Math.round(event.detail.height)}`;

            }
        })

        $('.modal').addClass('active')
        $('.modal-content').addClass('active')

        $('.modal').removeClass('remove')
        $('.modal-content').removeClass('remove')
    }
})



$('#input-file-banner').on('change', () => {
    img = 'crop-image-banner'
    let image = document.getElementById('img-cropper')
    let input = document.getElementById('input-file-banner')

    let archivos = input.files
    let extensiones = input.value.substring(input.value.lastIndexOf('.'), input.value.lenght)
    

    if(!archivos || !archivos.length){        
        image.src = "";
        
    } else if(input.getAttribute('accept').split(',').indexOf(extensiones) < 0){
         alert('Debes seleccionar una imagen')
        
    } else {
        let imagenUrl = URL.createObjectURL(archivos[0])
        image.src = imagenUrl

        cropper = new Cropper(image, {
            aspectRatio: 5, // es la proporción en la que queremos que recorte en este caso 1:1
            preview: '.img-sample', // contenedor donde se va a ir viendo en tiempo real la imagen cortada
            zoomable: false, //Para que no haga zoom 
            viewMode: 1, //Para que no estire la imagen al contenedor
            responsive: false, //Para que no reacomode con zoom la imagen al contenedor
            dragMode: 'none', //Para que al arrastrar no haga nada
            ready(){ // metodo cuando cropper ya este activo, le ponemos el alto y el ancho del contenedor de cropper al 100%
                document.querySelector('.cropper-container').style.width = '100%'
                document.querySelector('.cropper-container').style.height = '100%'
            },
            crop: function(event) {
                console.log(event.detail.x);
                console.log(event.detail.y);
                console.log(event.detail.width);
                console.log(event.detail.height);
                console.log(event.detail.rotate);
                console.log(event.detail.scaleX);
                console.log(event.detail.scaleY);
                cordenadasbanner = `${Math.round(event.detail.x)},${Math.round(event.detail.y)},${Math.round(event.detail.width)},${Math.round(event.detail.height)}`;

            }
        })

        $('.modal').addClass('active')
        $('.modal-content').addClass('active')

        $('.modal').removeClass('remove')
        $('.modal-content').removeClass('remove')
    }
})


/////////////////////////////////////////////////////////

$('#close').on('click', () => {
    let image = document.getElementById('img-cropper')
    image.src = "";
    cropper.destroy()
    $('.modal').addClass('remove')
    $('.modal-content').addClass('remove')
    $('.modal').removeClass('active')
    $('.modal-content').removeClass('active')
})

$('#cut').on('click', (event) => {
    event.preventDefault();
    let crop_image = document.getElementById(img)
    let canva = cropper.getCroppedCanvas()
    let image = document.getElementById('img-cropper')

    canva.toBlob(function(blob){
        let url_cut = URL.createObjectURL(blob)
        crop_image.src = url_cut;
    })

    image.src = "";
    cords.value = cordenadasfoto+':'+cordenadasbanner

    cropper.destroy()

    $('.modal').addClass('remove')
    $('.modal-content').addClass('remove')

    $('.modal').removeClass('active')
    $('.modal-content').removeClass('active')
})
