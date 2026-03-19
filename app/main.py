from db import create_tables
from services import save_selected_categories


from datetime import datetime
print(f"[{datetime.now()}] JOB START")

create_tables()
save_selected_categories()

print(f"[{datetime.now()}] JOB END")