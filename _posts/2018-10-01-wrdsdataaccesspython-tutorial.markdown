---
title: "WRDS Data Access via the Python API"
date: 2018-10-01 00:00
pillar: academic
series: code
topic: tutorial
summary: "Setting up a .pgpass file and running your first CRSP queries from Python."
tags: ["finance", "research", "python"]
---

## Prerequisites

* An active Wharton Research Data Services (WRDS) account
* Python 2.7+ or 3.0+
* The ```wrds``` Python library (install it with ```pip install wrds```)

## Setup

### Create the .pgpass File

On a Mac, create the ```.pgpass``` file under ```/Users/username``` with the following line:

```unix
wrds-pgdata.wharton.upenn.edu:9737:wrds:your_username:your_password
```

Replace your_username and your_password with your WRDS username and password.

#### Restrict File Permissions

```chmod 600 ~/.pgpass```

## Getting Started

With the profile set up, you can access your WRDS account through the Python API:

```python
import wrds
## provide your username 
db = wrds.Connection(wrds_username='username')

## Here is an example to get DOW daily index value.
db.raw_sql('SELECT date,dji FROM djones.djdaily limit 10')

## Get data from CRSP
crsp = db.raw_sql('select cusip,permno,date,bidlo,askhi from crsp.dsf LIMIT 100')
```

