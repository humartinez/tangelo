Tangelo test

Arquitectura y notas

Realice un cambio en la arquitectura, para hacerla de 3 capas, entiendo que no se pidio pero me parecio una buena propuesta
La solucion consta de 3 contenedores:

1) Un frontend nginx que deriva las peticiones a el webservice 

2) El webservice que se encarga de hacer el manejo de imagenes y el envio a la DB 

3) Una instancia de mongoDB que guarda la url y la imagen rescalada


FE -> WEBAPP -> DB

El unico puerto que se expone es el 80 del nginx, todo la comunicacion se realiza entre los contenedores con 2 redes,
una de frontend y otra para el backend

Elegi docker-compose para hacer el deploy de los contenedores, python+flask+gunicorn para hacer la app y mongoDB para
persistir los datos

La applicacion tiene 2 rutas en las que esta escuchando

  * /push, aqui es donde se hacen los POST de las imagenes
  * /health, este es el metodo que devuelve la disponibilidad de la DB

Uso

docker-compose up para levantar el ambiente

para probar usar la app 


hugo@hugo-VirtualBox:~/bes/tangelo$ curl -H "Content-Type: application/json" -X POST -d '{"URL":"https://tangelogames.com/wp-content/uploads/2016/06/02-vert-g-a-m-e-s-m-i-u-n-t.png"}' 127.0.0.1:80/push
hugo@hugo-VirtualBox:~/bes/tangelo$ curl 127.1/health
{"ok":1.0,"you":"172.26.0.3:36272"}

