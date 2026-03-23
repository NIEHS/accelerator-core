# Sample query by filter


### All records that came from cedar

```json

{"technical_metadata.original_source_link":"cedar"}

```

### All records that came from cedar that were disseminated to cafe

```json

{
  "technical_metadata.original_source_link": "cedar",
  "technical_metadata.dissemination_endpoints.endpoint_type": "cafe"
}

```

### All records that came from cedar that were not disseminated to cafe

```json

{
  "technical_metadata.original_source_link": "cedar",
  "technical_metadata.dissemination_endpoints": {
    "$not": {
      "$elemMatch": {
        "endpoint_type": "cafe"
      }
    }
  }
}



```
