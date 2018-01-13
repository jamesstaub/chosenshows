# CHOSEN SHOWS SMS

this is an sms app for discovering music and art events from the bostonhassle.com events calendar.

## first iteration
user texts music, art, or film
and receives an upcoming event listing.

each received + replied message is saved, so new listings can be sent on subsequent messages from a user.

### simple parsing
string match `today, tonight, tomorrow, monday,` etc
to create a date time to filter by


wp-json api for tribe events calendar
`http://bostonhassle.com/wp-json/tribe/events/v1/doc`








to run and build, follow [heroku django tutorial](https://devcenter.heroku.com/articles/getting-started-with-)




## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org). Also, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pipenv install

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
