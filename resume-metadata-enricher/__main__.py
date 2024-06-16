#!/usr/bin/env python

import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from yaml import safe_load as load, safe_dump as dump
import pypdf
from pypdf.errors import PdfReadError
from pprint import pprint

load_dotenv()

import asyncio

from deck.api import NextCloudDeckAPI
from deck.models import Card, Board, Stack, Label

METADATA_FILE = os.environ["METADATA_FILE"]
RESUME_FOLDER = os.environ["RESUME_FOLDER"]

START_BOLD = "\u001b[1m"
END_BOLD = "\033[0m"


def is_nextcloud_enabled():
    """Check whether to enable nextcloud support only if all env vars are set."""
    env_vars = ["NEXTCLOUD_BOARD_ID", "NEXTCLOUD_STACK_ID", "NEXTCLOUD_URL", "NEXTCLOUD_USER", "NEXTCLOUD_PASSWORD"]
    existing_vars = []
    for env_var in env_vars:
        existing_vars.append(os.environ.get(env_var))
    if any(existing_vars) and all(existing_vars):
        print(START_BOLD + "Enabling nextcloud support", END_BOLD)
        return True
    elif not any(existing_vars):
        print(START_BOLD + "No nextcloud support", END_BOLD)
        return False
    else:
        error = f"To enable nextcloud you need to set:\n"
        for i,env_var in enumerate(env_vars):
            if not existing_vars[i]:
                error += f"- {env_var}\n"
        raise Exception(error)



def hydrate_nextcloud(techs: set, nextcloud: dict):
    """Hydrate set of technologies with nextcloud"""
    nc = nextcloud["nc"]
    board_id = nextcloud["board_id"]
    stack_id = nextcloud["stack_id"]

    cards = nc.get_cards_from_stack(board_id=board_id, stack_id=stack_id)
    card: Card

    nextcloud_techs = set()
    for card in cards:
        nextcloud_techs.add(card.title)
        techs.add(card.title)

    # Write
    print("Added to nextcloud:")
    for tech in techs:
        if tech not in nextcloud_techs:
            print(f"- {tech}")
            nc.create_card(board_id=board_id, stack_id=stack_id, title=tech)
    print("\n")
    return techs

def hydrate(nextcloud: dict) -> dict:
    """Hydrate the data from nextcloud and yaml file and return it"""
    # Read
    with open(METADATA_FILE, "r") as stream:
        tech_data = load(stream)
    techs = set(tech_data["technologies"])

    if nextcloud:
        techs = hydrate_nextcloud(techs, nextcloud)

    tech_data["technologies"] = list(sorted(list(techs)))
    with open(METADATA_FILE, "w") as stream:
        stream.write(dump(tech_data, allow_unicode=True))

    return tech_data

def build_metadata(tech_data: dict) -> dict:
    """Build the metadata from the tech_data of nextcoud and yml file"""
    metadata = {}
    for key in tech_data.keys():
        pdfkey = "/"+key.capitalize()
        value = tech_data[key]
        if type(value) == str:
            metadata[pdfkey] = value
        elif type(value) == list:
            metadata[pdfkey] = ",".join(value)
    return metadata


def update_resumes(metadata: dict):
    """Update resumes metadata"""
    # techs = metadata["technologies"]
    folder = os.listdir(RESUME_FOLDER)
    resumes = []

    # Filter only pdf
    for file in folder:
        if file.endswith(".pdf"):
            resumes.append(file)

    for resume in resumes:
        filepath = f"{RESUME_FOLDER}/{resume}"
        print("file:", START_BOLD, filepath.split("/")[-1], END_BOLD)
        update_resume(metadata, filepath)

def update_resume(new_metadata: dict, filepath: str):
    """Update resume metadata"""
    with open(filepath, 'rb') as file:
        reader = pypdf.PdfReader(file)

        # Obtenir les métadonnées
        metadata = {}
        try:
            old_metadata = reader.metadata
            if old_metadata:
                metadata.update(dict(old_metadata.items()))
            else:
                print("No metadata found.")
        except PdfReadError as e:
            print("Impossible to read metadata, keep going anyway")
            print(f"PdfReadError: {e}")
        except Exception as e:
            print("Impossible to read metadata, keep going anyway")
            print(f"Exception: {e}")

        metadata.update(new_metadata)
        pprint(metadata)

        writer = pypdf.PdfWriter(clone_from=filepath)
        writer.add_metadata(metadata)

        # Save the new PDF to a file
        with open(filepath, "wb") as stream:
            writer.write(stream)



async def main():
    """Main"""

    if is_nextcloud_enabled():
        nextcloud = dict(
            board_id = int(os.environ["NEXTCLOUD_BOARD_ID"]),
            stack_id = int(os.environ["NEXTCLOUD_STACK_ID"]),
            nc = NextCloudDeckAPI(
                os.environ["NEXTCLOUD_URL"],
                HTTPBasicAuth(os.environ["NEXTCLOUD_USER"], os.environ["NEXTCLOUD_PASSWORD"]),
                ssl_verify=True,
            )
        )
    else:
        nextcloud = {}

    tech_data =  hydrate(nextcloud)
    metadata = build_metadata(tech_data)
    update_resumes(metadata)

if __name__ == "__main__":
    asyncio.run(main())
