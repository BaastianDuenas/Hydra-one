// Ejecutar con HYDRA_NODE_MODULES apuntando a un directorio que contenga sharp y playwright.
const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const base = process.env.HYDRA_NODE_MODULES;
if (!base) throw new Error('Definir HYDRA_NODE_MODULES para localizar sharp y playwright.');
const sharp = require(path.join(base, 'sharp'));
const {chromium} = require(path.join(base, 'playwright'));
(async () => {
  const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, 'catalogo.json'), 'utf8'));
  const executablePath = process.env.HYDRA_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
  const browser = await chromium.launch({headless:true, executablePath});
  const page = await browser.newPage();
  const results=[];
  try {
    for (const d of catalog) {
      const source=path.join(__dirname,'svg',d.slug+'.svg');
      await sharp(source,{density:144}).png().toFile(path.join(__dirname,'png',d.slug+'.png'));
      await page.goto(pathToFileURL(source).href);
      const check=await page.evaluate(() => {
        const svg=document.querySelector('svg');
        const vb=svg.viewBox.baseVal;
        const overflow=[...document.querySelectorAll('text')].filter(t=>{
          const b=t.getBBox();return b.x<0||b.y<0||b.x+b.width>vb.width||b.y+b.height>vb.height;
        }).map(t=>t.textContent);
        return {textCount:document.querySelectorAll('text').length,overflow};
      });
      results.push({diagram:d.slug,pngWidth:d.width*2,pngHeight:d.height*2,...check});
    }
    fs.writeFileSync(path.join(__dirname,'verificacion.json'),JSON.stringify({date:'2026-10-28',scope:'Exportación y límites de texto de los diagramas; no pruebas funcionales ni conexión remota',results},null,2));
    if(results.some(r=>r.overflow.length)) throw new Error('Texto fuera de límites; consultar verificacion.json');
    console.log(`Verificados ${results.length} diagramas; PNG a doble resolución; texto dentro del lienzo.`);
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
