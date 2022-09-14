# MOMO(MOvie eMOji) Quiz Discord Bot 🤖🌎🗑

This is Discord Bot for MOMO(MOvie eMOji) quiz. Users guess what movie it is by looking at the emoji.

Data used for quiz were created by GPT-3 in OpenAI API.

## Developer Settings

```
$ git clone https://github.com/ainize-team/momo-bot.git
$ cd momo-bot
$ poetry install
$ pre-commit install
```

## How to execute using Docker
```
$ git clone https://github.com/ainize-team/momo-bot.git
$ cd momo-bot
$ docker build -t momo-bot .
$ docker run -d \
-e GUILD_ID=<Discord GUILD ID> \
-e TOKEN=<Discord Bot Token> \
-e DATABASE_URL=<Firebase Realtime Database URL> \
-v <Firebase Credential Directory Path>:/app/key \
momo-bot
```


## Slash Commands
```
/quiz : Start a new quiz.
```

## Demo
### /quiz
<img src="https://user-images.githubusercontent.com/62659407/187357387-ac0ac0ed-57af-4413-b3e9-1c1dd3ce59ed.png" width="30%">

### Wrong Answer
<img src="https://user-images.githubusercontent.com/62659407/187357429-85406859-6c85-4779-83c8-e07f3d866b11.png" width="30%">

### Correct Answer
<img src="https://user-images.githubusercontent.com/62659407/187357442-8bf9115b-0b94-4f48-80fd-065c933b310c.png" width="30%">

### Leaderboard
<img src="https://user-images.githubusercontent.com/62659407/187357447-a8812bee-a7a5-45eb-aa89-3a948473bd1b.png" width="30%">

