import argparse
import logging
import os

from prettytable import PrettyTable

import dao
import fetcher
from dao import SubscriptionManager
from model import VideoStatus, Subscription, Policy, Retention, Video

logging.basicConfig(level=logging.INFO)

download_path = os.getcwd()  # download_path = manager.get_download_location()

if __name__ == '__main__':
    manager = SubscriptionManager()

    parser = argparse.ArgumentParser()
    cmd_parser = parser.add_subparsers(dest="command")
    create_db_parser = cmd_parser.add_parser("create-database", help="Create a new database")
    delete_db_parser = cmd_parser.add_parser("delete-database", help="Delete the current database")
    add_sub_parser = cmd_parser.add_parser("add-subscription", help="Add a new subscription")
    add_sub_parser.add_argument("channel", type=str, help="The URL of the channel to subscribe to")
    print_subs_parser = cmd_parser.add_parser("print-subscriptions", help="Print a list of all subscriptions")
    print_videos_parser = cmd_parser.add_parser("print-videos", help="Print a list of all videos")
    run_parser = cmd_parser.add_parser("run", help="Process videos for both download and delete")
    run_parser.add_argument("--download-path", type=str,
                            help="Provide a download path instead of the current working directory")
    run_parser.add_argument("--dry-run", help="Skip downloading videos, but perform every other action as normal",
                            action="store_true")
    help_parser = cmd_parser.add_parser("help", help="Show help information")
    args = parser.parse_args()

    if args.command == "create-database":
        manager.create_database()
    elif args.command == "delete-database":
        dao.delete_database()
    elif args.command == "add-subscription":
        if args.channel:
            subscription_url = args.channel
            if not subscription_url:
                print('Error: Subscription URL is null')
                exit()
            subscription = Subscription(
                url=subscription_url,
                policy=Policy(
                    type=Retention.DATE_BASED,
                    days_to_retain=7
                )
            )
            manager.add_subscription(subscription)
        else:
            print("Please specify a channel")
    elif args.command == "print-subscriptions":
        table = PrettyTable()
        table.field_names = [Subscription.id.name, Subscription.title.name, Subscription.rss_feed_url.name,
                             Subscription.url.name]
        subscriptions = manager.get_all_subscriptions()
        for subscription in subscriptions:
            table.add_row([subscription.id, subscription.title, subscription.rss_feed_url, subscription.url])
        print(table)

    elif args.command == "print-videos":
        table = PrettyTable()
        table.field_names = [Video.id, Video.title, Video.url, Video.status, Video.saved_path]
        videos = manager.get_all_videos()
        for video in videos:
            table.add_row([video.id, video.title, video.url, video.status.name, video.saved_path])
        print(table)

    elif args.command == "run":
        dry_run = False
        if args.dry_run:
            dry_run = True
        if args.download_path:
            download_path = args.download_path

        manager.update_subscription_metadata()
        subscriptions = manager.get_all_subscriptions()

        for subscription in manager.get_all_subscriptions():
            videos = fetcher.obtain_subscription_videos(subscription)
            manager.add_videos(videos)
            manager.exclude_videos_per_policy(subscription)

            for video in manager.all_pending_videos_per_policy(subscription):
                print(f"--> Video: ID={video.id} Title={video.title} Status={video.status}")
                manager.set_video_status(video, VideoStatus.IN_PROGRESS)
                success, filepath = fetcher.download_video(download_path, video.url, dry_run)
                if success:
                    video.status = VideoStatus.COMPLETE
                    manager.set_video_status(video, VideoStatus.COMPLETE)
                    manager.set_video_saved_path(video, filepath)
                else:
                    manager.set_video_status(video, VideoStatus.FAILED)
        exit(0)
        # TODO Need to ensure we're setting videos to excluded after they are outside of the retention policy
        # TODO Also need to delete old videos

    if not args.command:
        print("Use -h or --help to see commands")
