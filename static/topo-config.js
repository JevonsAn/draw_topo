var labelType, useGradients, nativeTextSupport, animate;

(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport 
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
    if (!this.elem) 
      this.elem = document.getElementById('log');
    this.elem.innerHTML = text;
    this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};


function init(){
  // init data
  var json = mydata//[{'adjacencies': [{'nodeTo': 'host1', 'nodeFrom': 'host0', 'data': {}}, {'nodeTo': 'router0', 'nodeFrom': 'host0', 'data': {}}], 'data': {'$type': 'host', 'ip': '10.0.3.4/24'}, 'id': 'host0', 'name': 'host0'}, {'adjacencies': [{'nodeTo': 'router0', 'nodeFrom': 'host1', 'data': {}}], 'data': {'$type': 'host', 'ip': '10.0.3.3/24'}, 'id': 'host1', 'name': 'host1'}, {'adjacencies': [{'nodeTo': 'BGP-router0', 'nodeFrom': 'router0', 'data': {}}], 'data': {'$type': 'router', 'ASN': '10', 'ip': ['10.0.3.2/24', '10.0.1.3/29']}, 'id': 'router0', 'name': 'router0'}, {'adjacencies': [{'nodeTo': 'router1', 'nodeFrom': 'BGP-router0', 'data': {}}, {'nodeTo': 'BGP-router1', 'nodeFrom': 'BGP-router0', 'data': {}}], 'data': {'$type': 'BGP-router', 'ASN': '10', 'ip': ['10.0.1.2/29', '10.0.0.2/29', '10.0.2.2/29']}, 'id': 'BGP-router0', 'name': 'BGP-router0'}, {'adjacencies': [{'nodeTo': 'router2', 'nodeFrom': 'router1', 'data': {}}, {'nodeTo': 'router3', 'nodeFrom': 'router1', 'data': {}}], 'data': {'$type': 'router', 'ASN': '10', 'ip': ['10.0.2.3/29', '10.0.4.2/28']}, 'id': 'router1', 'name': 'router1'}, {'adjacencies': [{'nodeTo': 'router3', 'nodeFrom': 'router2', 'data': {}}, {'nodeTo': 'host3', 'nodeFrom': 'router2', 'data': {}}], 'data': {'$type': 'router', 'ASN': '10', 'ip': ['10.0.4.3/28', '10.0.5.2/24']}, 'id': 'router2', 'name': 'router2'}, {'adjacencies': [{'nodeTo': 'host2', 'nodeFrom': 'router3', 'data': {}}], 'data': {'$type': 'router', 'ASN': '10', 'ip': ['10.0.4.4/28', '10.0.6.2/24']}, 'id': 'router3', 'name': 'router3'}, {'adjacencies': [], 'data': {'$type': 'host', 'ip': '10.0.6.3/24'}, 'id': 'host2', 'name': 'host2'}, {'adjacencies': [], 'data': {'$type': 'host', 'ip': '10.0.5.3/24'}, 'id': 'host3', 'name': 'host3'}, {'adjacencies': [{'nodeTo': 'router4', 'nodeFrom': 'BGP-router1', 'data': {}}], 'data': {'$type': 'BGP-router', 'ASN': '100', 'ip': ['10.0.0.3/29', '100.0.0.2/29']}, 'id': 'BGP-router1', 'name': 'BGP-router1'}, {'adjacencies': [{'nodeTo': 'host4', 'nodeFrom': 'router4', 'data': {}}], 'data': {'$type': 'router', 'ASN': '100', 'ip': ['100.0.0.3/29', '100.0.1.2/24']}, 'id': 'router4', 'name': 'router4'}, {'adjacencies': [], 'data': {'$type': 'host', 'ip': '100.0.1.3/24'}, 'id': 'host4', 'name': 'host4'}]
  // init ForceDirected
  var fd = new $jit.ForceDirected({
    //id of the visualization container
    injectInto: 'infovis',

    // new Canvas("mycanvas", { 
    //   backgroundColor: "#fff" 

    // });
    //Enable zooming and panning
    //with scrolling and DnD
    Navigation: {
      enable: true,
      type: 'Native',
      //Enable panning events only if we're dragging the empty
      //canvas (and not a node).
      panning: 'avoid nodes',
      zooming: 25 //zoom speed. higher is more sensible
    },
    // Change node and edge styles such as
    // color and width.
    // These properties are also set per node
    // with dollar prefixed data-properties in the
    // JSON structure.
    Node: {
      overridable: true,
      dim: 7
    },
    Edge: {
      overridable: true,
      color: '#00BFFF',
      lineWidth: 1.2
    },
    // Add node events
    Events: {
      enable: true,
      type: 'Native',
      //Change cursor style when hovering a node
      onMouseEnter: function() {
        fd.canvas.getElement().style.cursor = 'move';
      },
      onMouseLeave: function() {
        fd.canvas.getElement().style.cursor = '';
      },
      //Update node positions when dragged
      onDragMove: function(node, eventInfo, e) {
        var pos = eventInfo.getPos();
        node.pos.setc(pos.x, pos.y);
        fd.plot();
      },
      //Implement the same handler for touchscreens
      onTouchMove: function(node, eventInfo, e) {
        $jit.util.event.stop(e); //stop default touchmove event
        this.onDragMove(node, eventInfo, e);
      }
    },
    //Number of iterations for the FD algorithm
    iterations: 80,
    //Edge length
    levelDistance: 130,
    // This method is only triggered
    // on label creation and only for DOM labels (not native canvas ones).
    onCreateLabel: function(domElement, node){
      // Create a 'name' and 'close' buttons and add them
      // to the main node label
      var nameContainer = document.createElement('span'),
          style = nameContainer.style;
      nameContainer.className = 'name';
      nameContainer.innerHTML = node.name;
      domElement.appendChild(nameContainer);
      style.fontSize = "1em";
      style.color = "#000";
      //Fade the node and its connections when
      //clicking the close button
      //closeButton.onclick = function() {
       // node.setData('alpha', 0, 'end');
       // node.eachAdjacency(function(adj) {
       //   adj.setData('alpha', 0, 'end');
       // });
       // fd.fx.animate({
       //   modes: ['node-property:alpha',
       //           'edge-property:alpha'],
       //   duration: 500
       // });
      //};
      //Toggle a node selection when clicking
      //its name. This is done by animating some
      //node styles like its dimension and the color
      //and lineWidth of its adjacencies.
      nameContainer.onclick = function() {
        //set final styles
        fd.graph.eachNode(function(n) {
          if(n.id != node.id) delete n.selected;
          n.setData('dim', 7, 'end');
          n.eachAdjacency(function(adj) {
            adj.setDataset('end', {
              lineWidth: 1.2,
              color: '#00BFFF'
            });
          });
        });
        if(!node.selected) {
          node.selected = true;
          node.setData('dim', 17, 'end');
          node.eachAdjacency(function(adj) {
            adj.setDataset('end', {
              lineWidth: 4,
              color: '#4682B4'
            });
          });
        } else {
          delete node.selected;
        }
        //trigger animation to final styles
        fd.fx.animate({
          modes: ['node-property:dim',
                  'edge-property:lineWidth:color'],
          duration: 500
        });
        // Build the right column relations list.
        // This is done by traversing the clicked node connections.
        var html = "<h4>" + node.name + "</h4><b> connections:</b><ul><li>",
            list = [];
        node.eachAdjacency(function(adj){
          if(adj.getData('alpha')) list.push(adj.nodeTo.name+":"+adj.data.weight);
        });
        //append connections information
        $jit.id('inner-details').innerHTML = html + list.join("</li><li>") + "</li></ul>";
      };
    },
    // Change node styles when DOM labels are placed
    // or moved.
    onPlaceLabel: function(domElement, node){
      var style = domElement.style;
      var left = parseInt(style.left);
      var top = parseInt(style.top);
      var w = domElement.offsetWidth;
      style.left = (left - w / 2) + 'px';
      style.top = (top + 10) + 'px';
      style.display = '';
    }
  });
  // load JSON data.
  fd.loadJSON(json);
  
  //compute positions incrementally and animate.
  fd.computeIncremental({
    iter: 40,
    property: 'end',
    onStep: function(perc){
      // Log.write(perc + '% loaded...');
    },
    onComplete: function(){
      // Log.write('done');
      fd.animate({
        modes: ['linear'],
        transition: $jit.Trans.Elastic.easeOut,
        duration: 2500
      });
    }
  });
  //end
}

