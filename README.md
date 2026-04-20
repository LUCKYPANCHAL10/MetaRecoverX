# 🔍 MetaRecoverX - Exposing what lies beneath the surface

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**MetaRecoverX** is a digital forensic investigation tool designed to help investigators uncover hidden or deleted information from digital systems. It combines filesystem metadata analysis with signature-based file carving to recover deleted files from modern Linux filesystems, extract embedded metadata from recovered evidence, and produce structured forensic reports — all within a single environment available as both a GUI and CLI.

---

## Features

### A. Core Recovery Engine

These features focus on recovering as much data as possible while preserving the integrity of digital evidence.

- **Recovery of Deleted Files:** MetaRecoverX uses a combination of metadata analysis and signature-based file carving to recover deleted files from Btrfs and XFS filesystems. This approach improves the chances of retrieving data even when the original filesystem structure is partially damaged or missing.

- **Multi-Format Support:** The recovery engine supports more than 16 different file types, including documents, images, audio, video, and archives. A signature database is used to identify and reconstruct these files from raw disk data.

- **Metadata Extraction:** MetaRecoverX extracts important file metadata such as timestamps, inode numbers, and file permissions. It can also read embedded metadata like EXIF information from images and document properties from PDFs or Office files. This information helps investigators understand the history of recovered files.

- **File Integrity Verification:** Every recovered file is assigned a SHA-256 hash. This allows investigators to confirm that the evidence has not been altered and supports proper chain of custody during investigations.

- **File Type Detection (Magic Numbers):** Files are identified using their header signatures instead of relying only on file extensions. This ensures accurate classification even when file names or extensions have been changed or removed.

### B. Forensics Suite

These features help investigators organise and review recovered evidence in a structured and practical way.

- **Interactive Timeline:** MetaRecoverX collects timestamps from recovered files and presents them in a chronological timeline. This makes it easier to see patterns of activity and understand the sequence of events on a system.

- **Keyword Search:** Investigators can search through recovered text files using specific keywords such as passwords, confidential terms, or other relevant phrases. This helps locate important information quickly.

- **Forensic Report Generator:** The platform can generate structured reports that include recovered file details, metadata, integrity hashes, and search results. Reports can be exported as PDF or CSV for documentation and further analysis.

---

## User Interfaces

### A. Command Line Interface (CLI)
A terminal-based interface designed for technical users, with progress indicators and detailed output during the recovery process.

### B. Graphical User Interface (GUI)
A desktop interface built using PyQt6 that allows investigators to perform recovery and analysis tasks through an easy-to-use visual environment.

---

## Directory Structure

```
MetaRecoverX/
├── run.py                        # Main launcher (CLI/GUI interactive entrypoint)
├── MetaRecoverX_full.py               # CLI recovery script
│
├── src/
│   ├── core/                     # Core recovery engines
│   │   ├── btrfs_parser.py       # Btrfs filesystem parser
│   │   ├── xfs_parser.py         # XFS filesystem parser
│   │   ├── file_carver.py        # File carving engine
│   │   ├── metadata_extractor.py # EXIF/PDF/Office metadata extraction
│   │   └── partition_parser.py   # Partition table detection (MBR/GPT)
│   │
│   ├── ui/                       # User interfaces
│   │   ├── cli.py                # Command-line interface
│   │   └── gui.py                # Desktop GUI (PyQt6)
│   │
│   ├── app.py                    # Main application controller
│   └── utils.py                  # Utility functions
│
├── data/
│   ├── test_images/              # Test disk images
│   └── recovered_output/         # Recovery output directory
│
├── logs/                         # Application logs
├── README.md
├── requirements.txt
├── setup.py
└── LICENSE
```

---

## Installation

### Prerequisites

- **Python**: 3.12 or higher
- **Operating System**: Linux
- **RAM**: Minimum 4GB (16GB recommended for large disk images)
- **Disk Space**: At least 500MB for recovered data
- **Permissions**: Root/Administrator access for raw disk access

### Step 1 — Install System Dependencies

Only these packages need to be installed system-wide. Everything else goes inside the venv.

#### Ubuntu / Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    libmagic-dev \
    build-essential \
    xfsprogs \
    btrfs-progs \
    git
```

#### Arch Linux
```bash
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm \
    python \
    python-pip \
    python-setuptools \
    file \
    base-devel \
    xfsprogs \
    btrfs-progs \
    git
```

#### Fedora
```bash
sudo dnf update -y
sudo dnf install -y \
    python3 \
    python3-pip \
    python3-devel \
    file-devel \
    gcc \
    gcc-c++ \
    make \
    xfsprogs \
    btrfs-progs \
    git
