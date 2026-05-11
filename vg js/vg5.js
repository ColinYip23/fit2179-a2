var vg_5 = "vg json/ridership_sankey_diagram.vg.json";
vegaEmbed("#ridership_sankey_diagram", vg_5, { renderer: "svg", actions: false }).then(function(result) {
// Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
}).catch(console.error);
