#### Build
<pre>
Build image with docker and push the image to your docker repo.
</pre>

#### Telegram bot sends news every 4 hours during day
<pre>
Deployment is done via kubernetes (GCP Kubenertes engine)
Change this in kube_deploy.yaml 
      schedule: "30 7,19 * * *"
  to schedule as you wish.
</pre>

#### Config yaml example
<pre>
telegram:
  bot_token: '*******'
  bot_chat_id: '*******'

api_keys:
  worldcoin_key: "********"
  weather_api_key: "********"
</pre>
