const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const root=path.resolve(__dirname,'../../assets/brand/nexo-logo-v1');
fs.mkdirSync(root,{recursive:true});
// Geometric reconstruction from the original orange angular mark and lowercase lettering.
// All letters are closed vector paths: no fonts, embedded bitmaps or external resources.
const symbol='M 20 20 Q 25 15 30 20 L 111 98 Q 113 100 113 103 L 113 116 Q 113 120 109 120 L 98 120 Q 95 120 93 118 L 64 89 L 35 118 Q 32 121 28 121 L 22 121 Q 17 121 17 116 L 17 106 Q 17 103 20 100 L 49 71 L 20 42 Q 17 39 17 35 L 17 25 Q 17 22 20 20 Z';
const letters=[
// n
'M 151 47 L 171 47 L 171 56 C 177 48 186 44 196 44 C 216 44 226 57 226 78 L 226 120 L 205 120 L 205 81 C 205 68 200 62 190 62 C 179 62 172 70 172 82 L 172 120 L 151 120 Z',
// e, bowl and opening are one continuous outline; counter is a separate closed path.
'M 310 89 L 254 89 C 256 100 263 106 274 106 C 282 106 288 103 292 97 L 312 97 C 306 114 293 123 274 123 C 249 123 232 108 232 84 C 232 60 249 44 273 44 C 297 44 313 60 313 83 L 313 89 Z M 254 75 L 292 75 C 290 65 283 60 273 60 C 264 60 257 66 254 75 Z',
// x
'M 317 47 L 341 47 L 358 71 L 374 47 L 398 47 L 370 83 L 400 120 L 375 120 L 357 95 L 340 120 L 315 120 L 345 83 Z',
// o
'M 444 44 C 469 44 486 60 486 84 C 486 108 469 123 444 123 C 419 123 402 108 402 84 C 402 60 419 44 444 44 Z M 444 62 C 431 62 423 70 423 84 C 423 98 431 105 444 105 C 457 105 465 98 465 84 C 465 70 457 62 444 62 Z'
];
function svg(mark,word,icon=false){return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${icon?'0 0 132 140':'0 0 510 140'}" role="img" aria-labelledby="title"><title id="title">${icon?'Símbolo NEXO':'NEXO'}</title><path fill="${mark}" d="${symbol}"/>${icon?'':letters.map(d=>`<path fill="${word}" fill-rule="evenodd" d="${d}"/>`).join('')}</svg>`;}
const variants=[['nexo-principal','#FF850D','#FFFFFF'],['nexo-fundo-claro','#FF850D','#111315'],['nexo-monocromatico-branco','#FFFFFF','#FFFFFF'],['nexo-monocromatico-grafite','#111315','#111315']];
(async()=>{
 for(const [name,a,b] of variants){const src=svg(a,b);fs.writeFileSync(path.join(root,name+'.svg'),src);await sharp(Buffer.from(src)).resize({width:4096}).png().toFile(path.join(root,name+'-4096.png'));}
 for(const [name,color] of [['nexo-simbolo','#FF850D'],['nexo-simbolo-branco','#FFFFFF'],['nexo-simbolo-grafite','#111315']]){const src=svg(color,color,true);fs.writeFileSync(path.join(root,name+'.svg'),src);await sharp(Buffer.from(src)).resize({width:2048}).png().toFile(path.join(root,name+'-2048.png'));}
 const panels=[];
 for(let i=0;i<4;i++){const [name,a,b]=variants[i];const logo=await sharp(Buffer.from(svg(a,b))).resize({width:510}).png().toBuffer();const panel=await sharp({create:{width:640,height:240,channels:4,background:i%2?'#F3EFE9':'#111315'}}).composite([{input:logo,left:65,top:50}]).png().toBuffer();panels.push({input:panel,left:(i%2)*640,top:Math.floor(i/2)*240});}
 await sharp({create:{width:1280,height:480,channels:4,background:'#111315'}}).composite(panels).png().toFile(path.join(root,'NEXO-logo-variantes.png'));
 const preview=svg('#FF850D','#FFFFFF').replace('<path fill=', '<rect width="510" height="140" fill="#111315"/><path fill=');
 await sharp(Buffer.from(preview)).resize({width:1530}).png().toFile(path.join(root,'NEXO-logo-preview.png'));
 fs.writeFileSync(path.join(root,'LEIA-ME.txt'),'NEXO - LOGO VETORIAL v1\n\nReconstrução geométrica baseada no recorte original e na referência de briefing. É uma reconstrução, não o arquivo vetorial original.\n\nSVG: arquivo mestre, formas vetoriais fechadas, sem dependência de fontes, sem imagens embutidas e com fundo transparente. Escala sem pixelar.\nPNG: versões transparentes em 4096 px (assinaturas) e 2048 px (símbolos). Não ampliar além da resolução exportada; para novos tamanhos exportar do SVG.\n\nPrincipal: laranja #FF850D + branco #FFFFFF, para fundo grafite.\nFundo claro: laranja + grafite #111315.\nMonocromáticos: branco ou grafite.\n\nÁrea de proteção mínima: metade da altura do símbolo em cada lado. Não esticar, inclinar, adicionar brilho ou alterar as proporções. Para favicon e avatares usar símbolo isolado e verificar em 16/24/32 px.\n\nAs imagens preview e variantes têm fundo apenas para demonstração. Os demais SVGs e PNGs são transparentes.\nArquivos criados localmente; não publicados no GitHub.\n','utf8');
 console.log(root);
})();
