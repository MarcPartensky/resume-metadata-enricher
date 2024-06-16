# Resume Metadata Enricher
Enrich your resume with metadata to bypass the bots

# Demo
<!-- ![Demo](https://i.imgur.com/QIkz5fb.png) -->
![Demo](./terminalizer/resume-data-enricher.gif)


# Requirements
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
```bash
TECH_FILE="./technologies.yml"
RESUME_FOLDER="./resumes"
```

# Optional Nextcloud Deck support
You can enable nextcloud support to load the technologies from a stack of nextcloud deck.
So if you have a new idea of technologie you can just add it on the go for next time.

You will have to know the id of the board and stack in the nextcloud database.
You can contact your nextcloud administrator to get this information.
```
NEXTCLOUD_URL="https://nextcloud.example.com"
NEXTCLOUD_USER="user"
NEXTCLOUD_PASSWORD="password
NEXTCLOUD_BOARD_ID=1
NEXTCLOUD_STACK_ID=2
```

