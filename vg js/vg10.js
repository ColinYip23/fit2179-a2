var vg_10 = "./vg%20json/distance_vs_ridership.vg.json";
vegaEmbed("#distance_vs_ridership", vg_10, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
