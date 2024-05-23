# ELM327Drive

Tool to tap into OBDII port of your vehicle to monitor its data.

https://github.com/maker-ATOM/ELM327Drive/assets/87944335/306df5e6-f8a4-40a5-bcec-2e5cdeaec0f1

## Install Dependencies

```
pip install -r requirements.txt
```

## Usage

Plug [ELM327](https://www.elm327.com/) module...

```
+--------+  USB  +------+  OBDII  +-------+ 
|COMPUTER| ----> |ELM327| ------> |VEHICLE|
+--------+       +------+         +-------+
```

```
git clone git@github.com:maker-ATOM/ELM327Drive.git

cd ELM327Drive/dashboard

python3 main.py
```
---

Have something to improvise the codebase? do consider creating a Issue.
