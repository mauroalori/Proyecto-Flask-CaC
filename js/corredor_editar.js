console.log(location.search); // lee los argumentos pasados a este formulario
var id = location.search.substr(4);
console.log(id);
const { createApp } = Vue;
createApp({
  data() {
    return {
      paises: [],
      id: 0,
      nombre: "",
      apellido: "",
      pais: "",
      tiempo: 0,
      codigo_pais: "",
      nombre_pais: "",
      imagen_pais: "",
      url_corredores: "https://mauroalori.pythonanywhere.com/corredores/" + id,
    };
  },
  methods: {
    fetchData(url_corredores) {
      fetch(url_corredores)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.id = data.id;
          this.nombre = data.nombre;
          this.pais = data.pais;
          this.apellido = data.apellido;
          this.tiempo = data.tiempo;
          return fetch("https://mauroalori.pythonanywhere.com/paises/" + this.pais);
        })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.codigo_pais = data.codigo;
          this.nombre_pais = data.nombre;
          this.imagen_pais = data.imagen;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        });
      fetch("https://mauroalori.pythonanywhere.com/paises")
        .then((response) => response.json())
        .then((data) => {
          this.paises = data;
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
        pais: this.pais,
      };
      var options = {
        body: JSON.stringify(corredor),
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };
      fetch(this.url_corredores, options)
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
    this.fetchData(this.url_corredores);
  },
}).mount("#app");
