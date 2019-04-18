### Telegram bot sends news every 4 hours during day
Deployment is done via kubernetes (GCP Kubenertes engine)
Change this in kube_deploy.yaml 
      schedule: "30 7,19 * * *"
  to schedule as you wish.