# Currencies

App exposing endpoint for currencies conversion. Uses [exchangeratesapi.io](https://exchangeratesapi.io/) for getting current currency exchange rates.

## Tech stack
* Django and Django REST Framework - for out of the box validation and API setup
* requests - for integration with external API
* pytest - for writing and running tests in elegant way

## App setup
Install `Docker` and run:
```
docker-compose up
```

## API usage
Example endpoint call:

*Notice excluded trailing slash!*

```
POST http://localhost:8000/convert

{
  "currency_1": "PLN",
  "currency_2": "EUR",
  "amount": 100.5
}
```

## Running tests
Full test suite can be run with `docker-compose exec web pytest`. To exclude tests testing integration with external API run:
```
docker-compose exec web pytest -m 'not external'
```