```

### Step 2 — Clone and Set Up the Project

```bash
git clone https://github.com/luckypanchal10/MetaRecoverX.git
cd MetaRecoverX
```

### Step 3 — Create Virtual Environment and Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Step 4 — Fix CLI Import (One-Time Step)

```bash
sed -i 's/from ..app import MetaRecoverXApp, FileSystemType/from app import MetaRecoverXApp, FileSystemType/' src/ui/cli.py
```

### One-Command Install (Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/luckypanchal10/MetaRecoverX/master/install.sh | bash
```

This script automatically checks your Python version, installs system dependencies, sets up a virtual environment, and creates `MetaRecoverX`, `MetaRecoverX-gui`, and `MetaRecoverX-cli` shortcuts in your PATH.

---

## Creating Test Disk Images

MetaRecoverX requires a raw disk image file to scan. You cannot point it at a regular folder. The steps below show how to create test images for both XFS and Btrfs, add files, delete them, and prepare the image for recovery.

### A. XFS Test Image

**Step 1 — Create a blank 512MB image file**

```bash
dd if=/dev/zero of=~/test_xfs.img bs=1M count=512
```

**Step 2 — Format it as XFS**

```bash
mkfs.xfs ~/test_xfs.img
```

**Step 3 — Mount it**

```bash
sudo mkdir -p /mnt/test_xfs
sudo mount -o loop ~/test_xfs.img /mnt/test_xfs
```

**Step 4 — Copy files into it**

```bash
sudo cp ~/Downloads/yourfile.pdf /mnt/test_xfs/
sudo cp ~/Downloads/yourimage.jpeg /mnt/test_xfs/
```

**Step 5 — Flush to disk, then delete the files**

```bash
sudo sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'

sudo rm /mnt/test_xfs/yourfile.pdf
sudo rm /mnt/test_xfs/yourimage.jpeg
```

> `sync` forces file data to be written to the image before deletion. `drop_caches` clears the memory cache so the data exists only on disk. Without these two steps, the data may never reach the image file and nothing will be recoverable.

**Step 6 — Unmount**

```bash
sudo umount /mnt/test_xfs
```

The XFS image is now ready at `~/test_xfs.img`.

---

### B. Btrfs Test Image

**Step 1 — Create a blank 512MB image file**

```bash
dd if=/dev/zero of=~/test_btrfs.img bs=1M count=512
```

**Step 2 — Format it as Btrfs**

```bash
mkfs.btrfs ~/test_btrfs.img
```

**Step 3 — Mount it**

```bash
sudo mkdir -p /mnt/test_btrfs
sudo mount -o loop ~/test_btrfs.img /mnt/test_btrfs
```

**Step 4 — Copy files into it**

```bash
sudo cp ~/Downloads/yourfile.pdf /mnt/test_btrfs/
sudo cp ~/Downloads/yourimage.jpeg /mnt/test_btrfs/
```

**Step 5 — Flush to disk, then delete the files**

```bash
sudo sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'

sudo rm /mnt/test_btrfs/yourfile.pdf
sudo rm /mnt/test_btrfs/yourimage.jpeg
```

**Step 6 — Unmount**

```bash
sudo umount /mnt/test_btrfs
```

The Btrfs image is now ready at `~/test_btrfs.img`.

---

## Running MetaRecoverX

Always activate your venv before running:

```bash
cd ~/Downloads/MetaRecoverX
source venv/bin/activate
```

---

## GUI Mode

Launch the GUI:

```bash
sudo -E venv/bin/python run.py --gui
```

### Steps Inside the GUI

**1.** Click **+ Attach Source** at the bottom left and select **Disk Image File**.

**2.** In the file picker, navigate to your home folder and select `test_xfs.img` or `test_btrfs.img`.

**3.** The **File Carving Settings** dialog will appear. All file types are selected by default (JPG, PNG, PDF, ZIP, MP3, MP4, etc.). Click **Start Scan**.

**4.** The dashboard will show a progress bar with **Carving files...** at the top. Wait for it to complete.

**5.** Once done, the dashboard updates with:
- **Total Files** — files found via metadata
- **Carved Files** — files found via signature scanning
- **File Types Breakdown** — chart showing types recovered
- **Session Information** — source path, filesystem type, status

**6.** Click **Recovered Files** in the left sidebar to see the full list of recovered files.

**7.** Click **Report Generator** in the left sidebar to export a PDF or CSV forensic report.

### Output Location

