This is a Command Line Interface (CLI) application that allows you to create, manage, and monitor your YouTube
subscriptions. The app is written in Python and uses the YouTube Data API to retrieve information about channels and
videos.

## Prerequisites

To run this app, you need to have the following:

- Python 3.5 or higher

## Installation

1. Clone the repository to your local machine
2. Install the required packages with the following command:

   ```
   pip install -r requirements.txt
   ```

## Usage

The CLI app has the following commands:

- `create-database` - Creates a new SQLite database
- `delete-database` - Deletes an existing SQLite database
- `add-subscription` - Adds a new YouTube channel subscription
- `run` - Runs the subscriber application
- `help` - Shows the help message

This will add a subscription for the channel with the specified URL to the SQLite database.

### Create a Database

To create a new SQLite database, use the `create-database` command:

```
python main.py create-database
```

This will create a new SQLite database with the necessary tables.

### Delete a Database

To delete an existing SQLite database, use the `delete-database` command:

```
python main.py delete-database
```

This will delete the SQLite database and all of its contents.

### Add a Subscription

To add a new subscription to your YouTube channel, use the `add-subscription` command. You will need to provide the
channel URL as an argument:

```
python main.py add-subscription --channel https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw
```

### Run the Application

To download videos per the subscription retention policy, use the `run` command:

```
python main.py run
```
