# Redmine CSV Sync

Utility to sync the [redmine][] project management system with a CSV file.

## Installation

1. clone this repository as redmine_sync
2. pip install redmine_sync

##Usage

1. Generate csv of issues from the database

   > redmine_sync <url> <api_key> --filename tasks.csv

2. Update tasks.csv using the A,E or D flags (see redmine_sync -h) and resync as in 1



[redmine]: http://www.redmine.org

## License

Creative Commons Share-Alike Non-Commercial
