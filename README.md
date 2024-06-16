# Resume Metadata Enricher
Enrich your resume with metadata to bypass the bots

# Requirements
- Nextcloud Instance with user account and knowledge of board and stack id
- A PDF file
- Python3.11


# How to use
```sh
# clone the project
git clone https://github.com/MarcPartensky/resume-metadata-enricher
cd resume-metadata-enricher
# Create an .env file with .env.example
mv .env.example .env
# Create a metadata.yml file with metadata.example.yml
mv metadata.example.yml metadata.yml
# Install dependencies for python3.11
pip install -r requirements
# Run the project
python resume-metadata-enricher
```

# Environment variables
```sh
NEXTCLOUD_URL="https://nextcloud.example.com"
NEXTCLOUD_USER="user"
NEXTCLOUD_PASSWORD="password
NEXTCLOUD_BOARD_ID=1
NEXTCLOUD_STACK_ID=2
TECH_FILE="./technologies.yml"
RESUME_FOLDER="./resumes"
```
