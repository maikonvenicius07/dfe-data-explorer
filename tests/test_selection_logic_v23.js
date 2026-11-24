const assert=require('node:assert/strict');
const {HierarchicalSelection}=require('../public/selection.js');
const nodes=[
 {id:'W01',key:'W01',group:'W',parentRef:'A01'},
 {id:'W02',key:'W02',group:'W',parentRef:'W01'},
 {id:'W03',key:'W03',group:'W',parentRef:'W02'},
 {id:'W04',key:'W04',group:'W',parentRef:'W02'},
 {id:'W34',key:'W34',group:'W',parentRef:'W01'},
 {id:'W36',key:'W36',group:'W',parentRef:'W34'},
 {id:'W38',key:'W38',group:'W',parentRef:'W36'},
 {id:'B01',key:'B01',group:'B',parentRef:'A01'},
 {id:'B02',key:'B02',group:'B',parentRef:'B01'},
];
const s=new HierarchicalSelection(nodes);
assert.equal(s.count(),0);
s.all(false);assert.equal(s.count(),0);assert.equal(s.stateGroup('W'),'none');
s.changeKeys(['W02'],true);assert.deepEqual([...s.selected],['W02'],'Selecionar campo individual não pode selecionar filhos');
s.changeKeys(['W02'],false);assert.equal(s.count(),0);
s.changeKeys(['B02','W38'],true);assert.equal(s.count(),2,'Seleções de grupos diferentes devem acumular');
s.changeKeys(['B02'],false);assert.deepEqual([...s.selected],['W38']);
s.all(false);
s.changeNode('W02',true);assert.deepEqual([...s.selected].sort(),['W02','W03','W04']);
assert.equal(s.stateGroup('W'),'partial');
s.changeNode('W02',false);assert.equal(s.count(),0);
s.changeNode('W38',true);assert.equal(s.count(),1);
assert.deepEqual([...s.contextKeys()].sort(),['W01','W34','W36','W38']);
s.changeGroup('B',true);assert.equal(s.count(),3);assert.equal(s.stateGroup('B'),'all');
s.reset(nodes,['W38','B02']);assert.equal(s.count(),2);assert.deepEqual(s.ancestors('W38'),['W01','W34','W36']);
// IDs duplicados não criam um pai arbitrário.
const dup=new HierarchicalSelection([{id:'X',key:'X1',group:'W'},{id:'X',key:'X2',group:'W'},{id:'Y',key:'Y',group:'W',parentRef:'X'}]);
assert.equal(dup.ancestors('Y').length,0);
console.log('PASS: seleção parcial, todos os grupos, descendentes, contextos, carga e IDs duplicados');
