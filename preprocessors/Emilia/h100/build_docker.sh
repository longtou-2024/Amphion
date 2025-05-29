docker build -t longtou/amphion:emilia-pipe .
docker tag longtou/amphion:emilia-pipe us-central1-docker.pkg.dev/prod-ai-project/tts/amphion:emilia-pipe

#docker run -it --runtime=nvidia longtou/amphion:emilia-pipe /bin/bash
#gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://us-central1-docker.pkg.dev
#docker push us-central1-docker.pkg.dev/prod-ai-project/tts/amphion:emilia-pipe
