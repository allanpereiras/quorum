import os
from django.apps import apps
from django.db import IntegrityError
from django.core.management.base import BaseCommand
import pandas as pd

# Dictionary to map model names to the file names
FILES = {
    "Legislator": "legislators_(2).csv",
    "Bill": "bills_(2).csv",
    "Vote": "votes_(2).csv",
    "VoteResult": "vote_results_(2).csv",
}


class Command(BaseCommand):
    help = "Load sample data of Legislators, Bills, Votes and VoteResults"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--folder_path",
            type=str,
            default="bills/management/samples",
            help="Folder path (default: bills/management/samples)",
        )
        parser.add_argument(
            "-f",
            "--files",
            type=dict,
            default=FILES,
            help=f"Dictionary mapping models to files (default: {FILES})",
        )

    def handle(self, *args, **options):
        folder_path = options["folder_path"]
        files = options["files"]

        self.validate_arguments(folder_path, files)

        for model_name, filename in files.items():
            # Dynamically import the model using get_model
            model_class = apps.get_model("bills", model_name)
            df = pd.read_csv(f"{folder_path}/{filename}")

            created = []
            # Iterate through each row of data
            for index, row in df.iterrows():
                try:
                    # Create the instance with data from the row
                    obj = model_class(**row.to_dict())
                    obj.save()
                    created.append(obj)
                except IntegrityError as e:
                    # Handle potential foreign key constraint errors
                    self.stderr.write(
                        f"Error creating objects from {filename} "
                        f"at row {index+1}: {e}"
                    )
            self.stdout.write(
                f"Successfully created {len(created)} objects from {filename}"
            )

    def validate_arguments(self, folder, files) -> None:
        # Validate folder path
        if not os.path.exists(folder):
            raise ValueError(f"Folder path '{folder}' does not exist.")

        # Check if all files exist in the folder path
        for filename in files.values():
            full_path = os.path.join(folder, filename)
            if not os.path.exists(full_path):
                raise ValueError(f"File '{filename}' not found in '{folder}'.")
