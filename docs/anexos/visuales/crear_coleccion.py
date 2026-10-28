"""Construye el índice y las explicaciones; no genera ni modifica las imágenes."""
from pathlib import Path
from html import escape as h
import json
import struct
import zipfile

p=Path(__file__).resolve().parent
items=json.loads((p/'catalogo-ampliado.json').read_text(encoding='utf-8'))
intro=[
 dict(slug='01-arquitectura',title='Vista general del sistema',state='Introducción',read='El usuario interactúa con React; FastAPI procesa las solicitudes y PostgreSQL conserva los registros. Los cuatro iconos inferiores son módulos del mismo backend.',example='La pantalla pide, el backend procesa y la base de datos conserva.'),
 dict(slug='02-datos',title='Relaciones en una mirada',state='Introducción',read='Un activo puede tener cero o muchas mantenciones. Los repuestos todavía no están vinculados al consumo de una mantención.',example='Las tarjetas representan varios registros posibles, no una cantidad fija de tres.'),
 dict(slug='03-proceso',title='Registrar una mantención',state='Actual · recorrido resumido',read='Se elige un activo, se rellena el formulario, se validan los datos y se comprueba la existencia del activo antes de guardar. Datos inválidos pueden producir 422; activo inexistente, 404; alta correcta, 201.',example='Completar el formulario no significa cerrar una mantención. El stock permanece igual.')
]
all_items=intro+items
nav=''.join(f'<a href="#{s["slug"]}"><b>{s["slug"][:2]}</b> {h(s["title"])}</a>' for s in all_items)
cards=[]
fields=[('read','Cómo leerlo'),('example','Ejemplo para explicarlo'),('defense','Pregunta de defensa'),('limit','Alcance y límites'),('sources','Fuentes')]
for s in all_items:
    details=''.join(f'<div><h3>{title}</h3><p>{h(s[key])}</p></div>' for key,title in fields if s.get(key))
    cards.append(f'<section id="{s["slug"]}"><div class="section-head"><h2>{h(s["title"])}</h2><span>{h(s["state"])}</span></div><a href="{s["slug"]}.png" target="_blank"><img loading="lazy" src="{s["slug"]}.png" alt="{h(s["title"])}"></a><div class="actions"><a href="{s["slug"]}.png" download>Descargar imagen</a></div><details><summary>Entender y explicar este mapa</summary>{details}</details></section>')
