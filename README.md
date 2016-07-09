[![Build Status](https://travis-ci.org/biomaks/transit-bot.svg?branch=master)](https://travis-ci.org/biomaks/transit-bot)

# transit-bot

api.ini file required in the root of project with following content:
    
    [secret]
    api-key: <transit api key>
    bot-token: <your telegram bot token>
    

build, create container, commit and push

    docker build -t biomaks/transit-bot .
    docker run -d --name bot biomaks/transit-bot
    docker commit <container_id> biomaks/transit-bot:latest
    docker push biomaks/transit-bot:latest

add ini file:

    docker cp api.ini bot:/application