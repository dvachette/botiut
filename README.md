# Bot IUT EDT

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://choosealicense.com/licenses/gpl-3.0/)  

## Purpose
This code is intended to be used by a discord bot to help students who struggle with their timetable.

It will be integrated in the IUT server


## Fonctionality
- See timetables in a given time range
- Filter for the next course of a given subject
- Recieve a notification in case of changes in the incoming week
- get the daily timetable each morning

## Commands
### Get a schedule in a given time range
`/edt get <start> <end> <?group:user.@group>`

**Params**

- `start` : (required) : The begining date, in 'YYYY-MM-DD' format (ISO 8601)
- `end` : (required) : The end date, in 'YYYY-MM-DD' format (ISO 8601)
- `group` : (optional) : The required group (default is the runner's group) 

### Get the next course of a given subject 
`/edt next <subject> <?group:user.@group>`

**Params**
- `subject` : (required) : the targeted subject
- `group` : (optional) : The required group (default is the runner's group)

