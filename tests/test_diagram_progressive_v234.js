'use strict';const assert=require('node:assert/strict');const {DiagramState}=require('../public/diagram-state.js');
const nodes=[{id:'ROOT',key:'ROOT',group:'A',parentRef:null},{id:'A01',key:'A01',group:'A',parentRef:'ROOT'},
{id:'W01',key:'W01',group:'W',parentRef:'A01'}, {id:'W34',key:'W34',group:'W',parentRef:'W01'},
{id:'W36',key:'W36',group:'W',parentRef:'W34'},{id:'W37',key:'W37',group:'W',parentRef:'W36'},
{id:'W38',key:'W38',group:'W',parentRef:'W37'}, {id:'W42',key:'W42',group:'W',parentRef:'W36'},
{id:'B01',key:'B01',group:'B',parentRef:'A01'}];
const g=new DiagramState(nodes);const ids=(group,full=false)=>g.visible(group,'',full).map(x=>x.n.id);
assert.deepEqual(ids('__ALL__'),['ROOT','A01','W01','B01']);
assert.deepEqual(ids('W'),['W01']);g.toggle('W01');assert.deepEqual(ids('W'),['W01','W34']);g.toggle('W34');g.toggle('W36');
assert.deepEqual(ids('W'),['W01','W34','W36','W37','W42']);g.toggle('W37');assert.deepEqual(ids('W'),['W01','W34','W36','W37','W38','W42']);
g.toggle('W36');assert.deepEqual(ids('W'),['W01','W34','W36']);assert.equal(g.open.has('W37'),true,'colapsar pai preserva intenção de expansão interna');
g.toggle('W36');assert.equal(ids('W').includes('W38'),true);g.expandAll();assert.deepEqual(ids('W',true),ids('W'));
g.collapseAll();assert.deepEqual(ids('W'),['W01']);assert.equal(ids('W',true).length,6);
g.reveal('W38');assert.equal(ids('W').includes('W38'),true);
console.log('PASS: raiz, expandir independente, recolher pai, expansão completa, profundidade livre, revelar pesquisa');
