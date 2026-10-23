<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Daniel Dóniz García · Ingeniero Informático y desarrollador todoterreno · Tenerife">
</p>

<p align="center">
  <i>De la web al servidor y de los datos a los videojuegos: si se puede programar, me apunto.<br>
  Programo desde Tenerife, entre el Teide y el Atlántico.</i>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/daniel-d%C3%B3niz-728455185/"><code>linkedin</code></a> ·
  <a href="https://x.com/mrdoniz"><code>x</code></a> ·
  <a href="https://www.instagram.com/mrdoniz/"><code>instagram</code></a> ·
  <a href="mailto:donizgarciadaniel@gmail.com"><code>correo</code></a>
</p>

### `$ cat perfil.abap`

```abap
REPORT zrp_daniel_doniz.

" Sí, esto es ABAP: el del trabajo. Fuera de horario, toco de todo.
DATA(ls_perfil) = VALUE zcl_perfil=>ty_perfil(
  nombre    = `Daniel Dóniz García`
  isla      = `Tenerife, la isla de la eterna primavera`
  titulo    = `Ingeniero Informático por la Universidad de La Laguna`
  trabajo   = `Desarrollador en DISA`
  filosofia = `si no sé hacerlo todavía, lo aprendo por el camino` ).

DATA(lt_tiempo_libre) = VALUE string_table(
  ( `webs` ) ( `APIs` ) ( `servidores` ) ( `IA` ) ( `bots` ) ( `videojuegos` ) ).

DATA(lo_perfil) = NEW zcl_perfil( ls_perfil ).
lo_perfil->mostrar( lt_tiempo_libre ).
```

### `$ cat tfg.md`

> **[Mejora de diagnóstico de enfermedades neurodegenerativas usando redes LSTM](https://riull.ull.es/xmlui/handle/915/33918)**<br>
> Trabajo de Fin de Grado · Universidad de La Laguna · 2023<br>
> Mejora una solución previa de IA para el diagnóstico y pronóstico del alzhéimer con redes LSTM, a partir de las pruebas ADAS y MMSE.

### `$ ls ~/herramientas`

<table>
  <tr>
    <td><b>Frontend</b></td>
    <td><img src="https://skillicons.dev/icons?i=ts,js,react,nextjs,vite,tailwind,html,css" alt="TypeScript, JavaScript, React, Next.js, Vite, Tailwind CSS, HTML, CSS"><br><sub>Zustand · Leaflet · PWA</sub></td>
  </tr>
  <tr>
    <td><b>Backend</b></td>
    <td><img src="https://skillicons.dev/icons?i=nodejs,express,nestjs,fastapi,django,flask,php" alt="Node.js, Express, NestJS, FastAPI, Django, Flask, PHP"><br><sub>Socket.IO · TypeORM · Zod · JWT y OAuth</sub></td>
  </tr>
  <tr>
    <td><b>Bases de datos</b></td>
    <td><img src="https://skillicons.dev/icons?i=postgres,redis,mysql,sqlite" alt="PostgreSQL, Redis, MySQL, SQLite"> <img src="assets/iconos/sqlserver.svg" width="48" alt="SQL Server"> <img src="assets/iconos/phpmyadmin.svg" width="48" alt="phpMyAdmin"><br><sub>PostGIS</sub></td>
  </tr>
  <tr>
    <td><b>IA y datos</b></td>
    <td><img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow" alt="Python, PyTorch, TensorFlow"><br><sub>Transformers · CUDA · pandas · NumPy · Jupyter · Colab · Kaggle</sub></td>
  </tr>
  <tr>
    <td><b>SAP e integraciones</b></td>
    <td><img src="assets/iconos/sap.svg" width="48" alt="SAP"> <img src="https://skillicons.dev/icons?i=postman" alt="Postman"> <img src="assets/iconos/soapui.svg" width="48" alt="SoapUI"><br><sub>ABAP · APIs SOAP y REST</sub></td>
  </tr>
  <tr>
    <td><b>Automatización</b></td>
    <td><img src="assets/iconos/uipath.svg" width="48" alt="UiPath"> <img src="assets/iconos/powerautomate.svg" width="48" alt="Power Automate"> <img src="assets/iconos/powerapps.svg" width="48" alt="Power Apps"><br><sub>RPA y low-code</sub></td>
  </tr>
  <tr>
    <td><b>Servidores y despliegue</b></td>
    <td><img src="https://skillicons.dev/icons?i=docker,nginx,githubactions,bash,powershell" alt="Docker, Nginx, GitHub Actions, Bash, PowerShell"> <img src="assets/iconos/proxmox.svg" width="48" alt="Proxmox"> <img src="assets/iconos/esxi.svg" width="48" alt="VMware ESXi"> <img src="assets/iconos/hyperv.svg" width="48" alt="Hyper-V"> <img src="assets/iconos/plesk.svg" width="48" alt="Plesk"> <img src="assets/iconos/cpanel.svg" width="48" alt="cPanel"><br><sub>Caddy · VPS con despliegue continuo</sub></td>
  </tr>
  <tr>
    <td><b>Sistemas operativos</b></td>
    <td><img src="https://skillicons.dev/icons?i=linux,ubuntu,raspberrypi,windows,apple" alt="Linux, Ubuntu, Raspberry Pi OS, Windows, macOS"></td>
  </tr>
  <tr>
    <td><b>Pruebas y bots</b></td>
    <td><img src="https://skillicons.dev/icons?i=vitest,discord" alt="Vitest, Discord"><br><sub>Playwright · Supertest · bots de Telegram · Web Push</sub></td>
  </tr>
  <tr>
    <td><b>Juegos y bajo nivel</b></td>
    <td><img src="https://skillicons.dev/icons?i=unity,cs,cpp,c,java" alt="Unity, C#, C++, C, Java"></td>
  </tr>
  <tr>
    <td><b>Imagen y vídeo</b></td>
    <td><img src="https://skillicons.dev/icons?i=ps,ae,pr" alt="Photoshop, After Effects, Premiere"></td>
  </tr>
  <tr>
    <td><b>Día a día</b></td>
    <td><img src="https://skillicons.dev/icons?i=git,github,vscode,eclipse" alt="Git, GitHub, Visual Studio Code, Eclipse"> <img src="assets/iconos/notepadpp.svg" width="48" alt="Notepad++"></td>
  </tr>
</table>

### `$ git log --stat`

<p align="center">
  <img src="https://raw.githubusercontent.com/MrDoniz/MrDoniz/refs/heads/estadisticas/marea.svg" width="100%" alt="Calendario de contribuciones del último año">
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/MrDoniz/MrDoniz/refs/heads/estadisticas/resumen.svg" width="49%" alt="Contribuciones totales, rachas y mejor día">
  <img src="https://raw.githubusercontent.com/MrDoniz/MrDoniz/refs/heads/estadisticas/lenguajes.svg" width="49%" alt="Lenguajes más usados">
  <br>
  <img src="https://raw.githubusercontent.com/MrDoniz/MrDoniz/refs/heads/estadisticas/meses.svg" width="49%" alt="Contribuciones por mes">
  <img src="https://raw.githubusercontent.com/MrDoniz/MrDoniz/refs/heads/estadisticas/dias.svg" width="49%" alt="Contribuciones por día de la semana">
</p>

<br>

<p align="center">
  <img src="assets/pie.svg" width="100%" alt="Hecho en Tenerife, entre el Teide y el Atlántico">
</p>
