var vg_11 = "./vg%20json/ridership_proportional_symbol_map.vg.json";
vegaEmbed("#ridership_proportional_symbol_map", vg_11, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);