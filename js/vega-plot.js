const data = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "title": "wrapped facet",
    "description": "vega lite facet test",
    // data
    "data": {"url": "data/disk.json" },
    "mark":"point",
    "encoding":{
        "x":{"field":"datetime","type":"temporal"},
        "y":{"field":"usage","type":"quantitative","scale":{"zero":false}}
    }
  }
vegaEmbed("#gdata", data)