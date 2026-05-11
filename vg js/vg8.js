var vg_8 = "./vg%20json/top_stations.vg.json";
vegaEmbed("#top_stations", vg_8, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
