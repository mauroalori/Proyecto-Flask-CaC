const { createApp } = Vue;
createApp({
  data() {
    return {
      corredores: [],
      url: "http://localhost:5000/corredores",
      // si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
      //url:'http://mauroalori.pythonanywhere.com/corredores', // si ya lo subieron a pythonanywhere
      error: false,
      cargando: true,
      /*atributos para el guardar los valores del formulario */
      id: 0,
      nombre: "",
      apellido: "",
      ciudad: "",
      tiempo: 0,
    };
  },
  methods: {
    fetchData(url) {
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          this.corredores = data;
          this.ordenarCorredoresPorTiempoAsc();
          this.cargando = false;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        });
    },
    ordenarCorredoresPorTiempoAsc() {
      this.corredores = this.corredores.sort(function (corredor1, corredor2) {
        if (corredor1.tiempo > corredor2.tiempo) {
          return 1;
        }
        if (corredor1.tiempo < corredor2.tiempo) {
          return -1;
        }
        return 0;
      });
    },
    eliminar(corredor) {
      const url = this.url + "/" + corredor;
      var options = {
        method: "DELETE",
      };
      fetch(url, options)
        .then((res) => res.text()) // or res.json()
        .then((res) => {
          location.reload();
        });
    },
    grabar() {
      let corredor = {
        nombre: this.nombre,
        apellido: this.apellido,
        tiempo: this.tiempo,
        ciudad: this.ciudad,
      };
      var options = {
        body: JSON.stringify(corredor),
        method: "POST",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };
      fetch(this.url, options)
        .then(function () {
          alert("Corredor grabado");
          window.location.href = "index.html";
        })
        .catch((err) => {
          console.error(err);
          alert("Error al Grabarr");
        });
    },
  },
  created() {
    this.fetchData(this.url);
  },
}).mount("#app");
