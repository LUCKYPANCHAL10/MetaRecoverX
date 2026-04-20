import sys
sys.path.insert(0, '/home/lucky_panchal/Downloads/MetaRecoverX/src')

from app import MetaRecoverXApp
from pathlib import Path
from datetime import datetime

IMAGE = '/home/lucky_panchal/test_btrfs.img'
OUTPUT = f'/home/lucky_panchal/recovered_btrfs/session_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

Path(OUTPUT).mkdir(parents=True, exist_ok=True)
print(f"Output folder: {OUTPUT}")

app = MetaRecoverXApp()
session_id = app.create_session(IMAGE, OUTPUT)
print(f"Session ID: {session_id}")

# Step 1 - Detect filesystem
app.detect_filesystem(session_id)

# Step 2 - Recover deleted files
app.recover_deleted_files(session_id)

# Step 3 - Carve files
app.carve_files(session_id)

# Step 4 - Combine results
app.deduplicate_and_combine(session_id)

# Step 5 - Generate report
report_path = app.generate_report(session_id, format='pdf')
print(f"Report saved: {report_path}")

# Summary
info = app.get_session_info(session_id)
print(f"\nFilesystem : {info['fs_type']}")
print(f"Recovered  : {info['recovered_files_count']}")
print(f"Carved     : {info['carved_files_count']}")
print(f"Output     : {OUTPUT}")
