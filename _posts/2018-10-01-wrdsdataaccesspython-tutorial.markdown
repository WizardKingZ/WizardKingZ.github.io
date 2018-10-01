---
title: "Tutorial: WRDS Data Access Via Python API"
layout: post
blog: true
date: 2018-10-01 00:00
headerImage: false
tag:
- finance
- research
- python
star: false
category: blog
author: johnewzhang
description: "Tutorial: WRDS Data Access Via Python API"
---

## Prerequisites

* An active account with the Warton WRDS Web Service
* Python 2.7+ or 3.0+
* ```wrds``` Python library; if you don't have it, install it (```pip install wrds```)

## Setup

### To create .pgpass file

For Mac user, you can create the ```.pgpass``` under ```/Users/username```.

```wrds-pgdata.wharton.upenn.edu:9737:wrds:your_username:your_password```

where your_username is your WRDS username and your_password is your WRDS password. 

#### To restrict file permissions:

```chmod 600 ~/.pgpass```

## Getting Started

Now, you have set up your WRDS profile and can access your WRDS account through the Python API.

```python
import wrds
## provide your username 
db = wrds.Connection(wrds_username='username')

## Here is an example to get DOW daily index value.
db.raw_sql('SELECT date,dji FROM djones.djdaily limit 10')

## Get data from CRSP
crsp = db.raw_sql('select cusip,permno,date,bidlo,askhi from crsp.dsf LIMIT 100')
```

Enjoy :simple_smile:

