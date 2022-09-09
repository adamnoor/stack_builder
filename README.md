# Stack Builder


## Introduction

Stack Builder is a python application that reads a CSV file of unique players and creates a database of all of the unique combinations of nine players that are possible from that CSV file according to a set of validation rules.  Once the database is complete, the user will be able to filter a subset of these combinations and write this subset to a CSV file.



## Input CSV file

In order for the application to run, a file named players.csv must exist in the input_files folder.

- The schema of the players.csv file must be:
  - name_id: String
  - position: String
  - salary: Int
  - projection: Float
  - ratio: Float 



## Database

When the user selects the button to create the database, a table named rosters must be created using the players.csv file following the following validation rules:

- The schema for the rosters table must be:
  - qb: String
  - rb1: String
  - rb2: String
  - wr1: String
  - wr2: String
  - wr3: String
  - te: String
  - dst: String
  - fx: String
  - budget: Int
  - projection: Float
  - ratio: Float

- Each row must contain exactly nine unique players and must contain:
  - Exactly one player with the position of QB
  - Exactly one player with the position of DST
  - At least one player and at most two players with the position of TE
  - At least two players and at most three players with the position of RB
  - At least three players and at most four players with the position of WR
- The “qb” column must contain one player_id associated with a position of QB
- The “rb1” column must contain one player_id associated with a position of RB
- The “rb2” column must contain one player_id associated with a position of RB
- The “wr1” column must contain one player_id associated with a position of WR
- The “wr2” column must contain one player_id associated with a position of WR
- The “wr3” column must contain one player_id associated with a position of WR
- The “te” column must contain one player_id associated with a position of TE
- The “dst” column must contain one player_id associated with a position of DST
- The “fx” column must contain one player_id associated with a position of RB, WR or TE
- The “budget” column must contain the sum of the salaries associated with all of the players from the row.  This number must not exceed 50000
- The “projection” column must contain the sum of the projections associated with all of the players from the row. 
- The “ratio” column must contain the sum of the ratios associated with all of the players from the row.
- Each group of nine players must be a unique combination (not permutation)



## Output CSV file

The user is able to filter the rosters table once it exists by selecting a qb, and dst that must be in the grouping as well as any other players that should or shouldn’t be involved in the grouping.  The user should have the ability to see how many nine player groups the filter creates as well as the option to write the results to a CSV file that will go into a folder named output_files.



## User Interface

The user interface for this application is a simple column of basic widgets using tkinter.  A widgets used are:

  - A label to let users know the results when a function has completed
  - A button to allow users to create the rosters table in a database from the players.csv file
  - A label to let users know the last time the rosters table was updated
  - A button to allow users to get statistics from the latest filter done by the user
  - A label showing the statistic: Number of combinations
  - A label showing the statistic: Highest ratio
  - A label showing the statistic: Highest projection
  - A textfield to let users input the QB to include in the filtered combinations
  - A textfield to let users input the DST to include in the filtered combinations
  - A textfield to let users input any RB, WR or TE to include in the filtered combinations
  - A textfield to let users input any RB, WR or TE to exclude in the filtered combinations
  - A button to let users filter the rosters table based on the user inputs
  - A button to let users write the filtered combinations to a CSV file
  - A label showing the number of players that exist of the players.csv file
  - A label showing a list of all the names of the players that exist on the players.csv file with an id that can be used for the user to filter



## Sample Data

Four csv files are provided as sample data:
  - small.csv- Sample data with:
    - 35 players
    - 2,830,710 potential combinations
    - 2,358,561 valid combinations
  - medium.csv- Sample data with 
    - 41 players
    - 12,367,440 potential combinations
    - 11,347,990 valid combinations
  - large.csv- Sample data with:
    - 48 players
    - 109,452,276 potential combinations
    - 106,408,075 valid combinations
  - players.csv- Real world data with:
    - 43 players
    - 19,600,810 potential combinations
    - 16,713,091 valid combinations

To run files named small.csv, medium.csv or large.csv, first rename the players.csv file to something else and then rename the file you’ve selected to players.csv.  

