# Deployments

This directory contains the integration testing deployment artifacts for development and integration testing purposes.

## Helm Deployment

* Helm Charts for MongoDB: https://artifacthub.io/packages/helm/bitnami/mongodb
* Kubectl Quick Ref: https://kubernetes.io/docs/reference/kubectl/quick-reference/
* Default Mongo Values Template: [values.yaml](./values.yaml)

### Quick Deploy

```
helm install my-release oci://registry-1.docker.io/bitnamicharts/mongodb

```

TODO: add specific values and init scripts


MongoDB&reg; can be accessed on the following DNS name(s) and ports from within your cluster:

    my-release-mongodb.default.svc.cluster.local

To get the root password run:

    export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace default my-release-mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 -d)

To connect to your database, create a MongoDB&reg; client container:


Then, run the following command:
    mongosh admin --host "my-release-mongodb" --authenticationDatabase admin -u $MONGODB_ROOT_USER -p $MONGODB_ROOT_PASSWORD

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/my-release-mongodb 27017:27017 &
    mongosh --host 127.0.0.1 --authenticationDatabase admin -p $MONGODB_ROOT_PASSWORD

**Note that the default admin user is 'root'**


### Mongo DB Notes

* Compass is the MongoDB GUI: https://www.mongodb.com/products/tools/compass
