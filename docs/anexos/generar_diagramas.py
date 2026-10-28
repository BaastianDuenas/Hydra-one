"""Genera anexos vectoriales reproducibles; solo biblioteca estándar de Python.
Las coordenadas son compartidas por SVG y draw.io. No consulta la base de datos.
"""
from pathlib import Path
import xml.etree.ElementTree as E
from html import escape
import json

ROOT = Path(__file__).resolve().parent
BLUE, TEAL, AMBER, INK, GRAY = '#175cd3', '#087f8c', '#b65b13', '#172b4d', '#62748b'
ALL = []

class Diagram:
    def __init__(self, slug, title, w, h, status='ACTUAL · verificado en código'):
        self.slug, self.title, self.w, self.h, self.status = slug, title, w, h, status
        self.svg=[]; self.root=E.Element('root'); E.SubElement(self.root,'mxCell',id='0'); E.SubElement(self.root,'mxCell',id='1',parent='0'); self.i=1
        self.text(32,20,w-64,35,title,26,INK,True)
        self.text(32,62,w-64,25,status,14,AMBER if status.startswith('PROPUESTA') else TEAL,True)
        self.text(32,h-35,w-64,22,'HYDRA-ONE  /  Anexo técnico  /  28 oct 2026  /  fuente: código 5d449af',12,GRAY)
        ALL.append(self)
    def cell(self, value, style, x,y,w,h):
        self.i+=1
        c=E.SubElement(self.root,'mxCell',id=str(self.i),value=value,style=style,vertex='1',parent='1')
        E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
        return c
    def text(self,x,y,w,h,value,size=16,color=INK,bold=False,center=False):
        lines=value.split('\n'); lineheight=size*1.35
        tx=x+w/2 if center else x
        yy=y+(h-lineheight*len(lines))/2+size
        s=f'<text font-family="Arial, sans-serif" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{"middle" if center else "start"}">'
        for k,line in enumerate(lines): s+=f'<tspan x="{tx}" y="{yy+k*lineheight}">{escape(line)}</tspan>'
        self.svg.append(s+'</text>')
        self.cell(value,f'text;html=0;whiteSpace=wrap;align={"center" if center else "left"};verticalAlign=middle;fontFamily=Arial;fontSize={size};fontColor={color};fontStyle={1 if bold else 0};',x,y,w,h)
    def shape(self,x,y,w,h,kind='rect',fill='#ffffff',stroke=GRAY,dash=False):
        ds=' stroke-dasharray="7 5"' if dash else ''
        if kind=='diamond':
            s=f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}"'
        elif kind=='ellipse': s=f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}"'
        else: s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{8 if kind=="round" else 0}"'
        self.svg.append(s+f' fill="{fill}" stroke="{stroke}" stroke-width="1.6"{ds}/>')
        self.cell('',f'shape={"rhombus" if kind=="diamond" else "ellipse" if kind=="ellipse" else "rectangle"};rounded={1 if kind=="round" else 0};fillColor={fill};strokeColor={stroke};strokeWidth=1.6;dashed={1 if dash else 0};',x,y,w,h)
    def box(self,x,y,w,h,title,body='',color=BLUE,kind='round'):
        first=self.i
        self.shape(x,y,w,h,kind,'#ffffff',color)
        if body:
            self.text(x+14,y+10,w-28,30,title,17,color,True,True)
            self.text(x+14,y+47,w-28,h-55,body,15,INK,False,True)
        else: self.text(x+12,y+5,w-24,h-10,title,16,color,True,True)
        self.bundle(first,x,y,w,h)
    def bundle(self,first,x,y,w,h):
        children=[c for c in self.root if int(c.get('id'))>first]
        group=self.cell('','group;',x,y,w,h)
        self.root.remove(group)
        self.root.insert(list(self.root).index(children[0]),group)
        for c in children:
            c.set('parent',group.get('id'))
            g=c.find('mxGeometry')
            g.set('x',str(float(g.get('x'))-x));g.set('y',str(float(g.get('y'))-y))
    def group(self,x,y,w,h,title):
        self.shape(x,y,w,h,fill='#f7f9fc',stroke='#adbacc',dash=True)
        self.text(x+15,y+9,w-30,26,title,15,GRAY,True)
    def note(self,x,y,w,h,value):
        self.shape(x,y,w,h,fill='#fff7e8',stroke='#e7bf7a')
        self.text(x+14,y+8,w-28,h-16,value,14,INK)
    def edge(self,pts,label='',lx=None,ly=None,lw=260,dash=False,marker='arrow'):
        self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{GRAY}" stroke-width="1.7"'+(' stroke-dasharray="6 5"' if dash else '')+(f' marker-end="url(#{marker})"' if marker else '')+(' marker-start="url(#one)"' if marker=='many' else '')+'/>')
        self.i+=1
        c=E.SubElement(self.root,'mxCell',id=str(self.i),edge='1',parent='1',style=f'endArrow={"ERzeroToMany" if marker=="many" else "block" if marker else "none"};startArrow={"ERmandOne" if marker=="many" else "none"};endFill=1;strokeColor={GRAY};strokeWidth=1.7;dashed={int(dash)};')
        g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        for key,p in [('sourcePoint',pts[0]),('targetPoint',pts[-1])]: E.SubElement(g,'mxPoint',x=str(p[0]),y=str(p[1]),attrib={'as':key})
        if len(pts)>2:
            a=E.SubElement(g,'Array',attrib={'as':'points'})
            for p in pts[1:-1]: E.SubElement(a,'mxPoint',x=str(p[0]),y=str(p[1]))
        if label:
            x,y=lx,ly
            self.shape(x,y,lw,25,fill='#ffffff',stroke='#ffffff')
            self.text(x+3,y,lw-6,25,label,13,GRAY,False,True)
    def table(self,x,y,w,name,rows,color=TEAL):
        first=self.i
        h=48+len(rows)*30
        self.shape(x,y,w,h,stroke=color)
        self.shape(x,y,w,48,fill=color,stroke=color)
        self.text(x+14,y+4,w-28,40,name,19,'#ffffff',True)
        for i,row in enumerate(rows):
            yy=y+48+i*30
            if i%2==0: self.shape(x+1,yy,w-2,30,fill='#f2f6fa',stroke='#f2f6fa')
            self.text(x+12,yy,w-24,30,row,14,INK,row.startswith('PK'))
        self.bundle(first,x,y,w,h)
    def model(self):
        m=E.Element('mxGraphModel',dx=str(self.w),dy=str(self.h),grid='1',gridSize='10',page='1',pageWidth=str(self.w),pageHeight=str(self.h),math='0',shadow='0'); m.append(self.root); return m
    def save(self):
        defs='''<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 Z" fill="#62748b"/></marker><marker id="one" markerWidth="20" markerHeight="20" refX="1" refY="10" orient="auto"><path d="M7,2 V18 M13,2 V18" fill="none" stroke="#62748b" stroke-width="1.7"/></marker><marker id="many" markerWidth="28" markerHeight="22" refX="27" refY="11" orient="auto"><circle cx="6" cy="11" r="4" fill="white" stroke="#62748b" stroke-width="1.7"/><path d="M14,11 L27,2 M14,11 H27 M14,11 L27,20" fill="none" stroke="#62748b" stroke-width="1.7"/></marker></defs>'''
        (ROOT/'svg'/f'{self.slug}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img"><title>{escape(self.title)}</title>'+defs+f'<rect width="{self.w}" height="{self.h}" fill="white"/>'+''.join(self.svg)+'</svg>',encoding='utf-8')
        mx=E.Element('mxfile',host='app.diagrams.net',version='24.7.17'); page=E.SubElement(mx,'diagram',id=self.slug,name=self.title); page.append(self.model()); E.ElementTree(mx).write(ROOT/'drawio'/f'{self.slug}.drawio',encoding='utf-8',xml_declaration=True)

def build():
    d=Diagram('01-contexto','01 / Contexto del sistema · C4 nivel 1',1120,620)
    d.box(40,210,235,145,'Usuario de operaciones','Registra equipos, programa\nmantenciones y revisa stock',TEAL)
    d.box(465,170,330,220,'Hydra-One','Sistema de gestión operacional\n\nActivos · Mantenciones\nInventario · Alertas',BLUE)
    d.edge([(275,280),(465,280)],'usa mediante la web',280,240,180)
    d.note(465,440,565,100,'Alcance actual: aplicación CRUD con alertas calculadas.\nEl cargo «Administrador» de la interfaz es estático.\nNo hay autenticación ni permisos por rol implementados.')
    d.text(40,405,320,70,'Actor funcional; no equivale a un rol\nde seguridad ya implementado.',14,GRAY)

    d=Diagram('02-contenedores','02 / Arquitectura de contenedores · C4 nivel 2',1260,740)
    d.group(35,125,1190,445,'LÍMITE DEL SISTEMA HYDRA-ONE · monolito modular')
    d.box(75,230,275,180,'Aplicación web / SPA','React + TypeScript\nSe ejecuta en el navegador\nPáginas y formularios',BLUE)
    d.box(480,230,300,180,'API de aplicación','FastAPI + Pydantic\nRouters con lógica de negocio\nSQLAlchemy + psycopg',BLUE)
    d.box(925,230,260,180,'Base de datos','PostgreSQL\nActivos · Mantenciones\nRepuestos',TEAL)
    d.edge([(350,300),(480,300)],'HTTP / JSON',350,265,130)
    d.edge([(780,300),(925,300)],'SQL / PostgreSQL',780,265,145)
    d.text(70,450,300,65,'VITE_API_URL define la API.\nNo contiene credenciales de BD.',14,GRAY,False,True)
    d.text(480,450,300,65,'DATABASE_URL solo en backend.\nUna sesión SQLAlchemy por petición.',14,GRAY,False,True)
    d.text(925,450,260,65,'Neon: proveedor indicado\npor el equipo; remoto no auditado.',14,GRAY,False,True)
    d.note(35,600,1190,70,'En desarrollo: Vite sirve el frontend y Uvicorn ejecuta FastAPI. Son procesos distintos.\nCORS permite el origen del frontend; CORS no reemplaza autenticación. No se verificó un despliegue productivo.')

    d=Diagram('03-componentes','03 / Componentes y dependencias del código',1370,1000)
    d.group(35,120,1300,190,'FRONTEND · frontend/src')
    for x,title,body in [(60,'App.tsx','Rutas · Sidebar · Topbar'),(480,'pages/*.tsx','CRUD · Detalle · Alertas'),(900,'services/api.ts','fetch · JSON · errores HTTP')]: d.box(x,180,360,90,title,body)
    d.edge([(420,225),(480,225)]); d.edge([(840,225),(900,225)])
    d.group(35,365,1300,440,'BACKEND · backend/app · routers dentro del mismo proceso FastAPI')
    for x,t in [(60,'activos.py'),(380,'mantenciones.py'),(700,'repuestos.py'),(1020,'alertas.py')]: d.box(x,440,270,85,t,'routers / endpoints')
    d.edge([(1080,270),(1080,335),(195,335),(195,440)],'HTTP / JSON hacia los routers',430,307,300)
    d.edge([(1080,335),(1155,335)],marker='')
    d.edge([(515,335),(515,440)]); d.edge([(835,335),(835,440)]); d.edge([(1155,335),(1155,440)])
    d.box(60,660,350,100,'schemas/*.py','Pydantic: entrada y respuesta',TEAL)
    d.box(510,660,350,100,'models/*.py','Activo · Mantencion · Repuesto',TEAL)
    d.box(960,660,350,100,'database/connection.py','engine · SessionLocal · get_db',TEAL)
    for x in [195,515,835,1155]: d.edge([(x,525),(x,580)],marker='')
    d.edge([(195,580),(1155,580)],marker='')
    for x in [235,685,1135]: d.edge([(x,580),(x,660)])
    d.text(280,590,350,45,'Validan, consultan modelos\ny obtienen sesión',14,GRAY,False,True)
    d.box(960,860,350,80,'PostgreSQL','Persistencia del estado',TEAL)
    d.edge([(1135,760),(1135,860)],'SQL',1150,800,60)
    d.note(35,850,820,85,'Las líneas agrupadas resumen dependencias, no una secuencia de ejecución.\nDashboard usa cifras estáticas; /health solo comprueba respuesta de la API.\nNo existe todavía una capa separada de servicios o repositorios.')

    d=Diagram('04-erd-actual','04 / Modelo entidad–relación · esquema actual',1370,790)
    d.table(35,160,365,'activos',['PK  id : integer','UQ  codigo : varchar(50)','nombre : varchar(150)','tipo : varchar(100)','estado : varchar(50)','horometro : integer','kilometraje : integer'])
    d.table(530,160,365,'mantenciones',['PK  id : integer','FK  activo_id : integer','tipo : varchar(50)','descripcion : varchar(500)','fecha : date','horometro : integer','estado : varchar(50)'])
    d.table(965,160,365,'repuestos',['PK  id : integer','UQ  codigo : varchar(50)','nombre : varchar(150)','descripcion : varchar(500)','categoria : varchar(100)','stock_actual : integer','stock_minimo : integer','unidad_medida : varchar(50)','ubicacion : varchar(150)'])
    d.edge([(400,235),(530,235)],marker='many')
    d.text(405,175,120,45,'1  →  0..N',15,TEAL,True,True)
    d.text(405,265,120,65,'Cada mantención\npertenece a\nun activo.',13,GRAY,False,True)
    d.note(35,530,860,145,'PK: clave primaria · FK: clave foránea · UQ: valor único.\nTodos los campos son NOT NULL. Un activo puede tener cero o muchas mantenciones.\nRepuestos no tiene relación con mantenciones en este esquema.\nEl borrado en cascada está configurado en el ORM; no como ON DELETE CASCADE\nen la migración. Valores por defecto 0: ORM, no defaults de servidor.')
    d.note(965,530,365,145,'No hay tablas de usuarios, consumos,\nmovimientos ni alertas persistidas.\n\nEsquema deducido de modelos y\nmigraciones; no inspeccionado en Neon.')

    d=Diagram('05-secuencia-alta','05 / Secuencia UML · registrar una mantención',1220,1060)
    xs=[150,460,790,1090]
    for x,t in zip(xs,['Usuario / formulario','api.ts / fetch','FastAPI / router','SQLAlchemy / BD']):
        d.box(x-115,125,230,65,t)
        d.edge([(x,190),(x,960)],dash=True,marker='')
    def msg(a,b,y,label,ret=False):
        d.edge([(xs[a],y),(xs[b],y)],dash=ret)
        d.text(min(xs[a],xs[b])+10,y-31,abs(xs[b]-xs[a])-20,25,label,13,GRAY,False,True)
    msg(0,1,245,'1. Enviar formulario')
    msg(1,2,315,'2. POST /api/mantenciones/')
    d.note(620,345,360,62,'Pydantic valida datos. Si son inválidos:\nHTTP 422; el router no ejecuta el alta.')
    msg(2,3,455,'3. Buscar activo_id')
    msg(3,2,510,'4. Activo o ausencia',True)
    d.shape(350,550,830,360,fill='none',stroke=GRAY)
    d.text(365,558,790,28,'alt [activo no existe]',14,INK,True)
    msg(2,1,620,'5a. HTTP 404',True)
    d.edge([(350,660),(1180,660)],dash=True,marker='')
    d.text(365,665,790,28,'[activo existe]',14,INK,True)
    msg(2,3,735,'5b. add → commit → refresh')
    msg(3,2,795,'6. Mantención persistida',True)
    msg(2,1,855,'7. HTTP 201 + JSON',True)
    msg(1,0,950,'8. Mostrar resultado',True)
    d.text(35,985,1140,28,'Flujo de alta actual: no reserva repuestos, no descuenta stock y no genera movimientos.',14,AMBER)

    d=Diagram('06-alertas','06 / Reglas de alertas · árbol de decisión actual',1360,1000)
    d.box(460,120,440,65,'GET /api/alertas/ · cálculo al consultar')
    d.group(35,240,620,540,'A · INVENTARIO · por cada repuesto')
    d.group(705,240,620,540,'B · MANTENCIONES · solo estado Programada')
    d.edge([(680,185),(680,215),(345,215),(345,295)])
    d.edge([(680,215),(1015,215),(1015,295)])
    d.box(210,295,270,110,'stock_actual ≤\nstock_minimo?',kind='diamond')
    d.box(880,295,270,110,'fecha < hoy?',kind='diamond')
    d.box(75,480,240,110,'stock_actual = 0?',kind='diamond')
    d.box(425,495,190,75,'Sin alerta',color=GRAY)
    d.edge([(345,405),(345,440),(195,440),(195,480)],'sí',240,410,50)
    d.edge([(480,350),(550,350),(550,495)],'no',560,400,50)
    d.box(65,655,220,70,'Crítica · sin stock',color=AMBER)
    d.box(375,655,220,70,'Alta · stock bajo',color=AMBER)
    d.edge([(195,590),(195,620),(175,620),(175,655)],'sí',110,610,50)
    d.edge([(315,535),(365,535),(365,620),(485,620),(485,655)],'no',375,585,50)
    d.box(735,485,220,75,'Crítica · vencida',color=AMBER)
    d.box(1030,465,250,115,'fecha ≤ hoy + 7?',kind='diamond')
    d.edge([(1015,405),(1015,435),(845,435),(845,485)],'sí',865,405,50)
    d.edge([(1150,350),(1250,350),(1250,430),(1155,430),(1155,465)],'no',1260,385,50)
    d.box(755,655,245,70,'Media · próxima',color=AMBER)
    d.box(1080,655,220,70,'Sin alerta',color=GRAY)
    d.edge([(1030,522.5),(1005,522.5),(1005,610),(880,610),(880,655)],'sí',925,580,50)
    d.edge([(1155,580),(1155,615),(1190,615),(1190,655)],'no',1200,590,50)
    d.note(35,820,1290,100,'Se combinan los resultados A y B en una lista JSON. La bifurcación dibuja reglas, no tareas paralelas del servidor.\n«hoy» usa la fecha del servidor. El intervalo próximo incluye hoy y el séptimo día.\nNo se guardan alertas; no hay correo ni tarea programada. Una nueva consulta vuelve a evaluar los datos.')

    d=Diagram('07-despliegue','07 / Despliegue de desarrollo y conexión compartida',1300,810,'CONFIGURACIÓN DE DESARROLLO · Neon indicado por el equipo; conexión no verificada')
    for x,label in [(35,'EQUIPO A · desarrollador'),(695,'EQUIPO B · compañero')]:
        d.group(x,125,570,355,label)
        d.box(x+30,190,230,105,'Navegador + Vite','localhost:5173\nReact en el navegador')
        d.box(x+310,190,230,105,'Uvicorn + FastAPI','localhost:8000\nEntorno Python / backend')
        d.edge([(x+260,245),(x+310,245)])
        d.text(x+30,320,510,40,'HTTP / JSON en la máquina local · CORS_ORIGINS',14,GRAY,False,True)
        d.note(x+30,375,510,70,'backend/.env → DATABASE_URL\nEl secreto queda en el servidor, fuera de frontend y Git.')
    d.box(480,600,340,110,'Neon / PostgreSQL','Servidor remoto compartido\nMismo proyecto + rama + base de datos',TEAL)
    d.edge([(460,480),(460,550),(560,550),(560,600)],'PostgreSQL + TLS',260,510,190)
    d.edge([(1120,480),(1120,550),(740,550),(740,600)],'PostgreSQL + TLS',920,510,190)
    d.text(35,735,1230,30,'Compartir credenciales no configura automáticamente cada equipo. Cada backend debe usar la conexión correcta.',14,GRAY,False,True)

    d=Diagram('08-erd-propuesto','08 / Integración de inventario · modelo lógico propuesto',1370,960,'PROPUESTA · requiere acordar reglas, migraciones y pruebas; no implementado')
    d.table(35,145,345,'activos · existente',['PK  id : integer','… campos actuales'],BLUE)
    d.table(35,420,345,'mantenciones · existente',['PK  id : integer','FK  activo_id : integer','… campos actuales'],BLUE)
    d.table(520,420,370,'consumos · nueva',['PK  id : integer','FK  mantencion_id : integer','FK  repuesto_id : integer','cantidad : integer > 0','UQ (mantencion_id, repuesto_id)'],AMBER)
    d.table(990,145,345,'repuestos · existente',['PK  id : integer','stock_actual : integer ≥ 0','… campos actuales'],BLUE)
    d.table(990,610,345,'movimientos · nueva',['PK  id : integer','FK  repuesto_id : integer','FK  consumo_id : integer NULL','UQ  consumo_id (si no es NULL)','delta : integer ≠ 0','fecha : timestamptz','motivo : varchar'],AMBER)
    d.edge([(200,253),(200,420)],marker='many'); d.text(210,310,150,25,'1 → 0..N',14,GRAY)
    d.edge([(380,490),(520,490)],marker='many'); d.text(390,450,120,25,'1 → 0..N',14,GRAY)
    d.edge([(990,230),(705,230),(705,420)],marker='many'); d.text(750,195,220,25,'1 repuesto → 0..N consumos',13,GRAY)
    d.edge([(1235,283),(1235,610)],marker='many'); d.text(1240,420,90,25,'1 → 0..N',13,GRAY)
    d.edge([(890,550),(940,550),(940,700),(990,700)],marker=''); d.text(730,660,200,60,'consumo 0..1 ↔ 0..1\nmovimiento de salida',13,AMBER,False,True)
    d.note(35,725,840,150,'Azul: entidades existentes, campos abreviados. Ámbar: diseño por implementar.\nUn consumo puede originar como máximo una salida (FK única), y un movimiento\npuede no provenir de un consumo (entrada o ajuste). Al completar una mantención,\ncada consumo debe tener su salida; esta regla requiere lógica transaccional.\nDefinir política de anulaciones y borrados antes de aprobar este modelo.')

    d=Diagram('09-cierre-propuesto','09 / Actividad · cierre transaccional de mantención',1200,1170,'PROPUESTA · diseño de la integración pendiente; no implementado')
    d.group(40,110,1120,960,'BACKEND · una transacción para el cierre completo')
    d.shape(420,165,24,24,'ellipse',INK,INK)
    d.box(270,225,325,70,'Solicitar cierre y consumos')
    d.edge([(432,189),(432,225)])
    d.box(270,345,325,80,'Iniciar transacción','Bloquear mantención y repuestos')
    d.edge([(432,295),(432,345)])
    d.box(270,475,325,120,'¿Existe y está\npendiente de cierre?',kind='diamond')
    d.edge([(432,425),(432,475)])
    d.box(790,490,280,90,'Rechazar operación','Ausente o ya completada',color=AMBER)
    d.edge([(595,535),(790,535)],'no',650,500,60)
    d.box(270,650,325,120,'¿Cantidades válidas\ny stock suficiente?',kind='diamond')
    d.edge([(432,595),(432,650)],'sí',445,605,50)
    d.box(790,665,280,90,'Rollback + error','Sin cambios parciales',color=AMBER)
    d.edge([(595,710),(790,710)],'no',650,675,60)
    d.edge([(930,580),(930,665)])
    d.box(200,825,465,100,'Aplicar cierre atómico','Registrar consumos y movimientos\nDescontar stock · marcar Completada',TEAL)
    d.edge([(432,770),(432,825)],'sí',445,780,50)
    d.box(270,975,325,65,'Commit · devolver resultado',color=TEAL)
    d.edge([(432,925),(432,975)])
    d.note(740,840,360,170,'Ante fallo de escritura: rollback.\nEvitar doble descuento y cierres\nconcurrentes con bloqueo y\nrestricciones de unicidad.\nLas alertas se recalculan en\nla siguiente consulta.')
    d.text(40,1090,1120,38,'Hoy: actualizar estado solo guarda un texto. Este circuito requiere implementación y pruebas de concurrencia.',14,AMBER,False,True)

    for folder in ['svg','drawio','png']: (ROOT/folder).mkdir(parents=True,exist_ok=True)
    combined=E.Element('mxfile',host='app.diagrams.net',version='24.7.17')
    for d in ALL:
        d.save(); page=E.SubElement(combined,'diagram',id=d.slug,name=d.title); page.append(d.model())
    E.ElementTree(combined).write(ROOT/'Hydra-One-diagramas.drawio',encoding='utf-8',xml_declaration=True)
    (ROOT/'catalogo.json').write_text(json.dumps([dict(slug=d.slug,title=d.title,status=d.status,width=d.w,height=d.h) for d in ALL],ensure_ascii=False,indent=2),encoding='utf-8')
    cards=''.join(f'<article><h2>{escape(d.title)}</h2><p>{escape(d.status)}</p><a href="svg/{d.slug}.svg"><img loading="lazy" src="svg/{d.slug}.svg" alt="{escape(d.title)}"></a><nav><a href="svg/{d.slug}.svg">Abrir SVG / ampliar</a><a href="png/{d.slug}.png">PNG</a><a href="drawio/{d.slug}.drawio" download>Editar en draw.io</a></nav></article>' for d in ALL)
    (ROOT/'index.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Hydra-One · Anexos técnicos</title><style>body{margin:0;background:#edf2f7;color:#172b4d;font:16px Arial,sans-serif}header,main{max-width:1400px;margin:auto;padding:30px}h1{font-size:30px}header p{max-width:900px;line-height:1.6}article{background:white;margin:0 0 40px;padding:24px;border:1px solid #cfdae7;border-radius:12px}h2{font-size:22px}article p{color:#62748b}img{width:100%;height:auto}nav{display:flex;gap:24px;padding-top:15px}a{color:#175cd3}@media print{body{background:white}header,nav{display:none}article{break-before:page;padding:0;border:0;margin:0}article h2,article p{display:none}}</style><header><h1>Hydra-One / Anexos técnicos</h1><p>Diagramas editables para explicar el sistema, documentar su estado y discutir las integraciones pendientes. Haz clic en un diagrama para ampliarlo. Los archivos son locales y no necesitan conexión a Neon.</p><a href="Hydra-One-diagramas.drawio" download>Descargar todos los diagramas editables</a> · <a href="README.md">Guía de lectura y fuentes</a></header><main>'''+cards+'</main></html>',encoding='utf-8')
    print(f'Generados {len(ALL)} diagramas SVG y draw.io en {ROOT}')

if __name__=='__main__': build()
