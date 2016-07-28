webcamp16
=========

Python async web-frameworks benchmark and code examples for aiohttp project and
aio-libs.

## Benchmark 

I'm using [wrk](https://github.com/wg/wrk) tool with custom lua script that
will create resulting csv file and then build a chart from it with 
[d3](https://d3js.org).

```
make docker
make lab
make bench
```

Examples
========

For all code examples from the presentation see *demo* directory. 
