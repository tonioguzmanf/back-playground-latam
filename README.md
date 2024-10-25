# back-playground-latam

##### 0.

[Crea](https://console.cloud.google.com/projectcreate) un proyecto de Google Cloud Platform o reutiliza alguno 
existente.

##### 1.

Abre el [IDE](https://ide.cloud.google.com/) del Google Cloud Shell.

##### 2.

Asigna tu proyecto ejecutando el siguiente comando en la terminal: 
```
gcloud config set project YOUR_PROJECT_ID
```

##### 3.

Clona este repositorio ejecutando el siguiente comando en la terminal:
```
git clone https://github.com/tonioguzmanf/back-playground-latam
```

##### 4.
* Habilita las APIs de Cloud Run y Cloud Build.
```
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com
```

* Otorga los permisos necesarios a Google Cloud Build para generar el artefacto a desplegar a partir de tu código fuente.
```
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member=serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role=roles/cloudbuild.builds.builder
```

##### 5.
Despliega tu aplicación ejecutando el siguiente comando en la terminal:
```
gcloud run deploy YOUR_SERVICE_NAME --source .
```

### ¡Felicidades. Ya tienes tu backend service listo para atender las peticiones hacoa Gemini API!
