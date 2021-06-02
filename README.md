## Run

* Setup a linkedin app first
https://www.linkedin.com/developers/apps/new

* Get the client_id and client_secret
* Add redirect_uri as `127.0.0.1`
* Click on products and add `Sign In with linkedin`
[Read through Authorization Code Flow](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?context=linkedin%2Fcontext&tabs=HTTPS)

**linkedin**
```
pipenv shell
export FLASK_APP=linkedin
export OAUTHLIB_INSECURE_TRANSPORT=1


export LINKEDIN_CLIENT_ID=<>
export LINKEDIN_CLIENT_SECRET=<>

or use direnv allow with .envrc

flask run -p 8081
```

### nginx reverse proxy on mac
```
brew install nginx
brew services start nginx

vi /usr/local/etc/nginx/nginx.conf
```

add localhost proxy pass

```
http {
...

    server {
        listen 80;
        server_name localhost;

        location / {
          proxy_pass      http://127.0.0.1:8081;
        }
    }
```

restart nginx
```
brew services restart nginx
```
