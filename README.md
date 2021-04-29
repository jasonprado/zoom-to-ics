# zoom-to-ics
Creates an ICS file of all meetings in a Zoom account and uploads to S3.

## Setup
### Run once without OpenFAAS
* [Get your Zoom API key and secret](https://devforum.zoom.us/t/finding-your-api-key-secret-credentials-in-marketplace/3471)
* Copy `.env.example` to `.env` and edit it.
* `python zoomtoics/zoomtoics.py`

### Run automatically in OpenFAAS and Kubernetes
Assuming you have `faas-cli` and `kubectl` configured and working.
* `faas-cli secret create zoomtoics-keys --from-file=.env`
* `faas-cli deploy -f stack.yml`
* If `cron-connector` is installed, the function will execute hourly.

### Build your own image
* `export DOCKER_USER=<your docker.io username>`
* `faas-cli publish -f stack.yml --platforms linux/arm/v7,linux/amd64`
* `faas-cli deploy -f stack.yml`
