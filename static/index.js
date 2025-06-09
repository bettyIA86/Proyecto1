async function getAirQuality() {
  const city = document.getElementById("cityInput").value;
  const apiKey = "TU_API_KEY"; // Reemplaza con tu API Key real

  //const url = `https://api.airvisual.com/v2/city?city=${city}&state=Lima&country=Peru&key=${apiKey}`;
  const url = 'https://www.iqair.com/world-air-quality';

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data.status === "success") {
      const aqi = data.data.current.pollution.aqius;
      const status = getAQIDescription(aqi);
      document.getElementById("result").innerHTML =
        `<p><strong>${city}</strong>: AQI = ${aqi} (${status})</p>`;
    } else {
      document.getElementById("result").innerHTML = "Ciudad no encontrada.";
    }
  } catch (error) {
    document.getElementById("result").innerHTML = "Error al obtener los datos.";
  }
}

function getAQIDescription(aqi) {
  if (aqi <= 50) return "Buena";
  if (aqi <= 100) return "Moderada";
  if (aqi <= 150) return "Dañina para sensibles";
  if (aqi <= 200) return "Dañina";
  if (aqi <= 300) return "Muy dañina";
  return "Peligrosa";
}

function submitData() {
    const fechaI = document.getElementById('fechaIni').value;
    const fechaF = document.getElementById('fechaFin').value;

  //verificar que ambas fechas están seleccionadas
  if (!fechaI || !fechaF){
    alert('Por favor, seleccionar ambas fechas');
    return;
  }

  //crear el bojeto datos a enviar
  const datos = {
    fechaIni: fechaI,
    fechaFin: fechaF
  }
    fetch('/calcular', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ datos})
    })
    .then(response => response.json())
    .then(result => {
    // Mostrar el resultado en la página
       //document.getElementById("result").innerText = `Resultado: ${result.prediccion}`;
       alert('Resultado calculado con  exito' + `Resultado: ${result.prediccion}`)
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
