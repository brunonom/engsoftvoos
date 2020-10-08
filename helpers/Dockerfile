FROM lachlanevenson/k8s-kubectl as kubectl

FROM node:8
RUN npm i -g ejs-cli
COPY --from=kubectl /usr/local/bin/kubectl /usr/local/bin/kubectl
