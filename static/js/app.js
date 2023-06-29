// 1.	Use the D3 library to read in samples.json from
const all_query_values = "/api/v1.0/AZ"

// Fetch the JSON data and console log it
d3.json(all_query_values).then(function(data) {
  console.log(data);
});



// Create a droupdown menu and sample selection
function init() {
  // Use D3 to select the dropdown menu
  let dropdownMenu = d3.select("#selDataset");
  
  // Use D3 to get sample names and populate the drop-down selector
    d3.json(all_query_values).then((data) => {
        
        // Set a variable for the sample names
        let names = data.names;

    // Add  samples to dropdown menu
        names.forEach((id) => {    
    });
}
