# osrs-tracker

Parsing OSRS Hiscores periodically into csv database 

## Features

- Fetches Oldschool Runescape HiScores from the official website
- Stores these data in a csv file for each listed user under the specified data directory

## Prerequisites

- pandas
- requests

## Usage

Simply run the script, providing the directory in which the data will be stored as the first argument, and a list of usernames following.

```
python3 fetch.py datadir user1 user2 ... userN
```

### Cron Jobs

Perhaps the best way to use this script is to set up a cron task to run at a specified interval, for example every 15 minutes.

```
*/15 * * * * python3 ~/fetch.py ~/HiScores/ user1 user2 ... userN
```

Note that the official HiScores only refresh as the player logs out, and sometimes do not do so for longer periods as long as 6 hours at a time.

## TODO:

- Consider encoding into a different format
- Compression?
- safeguard against inserting garbage data (http response) into csv file when an error occurs. (unable to grab hiscores data -> receive http response)

## Issues:

- The script must be updated when new fields are added to the OSRS HiScores, as the API does not return a table header
- When an error occurs, i.e. timeout, an http response can be returned instead of csv data, potentially causing garbage data to be inserted into the csv

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
