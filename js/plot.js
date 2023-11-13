function formatDiskSize(sizeInBytes) {
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];

    let i = 0;
    const bigSize = new Big(sizeInBytes);
    while (bigSize.gte(1024) && i < sizes.length - 1) {
        bigSize.div(1024);
        i++;
    }

    // Round to two decimal places
    const roundedSize = bigSize.round(0);

    return {
        formatted: `${roundedSize.toString()} ${sizes[i]}`,
        numeric: +roundedSize // Use the unary plus operator to convert to a number
    };
}


function createChart(chartData, chartId) {
    chartData.forEach(trace => {
        trace.y = trace.y.map(sizeInBytes => formatDiskSize(sizeInBytes));
    });

    // Find the maximum numeric value for setting the y-axis range
    const maxYValue = Math.max(...chartData.flatMap(trace => trace.y.map(entry => entry.numeric)));
    
    // Increase maxYValue by 10%
    const increasedMaxValue = maxYValue * 1.25;

    const trace = {
        
    }

    var layout = { 
        title: chartId, 
        yaxis: {
            title: 'usage',
            range: [0, increasedMaxValue], // Set the range based on the numeric values
        },
        // height: height,
        // width: width
    };

    chartData.forEach(trace => {
        // Use the numeric values for plotting
        trace.y = trace.y.map(entry => entry.numeric);
        
        // Update hoverinfo to include formatted size
        trace.hoverinfo = 'y+text';
        trace.text = trace.y.map(entry => formatDiskSize(entry).formatted); // Set text for hoverinfo
    });

    var config = {responsive: true};

    Plotly.newPlot(chartId, chartData, layout, config);
}

// Fetch data from JSON file
fetch('data/dp9_gdata_lquota_output.json')
    .then(response => response.json())
    .then(data => {
        // Create gdata disk
        createChart(data.disk, 'gdata_disk');
        // Create gdata inode
        createChart(data.inode, 'gdata_inode');
    })
    .catch(error => console.error('Error fetching data:', error));

// Fetch data from JSON file
fetch('data/dp9_scratch_lquota_output.json')
    .then(response => response.json())
    .then(data => {
        // Create scretch disk
        createChart(data.disk, 'scratch_disk');
        // Create scratch inode
        createChart(data.inode, 'scratch_inode');
    })
    .catch(error => console.error('Error fetching data:', error));
