# Server Information Routes

## Get Server Information


### Default Route

#### HTTP Method and URL

`GET http://llm.cs.tcu.edu:5000/`

#### Parameters

None

#### Example Request

```bash
curl http://llm.cs.tcu.edu:5000/
```

#### Example Response

```html
<h1>ClassifAI Engine</h1><p>Version: 3.0.3</p><p>Environment: dev</p><p>Healthcheck: OK</p><a href='https://tcu-classifai.github.io/classifAI-engine/'>Documentation</a>
```

### Healthcheck Route

#### HTTP Method and URL

`GET http://llm.cs.tcu.edu:5000/healthcheck`

#### Parameters

None

#### Example Request

```bash
curl http://llm.cs.tcu.edu:5000/healthcheck
```

#### Example Response

```json
OK
```

### Config 

#### Editing Config

To edit the config, you can edit the `config.py` file in the `src/config` directory.

Please see the [config documentation](config.md) for more information on the config file.

#### HTTP Method and URL

`GET http://llm.cs.tcu.edu:5000/config`

#### Parameters

None

#### Example Request

```bash
curl http://llm.cs.tcu.edu:5000/config
```

#### Example Response
```json
{
  "CATEGORIZATION_MODEL": "gemma",
  "ENV_TYPE": "dev",
  "SUMMARIZATION_MODEL": "huggingface",
  "TRANSCRIPTION_MODEL": "large-v3",
  "VERSION": "3.0.3"
}
```


## Authentication

### Test Authentication

#### HTTP Method and URL

`GET http://llm.cs.tcu.edu:5000/auth`

#### Parameters

Must include an API key in the header.

#### Example Request

```bash
curl -H "X-API-KEY: MYAPIKEY" http://llm.cs.tcu.edu:5000/auth
```

#### Example Response

Success:

```json
OK, 200
```

Failure:

```json
{
  "message": "Unauthorized. Pleae add a header with the key API-Key and your secret key."
}
```
401


