// Code goes here

function exportToCsv() {
  var myCsv = "Col1,Col2,Col3\nval1,val2,val3";

  var myCsv = cy.json();

  window.open('data:text/csv;charset=utf-8,' + escape(myCsv));
}

//var button = document.getElementById('b');
//button.addEventListener('click', exportToCsv);


var cy = cytoscape({
  container: document.getElementById('cy'), // container to render in

  elements: { // list of graph elements to start with
    nodes: [{ // node a
      data: {
        id: 'ACC_PROD_ADMIN',
        style: {
          'shape': 'dimond'},
        actor: '#34d5eb'
      }
    }, { // node b
      data: {
        id: 'ACC_PROD_DEVOPS',
        actor: 'orange'
      }
    },
    { // node b
      data: {
        id: 'TEST11',
        actor: 'orange'
      }
    },
    { // node b
      data: {
        id: 'TEST22',
        actor: 'orange'
      }
    },
    { // node b
      data: {
        id: 'PROD_DB.MAIN_SCHEMA',
        actor: 'orange'
      }
    }, {
      data: {
        id: 'ACC_PROD_ANALYST',
        actor: '#34d5eb'
      }
    },{
      data: {
        id: 'FN_DEV_MANAGER',
        actor: '#34d500'
      }
    }, {
      data: {
        id: 'FN_PROD_MANAGER',
        actor: '#34d500'
      }
    }, {
      data: {
        id: 'ACC_DEV_DEVELOPER',
        actor: '#34d5eb'
      }
    }, {
      data: {
        id: 'PROD_DB.FED_SCHEMA',
        actor: 'orange'
      }
    },{
      data: {
        id: 'TEST_DB.FED_SCHEMA',
        actor: 'orange'
      }
    }, {
      data: {
        id: 'SYSADMIN',
        actor: 'red'
      }
    }, {
      data: {
        id: 'ACC_DEV_ADMIN',
        actor: '#34d5eb'
      }
    }],
    edges: [{ // edge ab
      data: {
        id: 'ab',
        source: 'ACC_PROD_ANALYST',
        target: 'PROD_DB.MAIN_SCHEMA',
        label: 'R'
      }
    }, {
      data: {
        id: 'bd',
        source: 'ACC_PROD_ADMIN',
        target: 'SYSADMIN',
        label: ''
      }
    }, 
    {
      data: {
        id: 'bd2',
        source: 'ACC_PROD_ANALYST',
        target: 'SYSADMIN',
        label: ''
      }
    },  {
      data: {
        id: 'df',
        source: 'ACC_PROD_ANALYST',
        target: 'PROD_DB.FED_SCHEMA',
        label: 'R'
      }
    }, {
      data: {
        id: 'dg',
        source: 'ACC_DEV_DEVELOPER',
        target: 'TEST_DB.FED_SCHEMA',
        label: 'RWO'
      }
    },{
      data: {
        id: 'dg1',
        source: 'ACC_DEV_DEVELOPER',
        target: 'FN_DEV_MANAGER'
      }
    }, {
      data: {
        id: 'dg2',
        source: 'FN_DEV_MANAGER',
        target: 'SYSADMIN'
      }
    }, {
      data: {
        id: 'dg3',
        source: 'ACC_DEV_ADMIN',
        target: 'SYSADMIN'
      }
    },{
      data: {
        id: 'fe',
        source: 'ACC_PROD_DEVOPS',
        target: 'PROD_DB.FED_SCHEMA',
        label: 'R'
      }
    }]
  },

  ready: function(e) {
    console.info("cytoscape is ready");
  },
  minZoom: 1e-5,
  maxZoom: 1e5,
  wheelSensitivity: 0.5,
  style: [ // the stylesheet for the graph
    {
      selector: 'node',
      style: {
        'shape': 'roundrectangle',
        'background-color': 'orange',
        'background-color':'data(actor)',
        'border-color': '#888',
        'shape ': 'roundrectangle',
        'width': 'label',
        'height': 'label',
        'padding-right': '3',
        'padding-left': '3',
        'padding-top': '3',
        'padding-bottom': '3',
        'text-wrap': 'wrap',
        'text-valign': 'center',
        'text-halign': 'center',
        'text-max-width': '100px',
        'label': 'data(id)',
        'font-size': '10'
      },
    }, {
      selector: 'edge',
      style: {
        'label': 'data(label)',
        'width': 3,
        'line-color': '#1100cc',
        'target-arrow-color': '#1100cc',
        'target-arrow-shape': 'triangle'
      }
    }
  ],
  layout: {
    name: 'grid',
    rows: 2
  }
});

