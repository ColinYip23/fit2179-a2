var vg_3 = "./vg%20json/hourly_ridership.vg.json";
vegaEmbed("#hourly_ridership", vg_3, { renderer: "svg", actions: false, loader: { baseURL: "./" } }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
