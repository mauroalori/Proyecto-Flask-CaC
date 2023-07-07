console.log(location.search); // lee los argumentos pasados a este formulario
var id = location.search.substr(4);
console.log(id);
const { createApp } = Vue;
createApp({
  data() {
    return {
      id: 0,
      nombre: "",
      apellido: "",
      ciudad: "",
      tiempo: 0,
      url: "https://mauroalori.pythonanywhere.com/corredores/" + id,
    };
  },
  methods: {
    fetchData(url) {
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.id = data.id;
          this.nombre = data.nombre;
          this.ciudad = data.ciudad;
          this.apellido = data.apellido;
          this.tiempo = data.tiempo;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        });
    },
    modificar() {
      let corredor = {
        nombre: this.nombre,
        apellido: this.apellido,
        tiempo: this.tiempo,
        ciudad: this.ciudad,
      };
      var options = {
        body: JSON.stringify(corredor),
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };
      fetch(this.url, options)
        .then(function () {
          alert("Registro modificado");
          window.location.href = "index.html";
        })
        .catch((err) => {
          console.error(err);
          alert("Error al Modificar");
        });
    },
  },
  created() {
    this.fetchData(this.url);
  },
}).mount("#app");
