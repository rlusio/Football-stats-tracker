from django.core.management.base import BaseCommand
from all_players.models import Competitions
import logging
import csv
import os

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = "Fetch and save matches from Football-Data API"
    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
        file_path_2 = os.path.join(data_folder,'competitions_ids.csv')
        if not os.path.exists(file_path_2):
            self.stdout.write(self.style.ERROR(f"File {file_path_2} not found."))
            return
        try:
            with open(file_path_2,'r',encoding='utf-8') as file:
                reader = csv.DictReader(file)  
                for row in reader:
                    c = row.get('Competition', 'Unknown')
                    Competitions.objects.update_or_create(Competitions = ['Competition'])
                    self.stdout.write( self.style.SUCCESS(f"Processed {c}"))
        except Exception as e:
            logger.error(f"Failed to load matches from file: {e}")
            self.stdout.write(self.style.ERROR(f"Error loading matches: {e}"))
