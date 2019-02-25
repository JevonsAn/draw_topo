const svg = d3.select("svg#topo");
const width = svg.attr("width");
const height = svg.attr("height");
let as_color = {
  "0": "#87CEEB",
  "1": "#FFC0CB",
  "2": "#FF1493",
  "-1": "#90EE90",
  "-2": "#008000",
}

svg.append('defs').append('marker')
    .attrs({'id':'arrowhead',
        'viewBox':'-0 -5 10 10',
        'refX':20,
        'refY':0,
        'orient':'auto',
        'markerWidth':5,
        'markerHeight':5,
        'xoverflow':'visible'})
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#888')
    .style('stroke','none')
    .style("stroke-opacity", 0.7);

svg.append('defs').append('marker')
    .attrs({'id':'arrowhead2',
        'viewBox':'-0 -5 10 10',
        'refX':-10,
        'refY':0,
        'orient':'auto',
        'markerWidth':5,
        'markerHeight':5,
        'xoverflow':'visible'})
    .append('svg:path')
    .attr('d', 'M 0,0 L 10 ,-5 L 10,5')
    .attr('fill', '#888')
    .style('stroke','none')
    .style("stroke-opacity", 0.7);


function clear(){
  svg.selectAll("g").remove();
}

function draw_path(topo_json, start_asn, stop_asn){  
	var link = svg.append("g")
         .attr("class", "links")
      	.selectAll("line")
      	.data(topo_json.links)
      	.enter().append("line")	
          .attr("stroke-width", 1)
	        .attr('marker-end',function(d) { 
	          if (d.shangye == "P2C") return "";
	          else return 'url(#arrowhead)';
	          })
	        .attr("marker-start",function(d) { 
	          if (d.shangye == "C2P") return "";
	          else return 'url(#arrowhead2)';
	          })
	        .attr("id",function (d) {
	          return "as" + d.source + "as" + d.target;
	        });

	var node = svg.selectAll(".node")
        .data(topo_json.nodes)
        .enter().append("g")
          .attr("class", "node")
          .attr("id",function (d) {
            return "as" + d.asn;
          });
          
    node.append("circle")
        .attr("id",function (d) {
            return "" + d.asn;
        })
        // .attr("fill", function(d) { 
        //     return as_color[d.tier];
        // })
        // .attr("stroke","#666")
        // .attr("stroke-width","1px") color(d.group)
        .attr("fill","#87CEEB")
        // .attr("class","node2")
        .attr("r", function(d){
          return 4; // + Math.log(d.degree + 1);
        })
        .on("dblclick", function(d){
          d.fx = null;
          d.fy = null;
        })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("title")
        .text(function (d) {
          return "自治域号 : " + d.asn;
        })

    let nodes_num = topo_json.nodes.length;
    if (nodes_num < 100){
      node.append("text")
        .text(d => d.asn)
    }
        
    svg.select("#as"+start_asn).select("circle").attr("r", function(d){
      d.fx = 20;
      d.fy = height / 2;
      return 4;
    });

    svg.select("#as"+stop_asn).select("circle").attr("r", function(d){
      d.fx = width - 20;
      d.fy = height / 2;
      return 4;
    });

	let simulation = d3.forceSimulation()
        .force("link", d3.forceLink()
                        .id(function(d) { return d.asn; })                                             
                        .iterations(60)) //.distance(lisan).strength(1)distance(100).
        .force("charge", d3.forceManyBody().strength(- 50000 / nodes_num)) //.strength(- 50000 / nodes_num)  .distanceMax(300) - Math.pow(nodes_num, 1)
        .force("center", d3.forceCenter(width / 2, height / 2));

    simulation
            .nodes(topo_json.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(topo_json.links);

    function ticked() {
      	link.attr("x1", function(d) { return d.source.x; })
          	.attr("y1", function(d) { return d.source.y; })
          	.attr("x2", function(d) { return d.target.x; })
          	.attr("y2", function(d) { return d.target.y; });
      	node.selectAll("circle")
          	.attr("cx", function(d) { return d.x; })
          	.attr("cy", function(d) {  return d.y; });
        node.selectAll("text")
            .attr("x", function(d) { return d.x - 17; })
            .attr("y", function(d) { return d.y - 10; });
    }
    
    function dragstarted(d) {
        if (!d3.event.active) {
            simulation.alphaTarget(0.1).restart();       
        }        
    }

    function dragged(d) {
        if (d3.event.active) {
        	d.x = d3.event.x;
        	d.y = d3.event.y;
        	d.fx = d.x;
        	d.fy = d.y;
        }        
    }

    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = d.x;
      d.fy = d.y;    
    }
}

function draw_svg(data_json){
  clear();
  let start_asn = data_json.src;
  let stop_asn = data_json.dst;
  let nodes = [];
  let links = [];
  let path_data = data_json.path.split(" ");
  let link_num = (path_data.length - 1) / 2;
  for (let i=0;i<link_num;i+=2){
    nodes.push({"asn":path_data[i]});
    links.push({"source":path_data[i] , "target":path_data[i+2], "shangye": path_data[i+1]});
  }
  nodes.push({"asn":path_data[path_data.length - 1]});
  console.log({"nodes": nodes, "links": links});
}