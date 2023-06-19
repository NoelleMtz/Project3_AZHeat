// 1.	Use the D3 library to read in samples.json from
const all_query_values = "/api/v1.0/AZ"
const twentyone_query_values = "api/v1.0/AZ2021";
const Apache_query_values = "/api/v1.0/ApacheCounty";

// Fetch the JSON data and console log it
d3.json(all_query_values).then(function(data) {
  console.log(data);
});

// Fetch the JSON data and console log it
d3.json(twentyone_query_values).then(function(data) {
  console.log(data);
});

// Fetch the JSON data and console log it
d3.json(Apache_query_values).then(function(data) {
  console.log(data);
});

function buildLineChart(Apache) {

    // Use D3 to retrieve all of the data
    d3.json(Apache_query_values).then((data) => {

      // Retrieve all sample data      
      let allInfo = Object.entries(data);
      let EHD = allInfo.map(entry => entry[0]);
      let years = allInfo.map(entry => entry[1]);

      let lineValues = {
          x: years,
          y: EHD,
          mode: 'lines+markers',
          marker: {
              size: 12,
              opacity:0.5
          }
      };

      let lineLayout = {
          title: "Extreme Heat Days in Apache County"
      };

      Plotly.newPlot("linePlot", [lineValues], lineLayout);
  });
};