html='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hydra-One · Colección visual completa</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f6f8fb;color:#183148;font:16px/1.65 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:28px}h1{font-size:clamp(26px,4vw,40px);line-height:1.2}header p{max-width:900px;color:#52667b}a{color:#087f8c;text-underline-offset:4px}nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:9px;margin:25px 0}nav a{background:white;border:1px solid #dbe4ec;border-radius:9px;padding:10px;text-decoration:none;font-size:14px}nav b{color:#d56b21;margin-right:8px}section{scroll-margin-top:15px;background:white;border-radius:16px;margin-bottom:42px;overflow:hidden;border:1px solid #dbe4ec}.section-head{padding:22px 28px 0;display:flex;justify-content:space-between;gap:16px;align-items:center}.section-head h2{font-size:22px;margin:0}.section-head span{font-size:12px;color:#516a7d}img{width:100%;height:auto;display:block}.actions{padding:0 28px 18px;font-size:14px}details{border-top:1px solid #dbe4ec;padding:20px 28px;background:#f4f8fa}summary{cursor:pointer;color:#087f8c;font-weight:700}details div{max-width:960px}h3{font-size:16px;margin:20px 0 4px}details p{margin:0 0 15px}.note{padding:12px 18px;background:#fff2df;border-radius:9px}@media(max-width:650px){header,main{padding:16px}.section-head{display:block;padding:18px}.section-head span{display:block}details{padding:18px}}@media print{nav,.actions,details,header{display:none}section{break-before:page;border:none}.section-head{display:none}body{background:white}}
</style><header><h1>Hydra-One · Colección visual completa</h1><p>Diez mapas para recorrer el proyecto: desde la idea general hasta las decisiones de arquitectura, datos, desarrollo y validación. Abre cada imagen para ampliarla; despliega su explicación para preparar el informe o la defensa.</p><p><a href="GUIA-COMPLETA.md">Guía completa</a> · <a href="../../Hydra-One-coleccion-visual.zip">Descargar colección ZIP</a> · <a href="../Hydra-One-diagramas.drawio">Diagramas técnicos editables anteriores</a></p><p class="note">Actual = respaldado por lectura del código. Propuesta = pendiente de implementar. Metodología = enfoque declarado en informes, cuya ejecución requiere evidencias. Son ilustraciones conceptuales, no capturas ni resultados de pruebas.</p>'''+nav+'</header><main>'+''.join(cards)+'</main></html>'
(p/'coleccion.html').write_text(html,encoding='utf-8')
# El enlace existente abre ahora la colección completa.
(p/'index.html').write_text(html,encoding='utf-8')
guide=['# Hydra-One · Guía de la colección visual ampliada','Revisión documental y del repositorio: 28 de octubre de 2026. Diez mapas PNG: tres introductorios y siete de profundización. Las imágenes se elaboraron con la herramienta integrada de generación de imágenes; los prompts de las siete nuevas están en catalogo-ampliado.json.','## Orden recomendado','Para explicar a público general: 01 → 02 → 03. Para revisión técnica: 04 → 05 → 06 → 07. Para alcance pendiente y proceso de trabajo: 08 → 09 → 10. Cada mapa tiene una función; no hace falta mostrarlos todos al responder una pregunta.','## Qué demuestra esta colección','Documenta un modelo explicativo del código y del enfoque declarado. No acredita que la conexión a Neon funcione, que se hayan ejecutado pruebas ni que se haya aplicado Scrum de manera completa. Las interfaces y servidores dibujados son metáforas visuales. Los PNG no contienen elementos editables; los anteriores draw.io siguen disponibles como complemento técnico.']
for s in all_items:
    guide.extend([f'## {s["slug"][:2]}. {s["title"]}',f'Estado: **{s["state"]}**.',f'![{s["title"]}]({s["slug"]}.png)'])
    for key,title in fields:
        if s.get(key): guide.extend([f'### {title}',s[key]])
guide.extend(['## Criterios para acompañar las imágenes con evidencias','- Documentación: requisito y decisión vinculados con la versión del diagrama.\n- Aplicación: recorrido reproducible, capturas reales, respuestas HTTP y resultado observado.\n- Base de datos: esquema real, migración aplicada y consulta del mismo registro usado en la demostración.\n- Metodología: backlog, objetivos, responsables, acuerdos y revisiones fechadas.\n- Pruebas: esperado frente a obtenido, versión, entorno y defectos encontrados.','## Revisión de las imágenes','Se revisaron las etiquetas, las relaciones y el sentido de las flechas. Se corrigieron dos conexiones generadas: «sin alerta» no aporta una alerta a la lista; y una consulta posterior a COMMIT no dispara rollback del cierre ya confirmado. Las imágenes finales incluidas contienen esas correcciones. La revisión de archivos comprueba PNG y enlaces locales; no son pruebas de Hydra-One.','## Ediciones de generación','07: eliminar la conexión de salida de «Sin alerta» hacia la campana central.\n\n08: eliminar la conexión desde «Alertas en próxima consulta» hacia ROLLBACK; conservar rollback solo para errores durante la transacción.','## Archivos','coleccion.html / index.html: galería local sin dependencias externas.\n\n01–10: imágenes PNG.\n\ncatalogo-ampliado.json: explicación estructurada, estado, fuentes y prompts de generación.\n\ncrear_coleccion.py: regenera la galería y esta guía sin modificar imágenes.\n\nLEEME.md: explicación original de los tres primeros mapas.'])
(p/'GUIA-COMPLETA.md').write_text('\n\n'.join(guide)+'\n',encoding='utf-8')
validation=[]
for s in all_items:
    f=p/(s['slug']+'.png')
    data=f.read_bytes()
    assert data[:8]==b'\x89PNG\r\n\x1a\n',f
    width,height=struct.unpack('>II',data[16:24])
    validation.append(dict(file=f.name,width=width,height=height,bytes=len(data)))
(p/'verificacion-coleccion.json').write_text(json.dumps(dict(images=validation,scope='Existencia y dimensiones PNG; revisión visual semántica realizada; no pruebas funcionales'),ensure_ascii=False,indent=2),encoding='utf-8')
archive=p.parents[1]/'Hydra-One-coleccion-visual.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(p.iterdir()):
        if f.is_file():
            if f.suffix=='.html':
                portable=f.read_text(encoding='utf-8').replace(' · <a href="../../Hydra-One-coleccion-visual.zip">Descargar colección ZIP</a>','').replace('../Hydra-One-diagramas.drawio','Hydra-One-diagramas.drawio')
                z.writestr('Hydra-One-visuales/'+f.name,portable)
            else: z.write(f,Path('Hydra-One-visuales')/f.name)
    z.write(p.parent/'Hydra-One-diagramas.drawio','Hydra-One-visuales/Hydra-One-diagramas.drawio')
print(f'Colección creada: {len(all_items)} PNG verificados. ZIP: {archive}')

