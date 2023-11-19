const elementosZoom5 = document.querySelectorAll('.zoom-5');
elementosZoom5.forEach(elemento => {
  const texto = elemento.textContent.trim();
  console.log(texto)
  const letrasAumentadas = texto
    .split('')
    .map(letra => `<span class="aumentar-5">${letra}</span>`)
    .join('');

  elemento.innerHTML = letrasAumentadas;
});

const elementosZoom4 = document.querySelectorAll('.zoom-4');
elementosZoom4.forEach(elemento => {
  const texto = elemento.textContent.trim();
  console.log(texto)
  const letrasAumentadas = texto
    .split('')
    .map(letra => `<span class="aumentar-4">${letra}</span>`)
    .join('');

  elemento.innerHTML = letrasAumentadas;
});

const elementosZoom3 = document.querySelectorAll('.zoom-3');
elementosZoom3.forEach(elemento => {
  const texto = elemento.textContent.trim();
  console.log(texto)
  const letrasAumentadas = texto
    .split('')
    .map(letra => `<span class="aumentar-3">${letra}</span>`)
    .join('');

  elemento.innerHTML = letrasAumentadas;
});

const elementosZoom2 = document.querySelectorAll('.zoom-2');
elementosZoom2.forEach(elemento => {
  const texto = elemento.textContent.trim();
  console.log(texto)
  const letrasAumentadas = texto
    .split('')
    .map(letra => `<span class="aumentar-2">${letra}</span>`)
    .join('');

  elemento.innerHTML = letrasAumentadas;
});

const elementosZoom1 = document.querySelectorAll('.zoom-1');
elementosZoom1.forEach(elemento => {
  const texto = elemento.textContent.trim();
  console.log(texto)
  const letrasAumentadas = texto
    .split('')
    .map(letra => `<span class="aumentar-1">${letra}</span>`)
    .join('');

  elemento.innerHTML = letrasAumentadas;
});