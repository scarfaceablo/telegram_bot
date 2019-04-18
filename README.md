### Telegram bot sends news every 4 hours during day
Deployment is done via kubernetes (GCP Kubenertes engine)
Change this in kube_deploy.yaml 
      schedule: "30 7,19 * * *"
  to schedule as you wish.

#### Config yaml example
* telegram:
  * bot_token: '765976228:AAFG2LpVm26q7yys1WeZF5fdbyl84bye2TE'
  * bot_chat_id: '685157744'

* api_keys:
  * worldcoin_key: "UgFCk4Ee6sVAHjKveMe8mzWwVrDboQ"
  * weather_api_key: "df2a9f94e5e9c1436fe3cbc0cb150e53"