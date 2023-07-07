const { createApp } = Vue;
createApp({
  data() {
    return {
      registros: [],
      url: "http://localhost:5000/productos",
      // si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
      //url:'http://mauroalori.pythonanywhere.com/productos', // si ya lo subieron a pythonanywhere
      error: false,
      cargando: true,
      /*atributos para el guardar los valores del formulario */
      id: 0,
      nombre: "",
      imagen: "",
      stock: 0,
      precio: 0,
    };
  },
  methods: {
    fetchData(url) {
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          this.registros = data;
          this.ordenarRegistrosPorTiempoAsc();
          this.cargando = false;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        });
    },
    ordenarRegistrosPorTiempoAsc() {
      this.registros = this.registros.sort(function (regi1, regi2) {
        if (regi1.tiempo > regi2.tiempo) {
          return 1;
        }
        if (regi1.tiempo < regi2.tiempo) {
          return -1;
        }
        return 0;
      });
    },
    eliminar(registro) {
      const url = this.url + "/" + registro;
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
      let producto = {
        nombre: this.nombre,
        apellido: this.apellido,
        tiempo: this.tiempo,
        ciudad: this.ciudad,
      };
      var options = {
        body: JSON.stringify(registro),
        method: "POST",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };
      fetch(this.url, options)
        .then(function () {
          alert("Registro grabado");
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
