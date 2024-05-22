# ELM327Drive

Tool to tap into OBDII port of your vehicle to monitor its data.

<!-- Image -->

## Dependencies

```
pip install -r requirements.txt
```

## Usage

Plug ELM327 module...

```
+--------+  USB  +------+  OBDII  +-------+ 
|COMPUTER| ----> |ELM327| ------> |VEHICLE|
+--------+       +------+         +-------+
```

```
git clone git@github.com:maker-ATOM/ELM327Drive.git

cd ELM327Drive

python3 main.py
```
---

Have something to improvise the codebase? do consider creating a Issue.