var vg_9 = "./vg%20json/ridership_volatility.vg.json";
vegaEmbed("#ridership_volatility", vg_9, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
