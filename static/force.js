// const d3 = require("d3.js");
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

let asinfo_vm = new Vue({
  el: '#info',
  data: {
    asInfos: [
      {
        name: "自治域号 : ",
        info: " "
      },
      {
        name: "自治域名称 : ",
        info: " "
      },
      {
        name: "所属国家 : ",
        info: " "
      },
      {
        name: "节点度 : ",
        info: " "
      },
    ]    
  },
  methods: {
    
  }
})

let legend_vm = new Vue({
  el: '#legend',
  data: {
    divwidth: 50,
    divheight:20, 
    legends: [
      {
        name: "自己和peer : ",
        color: as_color["0"]
      },
      {
        name: "第一层provider : ",
        color: as_color["1"]
      },
      {
        name: "第二层provider : ",
        color: as_color["2"]
      },
      {
        name: "第一层customer : ",
        color: as_color["-1"]
      },
      {
        name: "第二层customer : ",
        color: as_color["-2"]
      },
    ]  
  },
  methods: {
  }
})

function clear(){
  svg.selectAll("g").remove();
  svg.attr("width", 700)
    .attr("height", 700);
  // svg.selectAll(".links").remove();
}

function draw_topo(topo_json, center_asn){  
	var link = svg.append("g")
         .attr("class", "links")
      	.selectAll("line")
      	.data(topo_json.links)
      	.enter().append("line")	
          .attr("stroke-width", d => Math.max(Math.min(4, 0.7* Math.sqrt(0.4*d.value)), 0.6))
          .attr("value", d=>d.value)
	        // .attr('marker-end',function(d) { 
	        //   if (d.shangye == "P2C") return "";
	        //   else return 'url(#arrowhead)';
	        //   })
	        // .attr("marker-start",function(d) { 
	        //   if (d.shangye == "C2P") return "";
	        //   else return 'url(#arrowhead2)';
	        //   })
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
        .attr("fill", function(d) { 
            return as_color[d.tier];
        })
        // .attr("stroke","#666")
        // .attr("stroke-width","1px") color(d.group)
        // .attr("fill","#87CEEB")
        .attr("class","node2")
        .attr("r", function(d){
          return 4 + Math.log(d.degree + 1);
        })
        .on("click", function(d){
          asinfo_vm.asInfos[0].info  = d.asn;
          asinfo_vm.asInfos[1].info = d.asname;
          asinfo_vm.asInfos[2].info = d.country;
          asinfo_vm.asInfos[3].info = d.degree;
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
          return "自治域号 : " + d.asn + "\n" +
          "自治域名称 : " + d.asname + "\n" +
          "所属国家 : " + d.country + "\n" +
          // "图中节点度 : " + d.linknum + "\n" +
          "节点度 : " + d.degree;
        })

    let nodes_num = topo_json.nodes.length;
    if (nodes_num < 100){
      node.append("text")
        .text(d => d.asn)
    }
        
    svg.select("#as"+center_asn).select("circle").attr("r", function(d){
      d.fx = width / 2;
      d.fy = height / 2;
      return 4 + Math.log(d.degree + 1);
    });

    function calc_strength(degree1, degree2, linknum1, linknum2){
      // if (degree1>100) degree1=100;
      // if (degree2>100) degree2=100;
      let t1 = 1 + Math.log(degree1 + 1);
      let t2 = 1 + Math.log(degree2 + 1);
      return 1 / (t1 + t2 + Math.min(linknum1, linknum2));
    }

    function calc_charge(){
      if (nodes_num>=300)
        return -300;
      else if (nodes_num<20)
        return -10;
      else
        return -30;
    }

	let simulation = d3.forceSimulation()
        .force("link", d3.forceLink()
                        .id(function(d) { return d.asn; })
                        .strength(function(d) {                          
                           return calc_strength(d.source.degree, d.target.degree, d.source.linknum, d.target.linknum);
                         })                     
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
           // d.fx = d3.event.x;
           // d.fy = d3.event.y;
        }        
    }

    function dragended(d) {
	    // d.fx = null;
     //  d.fy = null;
      if (!d3.event.active) simulation.alphaTarget(0);
      // else{
      //   d.fx = d.x;
      //   d.fy = d.y;
      // }
      d.fx = d.x;
      d.fy = d.y;  
      // simulation.stop().tick(60);//iterations(60).stop();    
    }
}