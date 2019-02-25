let data2 = [
  {"name": "Eve",   "parent": ""},
  {"name": "Cain",  "parent": ""},
  {"name": "Seth",  "parent": ""},
  {"name": "Enos",  "parent": "Seth"},
  {"name": "Noam",  "parent": "Seth"},
  {"name": "Abel",  "parent": "Eve"},
  {"name": "Awan",  "parent": "Eve"},
  {"name": "Enoch", "parent": "Awan"},
  {"name": "Azura", "parent": "Eve"}
];

function draw_tree2(root, direction, transx){

	const g = svg.append("g")
	  .attr("font-family", "sans-serif")
	  .attr("font-size", 10)
	  .attr("transform", `translate(${width / 2},${transx})`);

	const link = g.append("g")
	.attr("fill", "none")
	.attr("stroke", "#555")
	.attr("stroke-opacity", 0.4)
	.attr("stroke-width", 1.5)
	.selectAll("path")
	.data(root.links())
	  .enter()
	  .append("path")
	  .attr("d", d3.linkHorizontal()
	      .x(d => direction * d.y)
	      .y(d => d.x));

	const node = g.append("g")
	  .attr("stroke-linejoin", "round")
	  .attr("stroke-width", 3)
	.selectAll("g")
	.data(root.descendants().reverse())
	  .enter()
	  .append("g")
	  .attr("transform", d => `translate(${direction * d.y},${d.x})`);

	// .join("g")
	//   .attr("transform", d => `translate(${d.y},${d.x})`);

	node.append("circle")
	  .attr("fill", function(d) { 
          return as_color[d.data.tier];
      })
      .attr("class","node2")
      .attr("r", function(d){
        // console.log(d);
        return 4 + Math.log(d.data.degree + 1);
      })
      .on("click", function(d){
          asinfo_vm.asInfos[0].info  = d.data.asn;
          asinfo_vm.asInfos[1].info = d.data.asname;
          asinfo_vm.asInfos[2].info = d.data.country;
          asinfo_vm.asInfos[3].info = d.data.degree;
        });
	  // .attr("fill", d => d.children ? "#555" : "#999")
	  // .attr("r", 2.5);

	node.append("text")
	  .attr("dy", function(d){
	  	if (d.data.tier == 0)
	  		return -10;
	  	else
	  		return `0.31em`;
	  })
	  .style("font-size", d => `${10 + Math.log(d.data.degree + 1)}px`)
	  .attr("x", function(d){
	  	if (d.data.tier == 0)
	  		return -17;
	  	else if (d.children)
	  		return direction * -6;
	  	else
	  		return direction * 6;
	  })
	  .attr("text-anchor", function(d){
	  	if (d.data.tier == 0)
	  		return "center";
	  	else if (direction==1){
	  		return d.children ? "end" : "start";
	  	}
	  	else{
	  		return d.children ? "start" : "end";
	  	}
	  })
	  .text(d => d.data.name);
	// .clone(true).lower()
	//   .attr("stroke", "white");
}
function draw2tree(now_json){
	// let max_pointnum = now_json["customers"].length >= now_json["providers"].length ? now_json["customers"].length : now_json["providers"].length;
	// let dx = 700 * 2 / max_pointnum;
	let root1 = d3.stratify()
	    .id(function(d) { return d.name; })
	    .parentId(function(d) { return d.parent; })
	    (now_json["customers"]);

	let start_size_y = 480;
	let leftx1 = 0;
	let rightx1 = 0;

	// if (now_json["customers"].length){
		root1.dx = start_size_y * 2 / now_json["customers"].length;
		root1.dy = width / (root1.height + 1) / 2;
		root1 = d3.tree().nodeSize([root1.dx, root1.dy])(root1);

		let left = root1;
		  let right = root1;
		  root1.eachBefore(node => {
		    if (node.x < left.x) left = node;
		    if (node.x > right.x) right = node;
		  });
		leftx1 = left.x;
		rightx1 = right.x;
	// }
	// let height1 = right.x - left.x + 30;

	let leftx2 = 0;
	let rightx2 = 0;
	// if (now_json["providers"].length){
		let root2 = d3.stratify()
		    .id(function(d) { return d.name; })
		    .parentId(function(d) { return d.parent; })
		    (now_json["providers"]);

		root2.dx = start_size_y * 2 / now_json["providers"].length;
		root2.dy = width / (root2.height + 1) / 2;
		root2 = d3.tree().nodeSize([root2.dx, root2.dy])(root2);

		left = root2;
		right = root2;
		  root2.eachBefore(node => {
		    if (node.x < left.x) left = node;
		    if (node.x > right.x) right = node;
		  });
		leftx2 = left.x;
		rightx2 = right.x;
	// }
	// let height2 = right.x - left.x + 30;

	let height = 30;
	let transx = 0;

	if (-leftx1 >= -leftx2){
		height += -leftx1;		
		transx = 15 - leftx1;		
	}
	else{
		height += -leftx2;
		transx = 15 - leftx2;
	}

	if (rightx1 >= rightx2){
		height += rightx1;		
	}
	else{
		height += rightx2;
	}
	// console.log
	svg.attr("height", height);
	draw_tree2(root1, -1, transx);
    draw_tree2(root2, 1, transx);
}