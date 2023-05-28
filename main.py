import argparse
import os
import re

import fetcher
from model import VideoStatus, Subscription, Policy, Retention
from subscription_manager import SubscriptionManager

CHANNEL_URL = './/{http://www.w3.org/2005/Atom}link[@rel="alternate"]'

CHANNEL_NAME = '{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name'

ATOM_LINK_REL_ALTERNATE_ = "{http://www.w3.org/2005/Atom}link[@rel='alternate']"

ORG_ATOM_TITLE = "{http://www.w3.org/2005/Atom}title"

database_file = "database.db"


def delete_database():
    if os.path.isfile(database_file):
        os.remove(database_file)
        print('Deleting database...')
    else:
        print("Error: file not found.")


def create_database():
    if os.path.isfile(database_file):
        print('Database file already exists')
    else:
        # Create the database if it doesn't exist
        manager.recreate_database()
        print('Creating database...')


if __name__ == '__main__':
    manager = SubscriptionManager(database_file)
    parser = argparse.ArgumentParser()

    download_path = os.getcwd()  # download_path = manager.get_download_location()

    parser.add_argument('command', choices=['create-database', 'delete-database', 'add-subscription', 'run', 'help'],
                        help='Command to execute')

    parser.add_argument('--channel', help='Link to the Youtube channel URL')

    args = parser.parse_args()

    if args.command == 'create-database':
        create_database()

    elif args.command == 'delete-database':
        print('Deleting the database...')
        delete_database()

    elif args.command == 'add-subscription':
        print('Adding a subscription...')
        subscription_url = args.channel
        if not subscription_url:
            print('Error: Subscription URL is null')
            exit()
        valid_url = re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtube\.com)\/(user\/.+|channel\/.+|c\/.+)$',
                             subscription_url)
        subscription = Subscription(
            url=subscription_url,
            policy=Policy(
                type=Retention.DATE_BASED,
                days_to_retain=7
            )
        )
        manager.add_subscription(subscription)
        print(args.channel)

        if not valid_url:
            print('Error: Invalid YouTube channel URL')
            exit()

    elif args.command == 'run':
        if not os.path.isfile(database_file):
            print("Database does not exist. Exiting.")
            exit()

        manager.update_subscription_metadata()
        subscriptions = manager.get_all_subscriptions()

        for subscription in manager.get_all_subscriptions():
            videos = fetcher.obtain_subscription_videos(subscription)
            manager.add_videos(videos)
            manager.exclude_videos_per_policy(subscription)

            for video in manager.all_pending_videos_per_policy(subscription):
                print(f"--> Video: ID={video.id} Title={video.title} Status={video.status}")
                manager.set_video_status(video, VideoStatus.IN_PROGRESS)
                success, filepath = fetcher.download_video(download_path, video)
                if success:
                    video.status = VideoStatus.COMPLETE
                    manager.set_video_status(video, VideoStatus.COMPLETE)
                    manager.set_video_saved_path(video, filepath)
                else:
                    manager.set_video_status(video, VideoStatus.FAILED)
        exit(0)
        # TODO Need to ensure we're setting videos to excluded after they are outside of the retention policy
        # TODO Also need to delete old videos

    elif args.command == 'help':
        parser.print_help()
