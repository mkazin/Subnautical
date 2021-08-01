
let markerTypes = new Set();
let svg;

// Note: this is a primitive use of D3. Learn it better and
// make it look good. See:
// https://observablehq.com/@xianwu/force-directed-graph-network-graph-with-arrowheads-and-lab -->
let min_x=-1500, max_x=1400;
let min_y=-1350, max_y=800;
let height=800, width=800, margin=50;

var yAxisLength = height - 2 * margin,
    xAxisLength = width - 2 * margin;

var xScale = d3
      .scaleLinear()
      .domain([min_x, max_x])
      .range([0, xAxisLength]),
    yScale = d3
      .scaleLinear()
      .domain([max_y, min_y])
      .range([0, yAxisLength]);

function renderXAxis() {
    var xAxis = d3
      .axisBottom()
      // .ticks(lawfulness.length)
      // .tickFormat(t => {
      //   return lawfulness[t];
      // })
      .scale(xScale);

    svg
      .append("g")
      .attr("class", "x-axis")
      .attr("transform", function() {
        return "translate(" + margin + "," + (height - margin) + ")";
      })
      .attr("opacity", 1)
      .call(xAxis);

    d3.selectAll("g.x-axis g.tick")
      .append("line")
      .classed("grid-line", true)
      .attr("x1", 0)
      .attr("y1", 0)
      .attr("x2", 0)
      .attr("y2", -(height - 2 * margin))
      .attr("opacity", 0.4);

      return true;
  }

function renderYAxis() {
    var yAxis = d3
      .axisLeft()
        <!--
      // .ticks(goodness.length)
      // .tickFormat(t => {
      //   return goodness[t];
      // })
      -->
      .scale(yScale);

    svg
      .append("g")
      .attr("class", "y-axis")
      .attr("transform", function() {
        return "translate(" + margin + "," + margin + ")";
      })
      .call(yAxis);

    d3.selectAll("g.y-axis g.tick")
      .append("line")
      .classed("grid-line", true)
      .attr("x1", 0)
      .attr("y1", 0)
      .attr("x2", yAxisLength)
      .attr("y2", 0)
      .attr("fill", d3.rgb("#000000"));
  }

function renderMarker(x, y, depth, text, color, markerType) {
    const node = svg //.selectAll(".nodes")
        //.data(dataset.nodes)
        // .enter()
        .append("g")
        .attr("class", "nodes")
        .attr("marker-type", markerType)

    let opacity = 1.0 - Math.min(-depth / 1000.0, .8);

    node.append("circle")
        .attr("transform", function() {
            return "translate(" + margin + "," + margin + ")";
        })
        .attr("cx", xScale(x))
        .attr("cy", yScale(y))
        .attr("fill", d3.rgb(color))
        .attr("opacity", opacity)
        .style("stroke", "black") //depth => depth > -1 ? "red" : undefined)
        .attr("r", 10);

    node.append("text")
        .attr("transform", function() {
            return "translate(" + margin + "," + margin + ")";
        })
        .attr("dy", yScale(y) + 4)
        .attr("dx", xScale(x) + 15)
        .text(text);

    node.append("title")
        .text(text);
}

function titleCase(text) {
    return text.split('_').map(word => {
            return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
        }).join(' ');
}

function renderLegend() {
    Array.from(markerTypes).sort().forEach(type_enum => {
        addLegendItem(type_enum)
    })

    document.querySelector(".legend-clear-all").addEventListener("click", function() {legendSetAll(false)})
    document.querySelector(".legend-check-all").addEventListener("click", function() {legendSetAll(true)})
}

function addLegendItem(type_enum) {
    let legendDiv = document.querySelector('.legend')
    let markerTypeDiv = document.createElement('div')
    legendDiv.appendChild(markerTypeDiv)

    addLegendItemCheckbox(type_enum, markerTypeDiv)
    addLegendItemLabel(type_enum, markerTypeDiv)
}

function addLegendItemCheckbox(type_enum, markerTypeDiv) {
    var checkbox = document.createElement('input')
    checkbox.setAttribute("type", "checkbox")
    checkbox.setAttribute("value", type_enum)
    checkbox.checked = true;
    markerTypeDiv.appendChild(checkbox)
    checkbox.addEventListener('click', checkboxClickListener)
}

function addLegendItemLabel(type_enum, markerTypeDiv) {
    var label = document.createElement('label')
    label.setAttribute("for", type_enum)
    label.textContent  = titleCase(type_enum.split('.')[1])
    markerTypeDiv.appendChild(label)
}
function checkboxClickListener(e) {
    var checkbox = e.target
    d3.selectAll(".nodes[marker-type='" + checkbox.value + "']")
        .style("opacity", (checkbox.checked ? 1 : 0))
}

function legendSetAll(checked) {
    document.querySelectorAll("input[type=checkbox]").forEach(checkbox => {
        if (checkbox.checked !== checked) {
            checkbox.click()
        }
    })
}

function renderAllMarkers(mapData) {
    mapData.forEach(marker => {
        markerTypes.add(marker.marker_type)
        renderMarker(marker.x, marker.y, marker.depth, marker.name, "#FF0000", marker.marker_type);
    });
}

function clearAllMarkers() {
    document.querySelectorAll('.nodes').forEach(node => {
        document.querySelector('.axis').removeChild(node)
        });
}

function renderMap(mapData) {
    svg = d3
        .select(".plot")
        .append("svg")
        .attr("class", "axis")
        .attr("width", width)
        .attr("height", height);

    Promise.all([renderXAxis(), renderYAxis()])
    Promise.resolve(renderAllMarkers(mapData))
    renderLegend()
}

document.querySelector(".add-bearing").addEventListener(function () {

});
