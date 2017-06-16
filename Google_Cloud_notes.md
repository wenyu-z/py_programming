# Google Cloud Notes
## Run Jupyter notebooks in a cluster
Originally I tried to use [this link](https://cloud.google.com/dataproc/docs/tutorials/jupyter-notebook) for a SLB project, but I'm not an owner of the project thus don't have the authority to create an SSH tunnel using `gcloud compute ssh` command. Note, I was able to use that link on my personal MacBook and connect to my personal GCP project.



Eventually I used [this link](https://cloud.google.com/compute/docs/instances/connecting-to-instance) as a reference and used PuTTY to connect successfully on Windows. The steps are:

1. Generate SSH key-pair using PuTTYgen
2. Add the key to the project metadata page
3. Use the external IP of the master instance to connect in PuTTY
   1. In Connection-SSH-Auth, use the private key file
   2. In Connection-Tunnels, use Source port `8900` and Destination `localhost:8888`
4. Run `jupyter notebook` in the PuTTY window
5. Connect via http://localhost:8900/tree?token=token (whatever the token is) in a browser

## Create cluster with additional parameters
The minimum set of parameters is provided in [the first link](https://cloud.google.com/dataproc/docs/tutorials/jupyter-notebook) from the previous section. Eventually these are used in addition:
```
gcloud dataproc clusters create cluster-2  \
--project slb-it-ads-tlm-dev --bucket cluster-2 --num-workers 4  \
--initialization-actions gs://dataproc-initialization-actions/jupyter/jupyter.sh \
--metadata "JUPYTER_CONDA_PACKAGES=numpy:pandas:scikit-learn:matplotlib" --metadata "MINICONDA_VARIANT=2"
```
Defined above: number of workers, preinstalled packages, Miniconda version (which decides Python version)
