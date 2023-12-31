const { createApp } = Vue;
createApp({
  data() {
    return {
      corredores: [],
      paises: [],
      //url: "http://localhost:5000/corredores",
      // si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
      url_corredores:'https://mauroalori.pythonanywhere.com/corredores', // si ya lo subieron a pythonanywhere
      url_paises:'https://mauroalori.pythonanywhere.com/paises', // si ya lo subieron a pythonanywhere
      error: false,
      cargando: true,
      filtrar_por: 'no-filtrar',
      /*atributos para el guardar los valores del formulario */
      id: 0,
      nombre: "",
      apellido: "",
      pais: "",
      tiempo: 0,
    };
  },
  methods: {
    fetchData(url_corredores,url_paises) {
      fetch(url_corredores)
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
      fetch(url_paises)
        .then((response) => response.json())
        .then((data) => {
          this.paises = data;
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
      for (const pos in this.corredores){
        this.corredores[pos].posicion = parseInt(pos)+1;
      }
    },
    eliminar(corredor) {
      const url = this.url_corredores + "/" + corredor;
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
        pais: this.pais,
      };
      var options = {
        body: JSON.stringify(corredor),
        method: "POST",
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };
      fetch(this.url_corredores, options)
        .then(function () {
          alert("Corredor grabado");
          window.location.href = "index.html";
        })
        .catch((err) => {
          console.error(err);
          alert("Error al Grabarr");
        });
    },
    imagenPais(codigo){
      return this.paises.find(pais => pais.codigo === codigo).imagen;
    },
  },
  computed: {
    corredoresFiltrados() {
      if (this.filtrar_por!="no-filtrar") {
        return this.corredores.filter(corredor => corredor.pais === this.filtrar_por);
      } 
      else {
        return this.corredores;
      }
    }
  },
  created() {
    this.fetchData(this.url_corredores,this.url_paises);
  },
}).mount("#app");
