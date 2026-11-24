/* DF-e Data Explorer — seleção hierárquica compartilhada (V2.3). Sem dependências externas. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.DfeSelection = factory();
})(typeof globalThis === 'object' ? globalThis : this, function () {
  'use strict';
  class HierarchicalSelection {
    constructor(nodes) {
      this.reset(nodes);
    }
    reset(nodes, selectedKeys) {
      this.nodes = (nodes || []).map(n => ({...n, key: String(n.key), group:String(n.group), id:String(n.id), parentRef:n.parentRef ?? n.parent ?? null}));
      this.map = new Map(this.nodes.map(n => [n.key,n]));
      this.groups = new Map();this.children = new Map();this.parent = new Map();
      const unique = new Map();const duplicates=new Set();
      for (const n of this.nodes) {if(unique.has(n.id)) duplicates.add(n.id);unique.set(n.id,n);if(!this.groups.has(n.group)) this.groups.set(n.group,[]);this.groups.get(n.group).push(n);}
      for (const n of this.nodes) {
        const p=unique.get(n.parentRef);
        // Só usar pais identificados sem ambiguidade, dentro do grupo, sem ciclos.
        if(p && !duplicates.has(n.parentRef) && p.key!==n.key && p.group===n.group) {
          this.parent.set(n.key,p.key);
          if(!this.children.has(p.key)) this.children.set(p.key,[]);
          this.children.get(p.key).push(n.key);
        }
      }
      this.selected=new Set(selectedKeys===undefined?this.nodes.map(n=>n.key):selectedKeys.filter(k=>this.map.has(k)));
    }
    descendants(key) {
      const acc=[],stack=[key],seen=new Set();
      while(stack.length){const k=stack.pop();if(seen.has(k)||!this.map.has(k))continue;seen.add(k);acc.push(k);for(const child of this.children.get(k)||[])stack.push(child);}
      return acc;
    }
    changeNode(key,checked) {for(const k of this.descendants(key))checked?this.selected.add(k):this.selected.delete(k);}
    changeGroup(group,checked) {for(const n of this.groups.get(group)||[])checked?this.selected.add(n.key):this.selected.delete(n.key);}
    all(checked){if(checked)this.selected=new Set(this.nodes.map(n=>n.key));else this.selected.clear();}
    stateKeys(keys){let amount=0;for(const k of keys)if(this.selected.has(k))amount++;return amount===0?'none':amount===keys.length?'all':'partial';}
    stateGroup(group){return this.stateKeys((this.groups.get(group)||[]).map(n=>n.key));}
    stateNode(key){return this.stateKeys(this.descendants(key));}
    ancestors(key){const arr=[],seen=new Set([key]);let cur=key;while(this.parent.has(cur)){cur=this.parent.get(cur);if(seen.has(cur))break;seen.add(cur);arr.unshift(cur);}return arr;}
    contextKeys(){const result=new Set(this.selected);for(const key of this.selected)for(const ancestor of this.ancestors(key))result.add(ancestor);return result;}
    count(){return this.selected.size;}
    countsByGroup(){const obj={};for(const [g,arr] of this.groups)obj[g]=arr.filter(n=>this.selected.has(n.key)).length;return obj;}
    orderedRows(){return this.nodes.filter(n=>this.selected.has(n.key));}
    // Grupo pode ter múltiplas raízes editoriais, sem inventar vínculo entre elas.
    tree(group){const list=this.groups.get(group)||[],roots=list.filter(n=>!this.parent.has(n.key));return roots.length?roots:list;}
  }
  return {HierarchicalSelection};
});
