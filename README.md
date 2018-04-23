# CHOSEN SHOWS SMS

this is a work in progress sms app for discovering music and art events from the bostonhassle.com events calendar.



## first iteration
user texts music, art, or film
and receives an upcoming event listing.

each received + replied message is saved, so new listings can be sent on subsequent messages from a user.

### simple parsing scenarios
string match `today, tonight, tomorrow, monday,` etc
to create a date time to filter by

> what's going on tonight?

> where is the *artist or event name* show?

> electronic music


wp-json api documentation for tribe events calendar
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


## additional feature ideas
outbound notifications
  - users opt to receive notifications when a show is added with a given tag
  - a daily task runs to request shows from the hassle api,
  - - save new events to this apps database and trigger sms notifications (and save users who have received notification about this show)


users can login to a settings config page associated with their phone number to adjust their message settings
- when to get notifications (day of, day before, week before)
-
