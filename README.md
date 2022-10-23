# Lottery-system

Lottery-system allows users to register and bet on everyday repeating lottery.

## Getting started

In order to run the app, git clone this project and execute:

```shell
docker-compose up -d --build
```

The code above creates and starts the container image. Once it's finished, the lottery-sys is ready to use.

## Functional features

* Lottery-system allows anyone to register as a lottery participant. Each participant is able to submit as many lottery
  ballots that day's lottery that isn’t yet finished.

* Each day at midnight the lottery event is considered closed and a random lottery winner will be selected from all
  participants for the day.

* All users are able to check the winning ballot for any specific date.

* The service persists the data regarding the lottery to a PostgresSQL database.

## Endpoints

Available endpoints and examples:

* POST /user
    * Description: Endpoint to create user
    * Body (data-raw) -> username: user's unique username in the system
    * Returns: Request status

```shell
curl curl --location --request POST 'host:port/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "my_user_name"
}'
```

* POST /bet
    * Description: Place lottery ballot on ongoing lottery
    * Query params -> username: user's unique username in the system
    * Returns: Lottery ballot information (Ticket model)

```shell
curl --location --request POST 'host:port/bet?username=my_user_name' \
--header 'Content-Type: application/json'
```

* GET /winner
    * Description: Get winning ticket information of any given date
    * Query params -> date: Date in YYYY-MM-DD format
    * Returns: Request status

```shell
curl --location --request GET 'host:port/winner?day="YYYY-MM-DD"'
```