//Custom node
$jit.ForceDirected.Plot.NodeTypes.implement({ 
  //// this node type is used for plotting resource types (web)
   'BGP-router': 
       { 'render': function(node, canvas) { 
           var ctx = canvas.getCtx(); 
           var img = new Image();
           var pos = node.getPos(); 
           img.src = 'static/assets/router1.png'; 
           //img.onload = function(){ 
               ctx.drawImage(img,pos.x-15, pos.y-15,30,30); 
           //} 
           //img.src = 'luyou.png'; 
       },
            'contains': 
            function(node, pos)
                    { 
                        var npos = node.pos.getc(true), 
                        dim = node.getData('dim'); 
                        return this.nodeHelper.square. contains(npos, pos, dim); 
                    } 
       },
       'router': 
       { 'render': function(node, canvas) { 
           var ctx = canvas.getCtx(); 
           var img = new Image();
           var pos = node.getPos(); 
           img.src = 'static/assets/router.png'; 
           //img.onload = function(){ 
               ctx.drawImage(img,pos.x-15, pos.y-15,30,30); 
           //} 
           //img.src = 'luyou.png'; 
       },
            'contains': 
            function(node, pos)
                    { 
                        var npos = node.pos.getc(true), 
                        dim = node.getData('dim'); 
                        return this.nodeHelper.square. contains(npos, pos, dim); 
                    } 
       },
       'switch': 
       { 'render': function(node, canvas) { 
           var ctx = canvas.getCtx(); 
           var img = new Image();
           var pos = node.getPos(); 
           img.src = 'static/assets/switch.png'; 
           //img.onload = function(){ 
               ctx.drawImage(img,pos.x-15, pos.y-15,30,30); 
           //} 
           //img.src = 'luyou.png'; 
       },
            'contains': 
            function(node, pos)
                    { 
                        var npos = node.pos.getc(true), 
                        dim = node.getData('dim'); 
                        return this.nodeHelper.square. contains(npos, pos, dim); 
                    } 
       },
       'host': 
       { 'render': function(node, canvas) { 
           var ctx = canvas.getCtx(); 
           var img = new Image();
           var pos = node.getPos(); 
           img.src = 'static/assets/host.png'; 
           //img.onload = function(){ 
               ctx.drawImage(img,pos.x-15, pos.y-15,30,30); 
           //} 
           //img.src = 'luyou.png'; 
       },
            'contains': 
            function(node, pos)
                    { 
                        var npos = node.pos.getc(true), 
                        dim = node.getData('dim'); 
                        return this.nodeHelper.square. contains(npos, pos, dim); 
                    } 
       }
}); 