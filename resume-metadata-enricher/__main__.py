#!/usr/bin/env python

import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from yaml import safe_load as load, safe_dump as dump
import pypdf

load_dotenv()

import asyncio

from deck.api import NextCloudDeckAPI
from deck.models import Board, Card, Stack, Label

# optional

TECH_FILE = os.environ["TECH_FILE"]
RESUME_FOLDER = os.environ["RESUME_FOLDER"]

BOARD_ID = int(os.environ["NEXTCLOUD_BOARD_ID"])
STACK_ID = int(os.environ["NEXTCLOUD_STACK_ID"])

nc = NextCloudDeckAPI(
    os.environ["NEXTCLOUD_URL"],
    HTTPBasicAuth(os.environ["NEXTCLOUD_USER"], os.environ["NEXTCLOUD_PASSWORD"]),
    ssl_verify=True,
)

def hydrate() -> dict:
    """Hydrate the data from nextcloud and yaml file and return it"""
    # Read
    with open(TECH_FILE, "r") as stream:
        tech_data = load(stream)
    techs = set(tech_data["technologies"])

    cards = nc.get_cards_from_stack(board_id=BOARD_ID, stack_id=STACK_ID)
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
            nc.create_card(board_id=BOARD_ID, stack_id=STACK_ID, title=tech)
    print("\n")

    tech_data["technologies"] = list(sorted(list(techs)))
    with open(TECH_FILE, "w") as stream:
        stream.write(dump(tech_data, allow_unicode=True))

    return tech_data

def build_metadata(tech_data: dict) -> dict:
    """Build the metadata from the tech_data of nextcoud and yml file"""
    metadata = {}
    for key in tech_data.keys():
        value = tech_data[key]
        if type(value) == str:
            metadata["/"+key.capitalize()] = value
        elif type(value) == list:
            metadata[key] = ",".join(value)
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
        print("filepath:", filepath)
        update_resume(metadata, filepath)

def update_resume(metadata: dict, filepath: str):
    """Update resume metadata"""
    with open(filepath, 'rb') as file:
        reader = pypdf.PdfReader(file)

    # Obtenir les métadonnées
    try:
        metadata = reader.metadata
        print(metadata)
        if metadata:
            # Afficher les métadonnées
            for key, value in metadata.items():
                print(f'{key}: {value}')
    except:
        print("impossible to read metadata")

    writer = pypdf.PdfWriter(clone_from=filepath)
    writer.add_metadata(metadata)

    # Save the new PDF to a file
    with open(filepath, "wb") as stream:
        writer.write(stream)


async def main():
    """Main"""
    tech_data =  hydrate()
    metadata = build_metadata(tech_data)
    update_resumes(metadata)

if __name__ == "__main__":
    asyncio.run(main())
