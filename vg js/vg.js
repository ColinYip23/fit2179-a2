var vg_1 = "./vg%20json/ridership_flowmap.vg.json";
vegaEmbed("#bar_chart", vg_1, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
