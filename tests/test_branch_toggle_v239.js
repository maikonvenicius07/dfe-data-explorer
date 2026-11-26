'use strict';
const assert=require('node:assert/strict');
const {HierarchicalSelection}=require('../public/selection.js');
const nodes=[
 {key:'root',id:'root',group:'A'},
 {key:'parent',id:'parent',parentRef:'root',group:'W'},
 {key:'child',id:'child',parentRef:'parent',group:'W'},
 {key:'grandchild',id:'grandchild',parentRef:'child',group:'W03'},
 {key:'other',id:'other',parentRef:'root',group:'B'}
];
const s=new HierarchicalSelection(nodes);
s.changeKeys(['other'],true);
assert.equal(s.toggleNode('parent'),true);
assert.equal(s.stateNode('parent'),'all');
assert.deepEqual([...s.selected].sort(),['child','grandchild','other','parent']);
assert.equal(s.toggleNode('parent'),false);
assert.deepEqual([...s.selected],['other']);
s.changeKeys(['child'],true);
assert.equal(s.stateNode('parent'),'partial');
assert.equal(s.toggleNode('parent'),true);
assert.equal(s.stateNode('parent'),'all');
assert.equal(s.toggleNode('child'),false);
assert(s.selected.has('parent'));
assert(!s.selected.has('grandchild'));
assert(s.selected.has('other'));
assert.equal(s.toggleNode('missing'),false);
assert.equal(s.count(),2);
console.log('PASS V2.3.9: marcar, desmarcar, parcial, descendentes profundos, seleção independente.');
