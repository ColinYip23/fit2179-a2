var vg_7 = "./vg%20json/fuel_vs_ridership.vg.json";
vegaEmbed("#fuel_vs_ridership", vg_7, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
