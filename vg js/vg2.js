var vg_1 = "./vg%20json/sg_vs_my_ridership.vg.json";
vegaEmbed("#sg_vs_my_ridership", vg_1, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
