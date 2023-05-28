This application lets you download a subset of a YouTube channel's videos per a retention policy. The app is written in Python and uses the public YouTube RSS Feed to retrieve channels and videos information.

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
python main.py add-subscription --channel <CHANNEL_URL>
```

This will add a subscription for the channel with the specified URL to the SQLite database.

### Run the Application

To download videos per each subscription retention policy, use the `run` command:

```
python main.py run
```
