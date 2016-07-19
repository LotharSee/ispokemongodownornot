# Pokémon GO server status - Datadog metric reporter

## How to run it?

- Use `env.example` to create a `env` file with your own credientials. `PGO_AUTH` is either `google` or `ptc`.
- Build the image `docker build -t pgo-check .`
- Run a container the first time `docker run -it --name pgo-check --env-file ./env pgo-check`
- It went well? Now you can just restart the container to run the check again `docker start -i pgo-check`
- Want to report it periodically? Put int in a `cron`, `watch` or whatever...


## Contributors

Thanks to [Datadog folks](http://datadoghq.com) for the dashboard and the check, and to [Ruben Vereecken](https://github.com/rubenvereecken) for his API!