var options = {
  name: 'cose',
  // Called on `layoutready`
  ready: function() {},
  // Called on `layoutstop`
  stop: function() {},
  // Whether to animate while running the layout
  animate: true,
  // The layout animates only after this many milliseconds
  // (prevents flashing on fast runs)
  animationThreshold: 250,
  // Number of iterations between consecutive screen positions update
  // (0 -> only updated on the end)
  refresh: 20,
  // Whether to fit the network view after when done
  fit: true,
  // Padding on fit
  padding: 30,
  // Constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  boundingBox: undefined,
  // Extra spacing between components in non-compound graphs
  componentSpacing: 100,
  // Node repulsion (non overlapping) multiplier
  nodeRepulsion: function(node) {
    return 400000;
  },
  // Node repulsion (overlapping) multiplier
  nodeOverlap: 10,
  // Ideal edge (non nested) length
  idealEdgeLength: function(edge) {
    return 10;
  },
  // Divisor to compute edge forces
  edgeElasticity: function(edge) {
    return 100;
  },
  // Nesting factor (multiplier) to compute ideal edge length for nested edges
  nestingFactor: 5,
  // Gravity force (constant)
  gravity: 80,
  // Maximum number of iterations to perform
  numIter: 1000,
  // Initial temperature (maximum node displacement)
  initialTemp: 200,
  // Cooling factor (how the temperature is reduced between consecutive iterations
  coolingFactor: 0.95,
  // Lower temperature threshold (below this point the layout will end)
  minTemp: 1.0,
  // Whether to use threading to speed up the layout
  useMultitasking: true
};

cy.layout(options);

cy.on('click', 'node', function(evt) {
  console.log('clicked ' + this.id());
  //console.log( cy.elements.node.position() );
  //console.log(cy.elements().jsons());
  //console.log(cy.edges().jsons());
});

cy.on('click', 'edge', function(evt) {
  console.log('clicked N:' + this.id());
  //console.log( cy.json() );
  //console.log(cy.elements().jsons());
  //console.log(cy.edges().jsons());
});

var destroy = function() {
  cy.destroy();
}

var layoutOpts = {
  name: 'cola',
  refresh: 2,
  edgeLength: 200,
  fit: false
}


function refreshLayout() {
  layout.stop();
  layout = cy.elements().makeLayout(layoutOpts);
  layout.run();
}

var addSchema = function() {
  //var elem_id = document.getElementById('node_id').value;
  //var from_node = document.getElementById('from_node').value;
  //if (elem_id.length === 0 || from_node.length === 0) {
    //alert("please fill both input fields");
    //return;
  //}

  for (var i = 0; i < 10; i++) {
    cy.add({
        data: { id: 'node' + i }
        }
    );
    var source = 'node' + i;
    cy.add({
        data: {
            id: 'edge' + i,
            source: source,
            target: (i % 2 == 0 ? 'a' : 'b')
        }
    });
}

  /* */
  var eles = cy.add([
    { group: 'nodes', data: { id: 'TEST112' }, position: { x: 100, y: 100 } },
    { group: 'nodes', data: { id: 'TEST22' }, position: { x: 200, y: 200 } }
  ]);
  

  //var elem_id = document.getElementById('node_id').value;
  //console.log(elem_id);

  //var nodesArray = [ { group: "nodes", x: 10, y: 35 },
  //                 { group: "nodes", x: 20, y: 70 } ];
  //var nodes = cy.addElements(nodesArray, true);
/* 
  var node1 = {
    group: "nodes",
    shape: "ellipse",
    size: 20,
    color: "0000ff",
    // etc...
    data: {
        id: 1
    }
};

cy.add(node1);


  var elements = cy.add({
    classes: 'eh-handle',
      position: { // the model position of the node (optional on init, mandatory after)
        x: 100,
        y: 100
      },
      grabbable: false,
      selectable: false,
      data: {label: 'dds'},
    group: 'nodes',
    data: { id: 'c1' }
  });
  
  cy.add({
    id: elem_id,
    group: 'nodes',
    data: { weight: 75 }
    ,position: { x: 200, y: 200 
    }
});*/
  //cy.layout(options);
  //refreshLayout();
  

};

var addNodeEdge = function() {
  var elem_id = document.getElementById('node_id').value;
  var from_node = document.getElementById('from_node').value;
  if (elem_id.length === 0 || from_node.length === 0) {
    alert("please fill both input fields");
    return;
  }
  cy.add([{
      data: {
        id: elem_id
      }
    }, {
      data: {
        id: from_node + '' + elem_id,
        source: from_node + '',
        target: elem_id + ''

      }
    }
  ]);
  cy.layout(options);

  function download1( name, type) {
  var a = document.getElementById("a");
  var file = new Blob([JSON.stringify(cy.json())], {type: type});
  a.href = URL.createObjectURL(file);
  a.download = name;
}

};

function download(name, type) {
  var a = document.getElementById("a");
  var file = new Blob([JSON.stringify(cy.json())], {type: type});
  a.href = URL.createObjectURL(file);
  a.download = name;
  //console.log(cy.elements().jsons());
  //console.log(cy.edges().jsons());
};
