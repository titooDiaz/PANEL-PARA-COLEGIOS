const elementosZoom = document.querySelectorAll('.zoom-5');
elementosZoom.forEach(elemento => {
  const texto = elemento.textContent.trim();
  console.log(texto)
  const letrasAumentadas = texto
    .split('')
    .map(letra => `<span class="aumentar-5">${letra}</span>`)
    .join('');

  elemento.innerHTML = letrasAumentadas;
});