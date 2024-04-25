import os
from django.apps import apps
from django.db import IntegrityError
from django.core.management.base import BaseCommand
import pandas as pd


class Command(BaseCommand):
    """
    Command to load the sample data provided for Legislators, Bills, Votes,
    and VoteResults.
    """

    help = "Load sample data from CSV files into the corresponding models."

    def add_arguments(self, parser):
        """
        Adds arguments to the command parser for folder path and file mappings.
        This method is intended to allow future loads using other CSV files.
        """

        parser.add_argument(
            "-p",
            "--folder_path",
            type=str,
            default="bills/management/samples",
            help="Folder path containing the data files (default: bills/management/samples)",
        )
        parser.add_argument(
            "-f",
            "--files",
            type=dict,
            default={
                "Legislator": "legislators_(2).csv",
                "Bill": "bills_(2).csv",
                "Vote": "votes_(2).csv",
                "VoteResult": "vote_results_(2).csv",
            },
            help="Dictionary mapping model names to CSV file names (default: %(default)s)",
        )

    def handle(self, *args, **options):
        """
        Reads data from CSV files and creates objects for the proper models.

        Handles folder path validation, file existence checks,
        and potential integrity errors. Provides informative output on
        successful creations and encountered errors.
        """

        folder_path = options["folder_path"]
        files = options["files"]

        self.validate_arguments(folder_path, files)

        created_objects = []
        for model_name, filename in files.items():
            model_class = apps.get_model("bills", model_name)
            filepath = os.path.join(folder_path, filename)

            df = pd.read_csv(filepath)
            for index, row in df.iterrows():
                try:
                    obj = model_class(**row.to_dict())
                    obj.save()
                    created_objects.append(obj)
                except IntegrityError as e:
                    self.stderr.write(
                        f"Error creating objects from {filename} "
                        f"at row {index + 1}: {e}"
                    )

        self.stdout.write(
            f"Successfully created {len(created_objects)} objects from all files."
        )

    def validate_arguments(self, folder_path, files):
        """
        Validates the provided folder path and files existence within it.

        Raises ValueErrors with informative messages for invalid paths or
        missing files.
        """

        if not os.path.exists(folder_path):
            raise ValueError(f"Folder path '{folder_path}' does not exist.")

        for filename in files.values():
            full_path = os.path.join(folder_path, filename)
            if not os.path.exists(full_path):
                raise ValueError(f"File '{filename}' not found in '{folder_path}'.")
