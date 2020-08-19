# URL Shortener Challenge

> I've decided to make this as simple as possible because of time constraints
>and the challenge's specs not containing too many requirements...

### How to run
The project is ready to be used with docker-compose, having it installed, clone
the project and run `docker-compose up --build` and everything should be working
automagically;

### How to use
As per requirement, the first page allows for shortening a url as well as expanding a shortened one.

With the docker containers running, go to `http://localhost:8000` on your browser, 
fill up the `FULL URL` field and hit the submit button beside. The
resulting `shortened code` will appear below in the form of a shortened url you can use
to be redirected **to** your `full url`.

If you have a code and you want to expand it, simply add it to the Shortened URL field and hit the
submit button by its side to see the full expanded url in the result area below.

As any url shortener server, hitting its url with the shortened code will get you redirected
to its origin.
> e.g.: Add `https://google.com` on the `Full URL` field and hit its submit button, then, copy
>the `result` that will appear and paste it on your browser's address bar and hit `enter`. This
>will get you redirected to google.

### Development
Running the project with the included docker-compose file will run django with `gunicorn`, which
is intended for production-like-environments.

To run in development mode, run `docker-compose run --rm -p 8000:8000 django start-dev.sh`

In order to allow for more customization some settings can come from a `.env` file on the root dir,
such as `DATABASE_URL`, `SECRET_SAUCE` (django's secret settings) and others you may want to include
yourself using `env(VARIABLE_NAME)` under the settings file.
> While trying to generate migrations (without docker) you may need to create this file with the `SECRET_SAUCE` variable.
> or export the env var otherwise.
>
> Of course the same can be done using docker using `docker-compose run --rm django python manage.py makemigrations` which won't need any env variables.

### Tests
To run the tests one could use docker as well, running `docker-compose run --rm django python manage.py test`

### What's next
I think it'd be nice to include validators such as URLValidator on the Full URL field
and some custom 404 page for when the client tries to find a non existing shortened url as
well as their respective tests.