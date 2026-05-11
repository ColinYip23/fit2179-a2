var vg_8 = "vg json/top_stations.vg.json";
vegaEmbed("#top_stations", vg_8, { renderer: "svg", actions: false }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
