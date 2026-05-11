var vg_4 = "./vg%20json/ridership_heatmap.vg.json";
vegaEmbed("#ridership_heatmap", vg_4, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
