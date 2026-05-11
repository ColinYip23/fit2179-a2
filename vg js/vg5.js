var vg_5 = "./vg%20json/ridership_sankey_diagram.vg.json";
vegaEmbed("#ridership_sankey_diagram", vg_5, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
