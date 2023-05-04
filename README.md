# Instashare "description"

## Github Actions

### Build Workflow

The build workflow is configured to build and push into his repository the docker image of the application. The workflow is triggered when a push is made into the master, develop or tag. The nomenclature for tagging the container is <branch>:<short hash of commit>The build workflow is configured to build and push into his repository the docker image of the application. The workflow is triggered when a push is made into the master, develop or tag. The nomenclature for tagging the container is ```instashare:<branch>-<short hash of commit>```, but if the container is master the configuration will push two tags, the first is ```instashare:<short hash of commit>``` (without branch) and ```instashare:latest``` (to keep continuously updated the last commit on latest tag).
