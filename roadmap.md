# Roadmap

## V1.0

* Find bus/... data across every API requests
* Return JSON formatted data
* Create generic API return model (needed for app)
* Generic method that parse GTFS data
* Python doc
* Swagger API (auto generated if possible)
* Some tests ~~+ actions~~
* ~~éUse https://github.com/google/yapf + actions~~
* ~~Link to Codecov~~

### API architecture

```
GET /{city} -> []transport_type[]type{
      ...type_details
}

GET /{city}/{transport_type} -> []type{
      ...type_details
}

GET /{city}/{transport_type}/{line} -> {
      []stop{
            ...stop_details
      },
      []type{
            ...type_details
      }
}

GET /{city}/{transport_type}/{type_id/ref} -> type{
      ...type_details
}

GET /{city}/{transport_type}/{stop_id/ref} -> {
      ...stop_details
}
```

## V2.0

* Create middleware that will call the correct method for each given parameters (for example, auxerre -> method that will call the French gov API, paris -> method that will extract data from GTSF files)