Recovered files are saved inside the project folder under:
```
data/recovered_output/YYYYMMDD_HHMMSS/
```

---

## CLI Mode

The CLI runs the full recovery pipeline in one command using `MetaRecoverX_full.py`.

### For XFS

Open `MetaRecoverX_full.py` and set the IMAGE and OUTPUT paths:

```python
IMAGE = '/home/your_username/test_xfs.img'
OUTPUT = f'/home/your_username/recovered_xfs/session_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
```

Then run:

```bash
cd ~/Downloads/MetaRecoverX
sudo -E venv/bin/python MetaRecoverX_full_xfs.py
```

### For Btrfs

{Open `MetaRecoverX_full.py` and change the IMAGE and OUTPUT paths:

```python
IMAGE = '/home/your_username/test_btrfs.img'
OUTPUT = f'/home/your_username/recovered_btrfs/session_{datetime.now().strftime("%Y%m%d_%H%M%S")}'}
```

Then run:

```bash
cd ~/Downloads/MetaRecoverX
sudo -E venv/bin/python MetaRecoverX_full_btrfs.py
```

### What the CLI Does

The script runs these steps in sequence inside a single session:

1. Creates a timestamped output folder
2. Detects the filesystem type (XFS or Btrfs)
3. Runs metadata-based recovery
4. Runs file carving on raw blocks
5. Combines and deduplicates results
6. Generates a PDF forensic report

### Sample Output

```
Output folder: /home/lucky_panchal/recovered_xfs/session_20260420_124134
Session ID: 77bbab39a511a7d1

Filesystem : xfs
Recovered  : 0
Carved     : 9
Report saved: /home/lucky_panchal/recovered_xfs/session_20260420_124134/report_77bbab39.pdf
Output     : /home/lucky_panchal/recovered_xfs/session_20260420_124134
```

### Verify Recovered Files

```bash
ls -lh ~/recovered_xfs/session_<timestamp>/
```

Example output:

```
carved_0001.jpg   22K
carved_0001.pdf  725K
carved_0002.jpg   30K
carved_0003.jpg   45K
report_77bbab39.pdf  7.1K
```

Each run creates a new timestamped folder so sessions never overwrite each other.

---

## Understanding the Results

| Metric | Meaning |
|---|---|
| Total Recovered | Files found via filesystem metadata (inode records) |
| Carved Files | Files found by scanning raw blocks for file signatures |
| Filesystem | Auto-detected as XFS or Btrfs |
| Hash Algorithm | SHA-256 applied to every recovered file for integrity |

**Why is Total Recovered 0?**
XFS and Btrfs both clear inode metadata quickly after deletion. This is expected behaviour. The file carver recovers the actual data from raw disk blocks regardless of whether metadata survived.

**Why are there extra JPGs?**
The file carver finds all JPEG signatures in the image including images embedded inside PDFs. Each embedded image is extracted separately.

---

## Quick Reference

| Task | Command |
|---|---|
| Activate venv | `source venv/bin/activate` |
| Launch GUI | `sudo -E venv/bin/python run.py --gui` |
| Launch CLI (interactive) | `sudo -E venv/bin/python run.py --cli` |
| Run full CLI recovery | `sudo -E venv/bin/python MetaRecoverX_full.py` |
| Check recovered files | `ls -lh ~/recovered_xfs/session_<timestamp>/` |
| Check logs | `cat logs/*.log` |
| Deactivate venv | `deactivate` |

---

## File System Support

### A. Btrfs (B-Tree File System)

#### Capabilities

- Parses the Btrfs superblock and tree roots to locate important filesystem structures.
- Traverses Copy-On-Write (COW) trees to identify filesystem metadata and data extents.
- Validates leaf nodes using the filesystem identifier (FSID) to ensure structural consistency.
- Supports extent-based recovery of file data stored across different blocks.
- Verifies data integrity using CRC32C checksums present in Btrfs structures.
- Performs file carving to recover deleted files directly from raw disk data when metadata is unavailable.

#### Known Limitations

- Compressed extents using zlib, lzo, or zstd are currently not decompressed during recovery.
- RAID-based Btrfs configurations may require additional handling depending on the storage layout.
- Due to the Copy-On-Write architecture, deleted metadata may disappear quickly, which reduces the time window for metadata-based recovery.

#### Recovery Mechanism

MetaRecoverX primarily relies on file carving for Btrfs recovery because of the nature of its Copy-On-Write design. When available, metadata parsing is used as a secondary method to identify file structures and improve recovery accuracy.

### B. XFS (Extended File System)

#### Capabilities

- Parses the XFS superblock to identify core filesystem configuration and layout.
- Analyses Allocation Groups (AGs) to locate filesystem structures distributed across the disk.
- Supports recovery of file information through inode analysis.

#### Known Limitations

- Advanced XFS recovery features are still under development and may not cover all edge cases.
- Some complex storage layouts or fragmented data structures may require deeper analysis beyond the current implementation.

#### Recovery Mechanism

For XFS, MetaRecoverX relies mainly on metadata parsing through inode analysis to locate file information. File carving can also be used as a supplementary method to recover data directly from disk blocks when metadata is incomplete or missing.

---

## Legal & Ethics

### Legal Disclaimer

**Important:** MetaRecoverX is developed for legitimate digital forensic investigations, security research, and educational use. The tool should only be used on systems and data where proper authorisation has been granted.

Using forensic tools without permission may violate privacy laws, organisational policies, or local regulations. Users are responsible for ensuring that they follow all applicable laws and ethical guidelines when using this software.

### Authorised Uses

- Law enforcement investigations with appropriate legal authorisation
- Corporate incident response on organisation-owned systems
- Personal data recovery on devices owned by the user
- Security research carried out with proper consent and approval
- Educational and training purposes on controlled test systems

### Unauthorised Uses

- Accessing computer systems or storage devices without permission
- Violating privacy regulations or data protection laws
- Attempting to bypass encryption or security controls without authorisation
- Modifying, destroying, or tampering with digital evidence
- Any activity that is illegal or unethical

### Ethical Guidelines

1. **Authorisation** — Always obtain proper permission before analysing any system, storage device, or dataset.

2. **Chain of Custody** — Follow proper evidence handling procedures. Every step of the investigation should be traceable.

3. **Privacy** — Respect applicable data protection and privacy laws such as GDPR, CCPA, or other regional regulations.

4. **Documentation** — Maintain clear and detailed records of all actions taken during the investigation.

5. **Integrity** — The original evidence should never be modified. Analysis should always be performed on copies or forensic images.

6. **Transparency** — Clearly describe the methods, tools, and processes used. Reports should explain how conclusions were reached so findings can be independently verified.

### Liability

The developers and contributors of MetaRecoverX provide this software **"AS IS"**, without any warranty or guarantee of performance.

By using this tool, you acknowledge that:

- The software is provided without any express or implied warranty.
- The developers are not responsible for any misuse of the tool.
- The developers are not liable for data loss, system damage, or any other consequences resulting from its use.
- Users are encouraged to have proper training or knowledge in digital forensics before using the tool in real investigations.

---

## Acknowledgments

- **Btrfs Developers** — For designing the B-Tree based Copy-On-Write filesystem and providing detailed technical documentation that helped guide the recovery implementation.

- **XFS Development Team** — For their extensive documentation on filesystem structures, which helped in understanding allocation groups, inodes, and recovery mechanisms.

- **The Sleuth Kit Team** — For building foundational open source digital forensics tools that continue to inspire modern forensic software development.

- **Open Source Community** — For the libraries, frameworks, and documentation that support the development of tools like MetaRecoverX.

---

## Platform Support

MetaRecoverX is primarily designed to run on Linux systems, where direct access to modern filesystems and low-level storage devices is most accessible.

- Native support for **Btrfs** and **XFS**, which are commonly used in Linux environments.
- Allows **raw disk access** with the required system permissions, making it possible to analyse storage devices and disk images directly.
- Provides **better performance for disk I/O operations**, which is important for large-scale data recovery tasks.
- Most **digital forensic tools and libraries** are readily available on Linux.

```bash
# Grant user access to disk devices (use carefully)
sudo usermod -aG disk $USER
```

---

## Support the Project

MetaRecoverX is a free and open source project. If you find it useful or interesting:

- **Star the repository** to help others discover the project.
- **Report bugs or suggest improvements** through issues.
- **Contribute code or documentation** if you would like to help improve the platform.
- **Share the project** with others who are interested in digital forensics or cybersecurity.

---

## Final Words

Thank you for taking the time to explore **MetaRecoverX**.

This project was built with a genuine interest in digital forensics and a belief that powerful investigative tools should be accessible to researchers, investigators, and the open source community. Whether you are recovering lost data, analysing digital evidence, or studying cybersecurity, we hope MetaRecoverX proves useful in your work.

Please remember that forensic tools carry responsibility. Always use them with proper authorisation and follow ethical and legal guidelines while conducting investigations.

**Happy investigating!**

*Made with ❤️ by the MetaRecoverX Development Team*
*Last Updated: April 2026*